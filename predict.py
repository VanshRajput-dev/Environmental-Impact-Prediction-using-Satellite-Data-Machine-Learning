import torch
import os
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

classes = [
    "AnnualCrop","Forest","HerbaceousVegetation","Highway",
    "Industrial","Pasture","PermanentCrop","Residential",
    "River","SeaLake"
]

model = models.resnet50(weights=None)
model.fc = nn.Sequential(
    nn.Linear(model.fc.in_features, 256),
    nn.ReLU(),
    nn.Linear(256, len(classes))
)

model.load_state_dict(torch.load("model.pth", map_location=device))
model = model.to(device)
model.eval()

def predict(image_path):
    img = Image.open(image_path).convert("RGB")
    img = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img)
        _, pred = torch.max(output, 1)

    return classes[pred.item()]

before_img = os.path.join("before", os.listdir("before")[0])
after_img = os.path.join("after", os.listdir("after")[0])

before_pred = predict(before_img)
after_pred = predict(after_img)

print("Before:", before_pred)
print("After:", after_pred)

if before_pred != after_pred:
    print("Change Detected 🚨")
    print(f"{before_pred} → {after_pred}")
else:
    print("No Significant Change ✅")