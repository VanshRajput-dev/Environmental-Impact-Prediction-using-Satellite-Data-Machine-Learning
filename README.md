# 🌍 Environmental Impact Prediction using Satellite Data (ML)

This project uses Machine Learning to detect environmental changes such as deforestation, urban expansion, and water body changes using satellite images.

---

## 🚀 Project Overview

The system analyzes **before and after satellite images** and predicts land-use categories to identify environmental impact.

### 🔍 Example:
- Forest → Industrial → Deforestation 🚨  
- River → Residential → Encroachment 🚨  
- Forest → Forest → No Change ✅  

---

## 🧠 Model

- Convolutional Neural Network (CNN)
- Trained on EuroSAT dataset
- Multi-class classification:
  - Forest
  - Industrial
  - Residential
  - River
  - Sea/Lake
  - etc.

---

## 📂 Project Structure
├── dataset/ # Raw dataset (EuroSAT)
├── data/ # Train / Val / Test split
│ ├── train/
│ ├── val/
│ ├── test/
│
├── before/ # Before images
├── after/ # After images
│
├── model.py # Training script
├── predict.py # Prediction script
├── model.pth # Trained model
├── requirements.txt
└── README.md

---

## ⚙️ Setup

### 1. Clone the repository

git clone https://github.com/your-username/your-repo-name.git

cd your-repo-name


### 2. Install dependencies

pip install -r requirements.txt


---

## ▶️ Training


python model.py


---

## 🔮 Prediction (Coming Soon)


python predict.py


This will:
- Take before & after images
- Predict land categories
- Detect environmental change

---

## 📊 Dataset

- EuroSAT Dataset (RGB Satellite Images)
- 10 Land Use Classes

---

## 💡 Future Improvements

- Add segmentation for precise change detection
- Use ResNet / Transfer Learning for higher accuracy
- Add GUI / Web App
- Show % change heatmaps

---

## 🧑‍💻 Author

Vansh Rajput  
B.Tech Data Science | SRM University  

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!

add image verfication if its satlit image or not 