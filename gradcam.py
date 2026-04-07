import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import time

output_path = r"C:\Users\vr740\OneDrive\Documents\Environmental-Impact-Prediction-using-Satellite-Data-Machine-Learning\gradcam_outputs\gradcam_result.jpg"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

classes = [
    "AnnualCrop","Forest","HerbaceousVegetation","Highway",
    "Industrial","Pasture","PermanentCrop","Residential",
    "River","SeaLake"
]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

model = models.resnet50(weights=None)
model.fc = nn.Sequential(
    nn.Linear(model.fc.in_features, 256),
    nn.ReLU(),
    nn.Linear(256, len(classes))
)

model.load_state_dict(torch.load("model.pth", map_location=device))
model = model.to(device)
model.eval()

gradients = []
activations = []

def backward_hook(module, grad_in, grad_out):
    gradients.append(grad_out[0])

def forward_hook(module, input, output):
    activations.append(output)

target_layer = model.layer4[-1]

target_layer.register_forward_hook(forward_hook)
target_layer.register_backward_hook(backward_hook)

def generate_gradcam(image_path):
    gradients.clear()
    activations.clear()

    img = Image.open(image_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0).to(device)

    output = model(img_tensor)
    pred_class = output.argmax(dim=1)

    model.zero_grad()
    output[0, pred_class].backward()

    grad = gradients[0].cpu().data.numpy()[0]
    act = activations[0].cpu().data.numpy()[0]

    weights = np.mean(grad, axis=(1, 2))
    cam = np.zeros(act.shape[1:], dtype=np.float32)

    for i, w in enumerate(weights):
        cam += w * act[i]

    cam = np.maximum(cam, 0)
    cam = cv2.resize(cam, (224, 224))
    cam = cam - cam.min()
    cam = cam / cam.max()

    img_np = np.array(img.resize((224, 224)))
    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    superimposed = heatmap * 0.4 + img_np

    # ✅ CREATE FOLDER FIRST
    output_dir = r"C:\Users\vr740\OneDrive\Documents\Environmental-Impact-Prediction-using-Satellite-Data-Machine-Learning\gradcam_outputs"
    os.makedirs(output_dir, exist_ok=True)

    # ✅ UNIQUE FILE NAME
    filename = f"gradcam_{int(time.time())}.jpg"
    output_path = os.path.join(output_dir, filename)

    # ✅ SAVE IMAGE
    cv2.imwrite(output_path, superimposed)

    print(f"Saved: {output_path}")
    print(f"Prediction: {classes[pred_class.item()]}")


# 🔒 SAFE IMAGE PICKER (IMPORTANT)
def get_image(folder):
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path) and file.lower().endswith((".jpg", ".png", ".jpeg")):
            return path
    print(f"No valid image in {folder}")
    exit()


# TEST BOTH IMAGES
before_img = get_image("before")
after_img = get_image("after")

generate_gradcam(before_img)
generate_gradcam(after_img)