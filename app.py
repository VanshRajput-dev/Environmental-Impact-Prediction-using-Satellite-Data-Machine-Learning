# ---------------- IMPORTS ---------------- #
from flask import Flask, render_template, request
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import os
import cv2
import numpy as np
import time
import torch.nn.functional as F
from datetime import date

try:
    from sentinel import fetch_sentinel_image, validate_coords, validate_date as validate_sat_date
    SENTINEL_AVAILABLE = True
except ImportError:
    SENTINEL_AVAILABLE = False
    print("[WARNING] sentinel.py dependencies missing. GPS mode disabled.")
    print("  Fix: pip install pystac-client planetary-computer odc-stac rioxarray")

# ---------------- CONFIG ---------------- #
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

classes = [
    "AnnualCrop", "Forest", "HerbaceousVegetation", "Highway",
    "Industrial", "Pasture", "PermanentCrop", "Residential",
    "River", "SeaLake"
]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],   # ✅ FIX: Added ImageNet normalization
                         std=[0.229, 0.224, 0.225])     #    ResNet50 expects normalized input
])

# ---------------- MODEL ---------------- #
model = models.resnet50(weights=None)
model.fc = nn.Sequential(
    nn.Linear(model.fc.in_features, 256),
    nn.ReLU(),
    nn.Dropout(0.3),        # must match train.py exactly
    nn.Linear(256, len(classes))
)

model.load_state_dict(torch.load("model.pth", map_location=device))
model = model.to(device)
model.eval()

# ✅ FIX: Removed global hook registrations entirely.
#    They caused hooks to stack up across calls, making both
#    Grad-CAM outputs look identical (stale activations leaked in).

# ---------------- VALIDATION ---------------- #

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_image(path):
    try:
        img = Image.open(path)
        img.verify()
        return True
    except Exception:
        return False

def is_valid_size(path):
    img = Image.open(path)
    return img.size[0] >= 64 and img.size[1] >= 64

def is_satellite_like(path):
    """
    Minimal filter — only rejects images we are 100% certain are not satellite:
    1. Human face detected
    2. More than 35% skin-tone pixels
    Everything else is accepted. The model itself will give a low-confidence
    score if the image is not a valid land-use patch.
    """
    try:
        img_pil = Image.open(path).convert("RGB")
        img_small = img_pil.resize((224, 224))
        arr  = np.array(img_small, dtype=np.float32)
        gray = cv2.cvtColor(arr.astype(np.uint8), cv2.COLOR_RGB2GRAY)

        # Face detection
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.05, minNeighbors=8, minSize=(50, 50)
        )
        if len(faces) > 0:
            return False

        # Skin tone check
        r_ch = arr[:, :, 0]
        g_ch = arr[:, :, 1]
        b_ch = arr[:, :, 2]
        skin_mask = (
            (r_ch > 95) & (g_ch > 40) & (b_ch > 20) &
            (r_ch > g_ch) & (r_ch > b_ch) &
            ((r_ch - g_ch) > 15) &
            (np.abs(r_ch.astype(int) - g_ch.astype(int)) > 15)
        )
        if skin_mask.sum() / skin_mask.size > 0.35:
            return False

        return True
    except Exception:
        return False


# ---------------- PREDICTION ---------------- #

def predict(image_path):
    img = Image.open(image_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img_tensor)
        probs = F.softmax(output, dim=1)
        conf, pred = torch.max(probs, 1)

    # ✅ Also return top-3 predictions for richer UI display
    top3_probs, top3_idx = torch.topk(probs, 3, dim=1)
    top3 = [
        (classes[top3_idx[0][i].item()], round(top3_probs[0][i].item() * 100, 2))
        for i in range(3)
    ]

    return classes[pred.item()], round(conf.item() * 100, 2), img, top3

# ---------------- GRAD-CAM ---------------- #

