# debug_filter.py
# Run this on any image to see exactly which check rejects it:
#   python debug_filter.py path/to/your/image.jpg

import sys
import cv2
import numpy as np
from PIL import Image

def debug_satellite_filter(path):
    print(f"\n=== Debugging: {path} ===\n")

    img_pil = Image.open(path).convert("RGB")
    img_pil = img_pil.resize((224, 224))
    arr = np.array(img_pil, dtype=np.float32)
    gray = cv2.cvtColor(arr.astype(np.uint8), cv2.COLOR_RGB2GRAY)

    # CHECK 1: Face detection
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
    print(f"CHECK 1 — Face detection:         {'FAIL ❌ faces found: ' + str(len(faces)) if len(faces) > 0 else 'PASS ✅ no faces'}")

    # CHECK 2: Spatial texture
    h, w = gray.shape
    bh, bw = h // 4, w // 4
    block_stds = []
    for r in range(4):
        for c in range(4):
            block = gray[r*bh:(r+1)*bh, c*bw:(c+1)*bw]
            block_stds.append(np.std(block))
    low_texture_blocks = sum(1 for s in block_stds if s < 12)
    print(f"CHECK 2 — Low-texture blocks:     {low_texture_blocks}/16  (threshold: fail if >= 6)")
    print(f"          Block stds: {[round(s,1) for s in block_stds]}")
    print(f"          Result: {'FAIL ❌' if low_texture_blocks >= 6 else 'PASS ✅'}")

    # CHECK 3: Dominant colour
    pixels = arr.reshape(-1, 3).astype(np.uint8)
    quantised = (pixels // 64)
    keys = quantised[:, 0] * 16 + quantised[:, 1] * 4 + quantised[:, 2]
    counts = np.bincount(keys, minlength=64)
    dominant_fraction = counts.max() / counts.sum()
    print(f"CHECK 3 — Dominant colour fraction: {dominant_fraction:.3f}  (threshold: fail if > 0.55)")
    print(f"          Result: {'FAIL ❌' if dominant_fraction > 0.55 else 'PASS ✅'}")

    # CHECK 4: Edge distribution entropy
    edges = cv2.Canny(gray.astype(np.uint8), 50, 150)
    edge_counts = []
    for r in range(4):
        for c in range(4):
            block = edges[r*bh:(r+1)*bh, c*bw:(c+1)*bw]
            edge_counts.append(float(block.sum()))
    total_edges = sum(edge_counts) + 1e-8
    edge_fractions = [e / total_edges for e in edge_counts]
    entropy = -sum(p * np.log(p + 1e-8) for p in edge_fractions)
    edge_uniformity = entropy / np.log(16)
    print(f"CHECK 4 — Edge uniformity:        {edge_uniformity:.3f}  (threshold: fail if < 0.55)")
    print(f"          Result: {'FAIL ❌' if edge_uniformity < 0.55 else 'PASS ✅'}")

    # Overall
    passed = (
        len(faces) == 0 and
        low_texture_blocks < 6 and
        dominant_fraction <= 0.55 and
        edge_uniformity >= 0.55
    )
    print(f"\n{'✅ OVERALL: ACCEPTED as satellite image' if passed else '❌ OVERALL: REJECTED'}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_filter.py path/to/image.jpg")
        sys.exit(1)
    debug_satellite_filter(sys.argv[1])