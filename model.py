# train.py — Fixed EuroSAT ResNet50 training script
# Fixes: normalization mismatch, frozen backbone, epoch labelling, LR scheduling

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from tqdm import tqdm

torch.backends.cudnn.benchmark = True
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

if __name__ == "__main__":

        # ── FIX 1: Add ImageNet normalization — MUST match app.py exactly ─────────────
        # Training and inference must use identical preprocessing.
        # Your app.py already had Normalize() but training didn't — this caused the
        # model to see completely different pixel distributions at inference time.
        transform_train = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),          # free augmentation for satellite images
            transforms.RandomVerticalFlip(),            # satellite images have no natural orientation
            transforms.ColorJitter(brightness=0.2, contrast=0.2),  # simulate lighting variation
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],       # ImageNet stats
                                 std=[0.229, 0.224, 0.225]),
        ])

        transform_val = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])

        train_data = datasets.ImageFolder("data/train", transform=transform_train)
        val_data   = datasets.ImageFolder("data/val",   transform=transform_val)

        print(f"Classes: {train_data.classes}")
        print(f"Train: {len(train_data)} images | Val: {len(val_data)} images")

        train_loader = DataLoader(train_data, batch_size=64, shuffle=True,  num_workers=0, pin_memory=True)
        val_loader   = DataLoader(val_data,   batch_size=64, shuffle=False, num_workers=0, pin_memory=True)

        # ── FIX 2: Unfreeze layer3 + layer4 for domain adaptation ────────────────────
        # ResNet50 was pretrained on ImageNet (natural photos, not satellite images).
        # Keeping the entire backbone frozen means the model extracts ImageNet-style
        # features (edges, textures of objects) rather than satellite-relevant features
        # (spectral patterns, land-use geometry). Unfreezing the last two layer groups
        # lets the model adapt to the satellite domain while keeping early features stable.
        model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)

        # Freeze early layers (keep ImageNet low-level features: edges, colours)
        for name, param in model.named_parameters():
            if "layer1" in name or "layer2" in name:
                param.requires_grad = False

        # Unfreeze layer3, layer4, and fc (adapt to satellite domain)
        for name, param in model.named_parameters():
            if "layer3" in name or "layer4" in name or "fc" in name:
                param.requires_grad = True

        model.fc = nn.Sequential(
            nn.Linear(model.fc.in_features, 256),
            nn.ReLU(),
            nn.Dropout(0.3),                   # dropout helps prevent overfit on small heads
            nn.Linear(256, len(train_data.classes))
        )

        model = model.to(device)

        # ── FIX 3: Two param groups — lower LR for backbone, higher for FC ───────────
        # The backbone already has good weights — nudge them gently (1e-4).
        # The FC head starts random — train it faster (1e-3).
        backbone_params = [p for n, p in model.named_parameters()
                           if p.requires_grad and "fc" not in n]
        head_params     = list(model.fc.parameters())

        optimizer = optim.Adam([
            {"params": backbone_params, "lr": 1e-4},
            {"params": head_params,     "lr": 1e-3},
        ])

        criterion = nn.CrossEntropyLoss()

        # ── FIX 4: LR scheduler + proper epoch loop ───────────────────────────────────
        # ReduceLROnPlateau halves LR when val accuracy stops improving.
        # This replaces the fixed LR that kept training at full speed when the model
        # had already converged (causing overfitting in later epochs).
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode="max", factor=0.5, patience=2
        )

        NUM_EPOCHS  = 15
        best_val_acc = 0.0

        for epoch in range(NUM_EPOCHS):                         # FIX: range(0, NUM_EPOCHS) not range(10,15)
            # ── Train ──────────────────────────────────────────────────────────────
            model.train()
            total_loss   = 0.0
            train_correct = 0
            train_total   = 0

            loop = tqdm(train_loader, desc=f"Epoch {epoch+1}/{NUM_EPOCHS} [train]")
            for images, labels in loop:
                images = images.to(device, non_blocking=True)
                labels = labels.to(device, non_blocking=True)

                optimizer.zero_grad()
                outputs = model(images)
                loss    = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                total_loss    += loss.item()
                preds          = outputs.argmax(dim=1)
                train_correct += (preds == labels).sum().item()
                train_total   += labels.size(0)
                loop.set_postfix(loss=f"{loss.item():.3f}")

            train_acc = 100 * train_correct / train_total

            # ── Validate ────────────────────────────────────────────────────────────
            model.eval()
            val_correct = 0
            val_total   = 0

            with torch.no_grad():
                for images, labels in tqdm(val_loader, desc=f"Epoch {epoch+1}/{NUM_EPOCHS} [val]  "):
                    images = images.to(device)
                    labels = labels.to(device)
                    outputs = model(images)
                    preds   = outputs.argmax(dim=1)
                    val_correct += (preds == labels).sum().item()
                    val_total   += labels.size(0)

            val_acc = 100 * val_correct / val_total

            print(f"\nEpoch {epoch+1}/{NUM_EPOCHS} | "
                  f"Loss: {total_loss:.2f} | "
                  f"Train acc: {train_acc:.1f}% | "
                  f"Val acc: {val_acc:.1f}%")

            # Step scheduler on val accuracy
            scheduler.step(val_acc)
            current_lr = optimizer.param_groups[0]["lr"]
            print(f"  LR backbone: {current_lr:.2e}")

            # Save best model only
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                torch.save(model.state_dict(), "model.pth")
                print(f"  Saved new best model (val acc: {val_acc:.1f}%)")

        print(f"\nTraining complete. Best val accuracy: {best_val_acc:.1f}%")
        print("Model saved to model.pth")