def gradcam(img):
    """
    ✅ FIX: All hooks are registered and removed INSIDE this function only.
    No global hook state. Fresh lists per call. Handles edge cases
    where cam.max() == 0 (flat gradient) gracefully.
    """
    img_resized = img.resize((224, 224))
    img_tensor = transform(img_resized).unsqueeze(0).to(device)

    model.eval()
    model.zero_grad()

    # Fresh, isolated lists — no bleed between calls
    gradients = []
    activations = []

    def forward_hook(module, input, output):
        activations.append(output.detach())          # ✅ FIX: detach eagerly to save memory

    def backward_hook(module, grad_in, grad_out):
        gradients.append(grad_out[0].detach())       # ✅ FIX: detach eagerly

    handle_f = model.layer4[-1].register_forward_hook(forward_hook)
    handle_b = model.layer4[-1].register_full_backward_hook(backward_hook)

    try:
        output = model(img_tensor)
        pred_class = output.argmax(dim=1)
        output[0, pred_class].backward()

        if not gradients or not activations:
            raise ValueError("Hooks did not capture gradients/activations.")

        grad = gradients[0].cpu().numpy()[0]   # shape: (C, H, W)
        act  = activations[0].cpu().numpy()[0] # shape: (C, H, W)

        weights = np.mean(grad, axis=(1, 2))   # Global average pooling over spatial dims
        cam = np.zeros(act.shape[1:], dtype=np.float32)

        for i, w in enumerate(weights):
            cam += w * act[i]

        cam = np.maximum(cam, 0)               # ReLU
        cam_max = cam.max()

        if cam_max == 0:
            # ✅ FIX: If gradient is flat (model is very confident / no gradient flow),
            #    return a neutral blue heatmap overlay instead of dividing by zero.
            cam = np.zeros((224, 224), dtype=np.float32)
        else:
            cam = cam / cam_max

        cam = cv2.resize(cam, (224, 224))

        # Reconstruct original-scale numpy image for overlay (without normalization artifacts)
        img_np = np.array(img_resized, dtype=np.uint8)

        heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
        heatmap_rgb = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)  # ✅ FIX: convert to RGB before blending

        superimposed = (heatmap_rgb * 0.4 + img_np * 0.6).astype(np.uint8)  # ✅ FIX: balanced blend + uint8 cast

        filename = f"gradcam_{int(time.time() * 1000)}.jpg"   # ✅ FIX: millisecond timestamp avoids collisions
        path = os.path.join(OUTPUT_FOLDER, filename)

        # ✅ FIX: Save as RGB (PIL) instead of BGR (cv2.imwrite) to avoid color shift
        Image.fromarray(superimposed).save(path, quality=92)

        return filename

    finally:
        # ✅ FIX: Always remove hooks, even if an exception occurs
        handle_f.remove()
        handle_b.remove()

# ---------------- IMPACT ---------------- #

# ✅ FIX: Expanded impact classification — original only had 3 rules,
#    meaning most class changes returned a generic "Land Use Change" message.
IMPACT_RULES = {
    ("Forest",                "Industrial"):          ("Deforestation → Industrial 🌳🏭", "HIGH 🔴"),
    ("Forest",                "Residential"):         ("Deforestation → Residential 🌳🏘️", "HIGH 🔴"),
    ("Forest",                "AnnualCrop"):          ("Deforestation → Agriculture 🌳🌾", "HIGH 🔴"),
    ("Forest",                "PermanentCrop"):       ("Deforestation → Agriculture 🌳🌾", "MEDIUM 🟡"),
    ("Forest",                "HerbaceousVegetation"):("Forest Degradation 🌳⚠️",         "MEDIUM 🟡"),
    ("HerbaceousVegetation",  "Industrial"):          ("Greenland Urbanization 🌿🏭",      "HIGH 🔴"),
    ("HerbaceousVegetation",  "Residential"):         ("Greenland Urbanization 🌿🏘️",      "HIGH 🔴"),
    ("Pasture",               "Industrial"):          ("Agricultural Land Lost 🐄🏭",      "HIGH 🔴"),
    ("Pasture",               "Residential"):         ("Agricultural Land Lost 🐄🏘️",      "MEDIUM 🟡"),
    ("River",                 "Residential"):         ("Water Encroachment 🌊🏘️",          "HIGH 🔴"),
    ("River",                 "Industrial"):          ("Water Encroachment 🌊🏭",          "HIGH 🔴"),
    ("SeaLake",               "Residential"):         ("Coastal Encroachment 🌊🏘️",        "HIGH 🔴"),
    ("AnnualCrop",            "Residential"):         ("Farmland Urbanization 🌾🏘️",       "MEDIUM 🟡"),
    ("AnnualCrop",            "Industrial"):          ("Farmland Industrialized 🌾🏭",      "HIGH 🔴"),
    ("Residential",           "Industrial"):          ("Residential → Industrial 🏘️🏭",    "MEDIUM 🟡"),
    ("Industrial",            "Forest"):              ("Industrial Reforestation 🏭🌳",     "LOW 🟢"),
    ("Industrial",            "HerbaceousVegetation"):("Industrial → Green Recovery 🏭🌿", "LOW 🟢"),
}

def classify_impact(before, after):
    if before == after:
        return "No Significant Change ✅", "LOW 🟢"
    result = IMPACT_RULES.get((before, after))
    if result:
        return result
    return f"Land Use Change: {before} → {after} ⚠️", "MEDIUM 🟡"

# ---------------- ROUTE ---------------- #

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        before_file = request.files.get("before")
        after_file  = request.files.get("after")

        if not before_file or not after_file:
            return render_template("index.html", error="Please upload both images.")

        if not (allowed_file(before_file.filename) and allowed_file(after_file.filename)):
            return render_template("index.html", error="Only JPG/PNG files are allowed.")

        timestamp   = int(time.time() * 1000)
        before_name = f"{timestamp}_before.jpg"
        after_name  = f"{timestamp}_after.jpg"

        before_path = os.path.join(UPLOAD_FOLDER, before_name)
        after_path  = os.path.join(UPLOAD_FOLDER, after_name)

        before_file.save(before_path)
        after_file.save(after_path)

        if not is_valid_image(before_path) or not is_valid_image(after_path):
            return render_template("index.html", error="One or both files are not valid images.")

        if not is_valid_size(before_path) or not is_valid_size(after_path):
            return render_template("index.html", error="Images must be at least 64×64 pixels.")

        before_sat = is_satellite_like(before_path)
        after_sat  = is_satellite_like(after_path)
        print(f"[DEBUG] before_sat={before_sat}  after_sat={after_sat}")
        if not before_sat or not after_sat:
            which = "Before" if not before_sat else "After"
            return render_template("index.html", error=f"{which} image was rejected by the satellite filter. If this is a real satellite image, please report it.")

        # PREDICT
        before_pred, before_conf, before_img, before_top3 = predict(before_path)
        after_pred,  after_conf,  after_img,  after_top3  = predict(after_path)

        impact, severity = classify_impact(before_pred, after_pred)

        before_cam = gradcam(before_img)
        after_cam  = gradcam(after_img)

        return render_template("index.html",
            before=before_name,
            after=after_name,
            before_pred=before_pred,
            after_pred=after_pred,
            before_conf=before_conf,
            after_conf=after_conf,
            before_top3=before_top3,
            after_top3=after_top3,
            impact=impact,
            severity=severity,
            before_cam=before_cam,
            after_cam=after_cam
        )

    return render_template("index.html")


# ---------------- GPS ROUTE ---------------- #

@app.route("/gps", methods=["GET", "POST"])
def gps():
    if not SENTINEL_AVAILABLE:
        return render_template("gps.html",
            error="GPS dependencies not installed. Run: pip install pystac-client planetary-computer odc-stac rioxarray",
            today=date.today().isoformat()
        )

    if request.method == "POST":
        try:
            lat         = float(request.form["lat"])
            lon         = float(request.form["lon"])
            date_before = request.form["date_before"].strip()
            date_after  = request.form["date_after"].strip()
        except (KeyError, ValueError):
            return render_template("gps.html",
                error="Please fill in all fields with valid values.",
                today=date.today().isoformat()
            )

        try:
            validate_coords(lat, lon)
            validate_sat_date(date_before)
            validate_sat_date(date_after)
        except ValueError as e:
            return render_template("gps.html", error=str(e), today=date.today().isoformat())

        if date_before >= date_after:
            return render_template("gps.html",
                error="'Before' date must be earlier than 'After' date.",
                today=date.today().isoformat()
            )

        timestamp   = int(time.time() * 1000)
        before_name = f"{timestamp}_before.jpg"
        after_name  = f"{timestamp}_after.jpg"
        before_path = os.path.join(UPLOAD_FOLDER, before_name)
        after_path  = os.path.join(UPLOAD_FOLDER, after_name)

        try:
            fetch_sentinel_image(lat, lon, date_before, before_path)
            fetch_sentinel_image(lat, lon, date_after,  after_path)
        except (RuntimeError, EnvironmentError) as e:
            return render_template("gps.html", error=str(e), today=date.today().isoformat())
        except Exception as e:
            return render_template("gps.html",
                error=f"Unexpected error: {str(e)}",
                today=date.today().isoformat()
            )

        before_pred, before_conf, before_img, before_top3 = predict(before_path)
        after_pred,  after_conf,  after_img,  after_top3  = predict(after_path)
        impact, severity = classify_impact(before_pred, after_pred)
        before_cam = gradcam(before_img)
        after_cam  = gradcam(after_img)

        return render_template("gps.html",
            lat=lat, lon=lon,
            date_before=date_before,
            date_after=date_after,
            before=before_name,
            after=after_name,
            before_pred=before_pred,
            after_pred=after_pred,
            before_conf=before_conf,
            after_conf=after_conf,
            before_top3=before_top3,
            after_top3=after_top3,
            impact=impact,
            severity=severity,
            before_cam=before_cam,
            after_cam=after_cam,
            today=date.today().isoformat(),
        )

    return render_template("gps.html", today=date.today().isoformat())


if __name__ == "__main__":
    app.run(debug=True)