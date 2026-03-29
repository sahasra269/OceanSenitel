# 🌊 Ocean Sentinel

> AI-Powered Ocean Pollution Detection System

Ocean Sentinel is a real-time ocean pollution detection platform that uses deep learning to identify and classify waste materials — plastic, glass, metal, paper, cardboard, and trash — from images captured by drones or boats. Detections are plotted live on an interactive map, giving coastguards and environmental teams a real-time view of pollution hotspots.

---

## 🏗️ Built On

This project builds upon the open-source [tensorflow-image-detection](https://github.com/antiplasti/Plastic-Detection-Model) repo by Arun Michael Dsouza & Royal Bhati (MIT License), which we:
- Migrated fully from **TensorFlow 1.x → TensorFlow 2.x** for Apple Silicon (M1/M2/M3) compatibility
- Extended with a **Flask REST API**, **React dashboard**, and **Firebase integration**
- Retrained with **8000 steps** for improved accuracy

Dataset sourced from [TrashNet](https://github.com/garythung/trashnet) by Gary Thung (Stanford).

---

## 🎯 What It Does

```
Drone / Boat captures image
        ↓
Flask API receives image + GPS coordinates
        ↓
Inception v3 model classifies waste type
        ↓
Result saved to Firebase (cloud)
        ↓
React dashboard plots detection live on map
```

---

## 🧠 Model

- **Architecture**: Google Inception v3 (pre-trained on ImageNet)
- **Technique**: Transfer Learning — retrained final layer on waste dataset
- **Categories**: Plastic, Glass, Metal, Paper, Cardboard, Trash
- **Training Steps**: 8000
- **Final Test Accuracy**: ~90%
- **Dataset**: ~2500 images from TrashNet

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| ML Model | TensorFlow 2.x + Inception v3 |
| Backend API | Flask + Flask-CORS |
| Frontend | React.js |
| Map | Leaflet.js + React-Leaflet |
| Database | Google Firebase Realtime Database |
| Auth | Firebase Authentication |

---

## 📁 Project Structure

```
Plastic-Detection-Model/
├── retrain.py              # Transfer learning script (TF2 compatible)
├── classify.py             # CLI image classifier
├── app.py                  # Flask REST API
├── firebase.py             # Firebase integration
├── env.py                  # Environment credentials (not committed)
├── service.py              # Background service for drone/Pi deployment
├── train.sh                # Training shell script
├── training_dataset/       # Image dataset (6 categories)
├── dashboard/              # React frontend
│   ├── src/
│   │   ├── App.js          # Main dashboard component
│   │   └── App.css         # Styling
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 18+
- pip
- A Firebase project ([set one up here](https://console.firebase.google.com))

---

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/ocean-sentinel.git
cd ocean-sentinel
```

### 2. Set up Python environment

```bash
python3 -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
```

### 3. Install Python dependencies

```bash
pip install tensorflow-macos   # Apple Silicon Mac
# OR
pip install tensorflow         # Intel Mac / Linux / Windows

pip install flask flask-cors pyrebase4 tensorboard
```

### 4. Configure Firebase credentials

Create `env.py` in the project root (this file is gitignored):

```python
auth_cred = {
    "API_KEY": "your_api_key",
    "AUTH_DOMAIN": "your-project.firebaseapp.com",
    "DATABASE_URL": "https://your-project-default-rtdb.firebaseio.com",
    "STORAGE_BUCKET": "your-project.firebasestorage.app",
    "EMAIL": "your@email.com",
    "PASS": "yourpassword",
    "B_ID": "B-001"
}
```

### 5. Download the dataset

[Download Dataset](https://bit.ly/3mcb3aS) and unzip into the project root:

```
training_dataset/
├── plastic/
├── glass/
├── metal/
├── paper/
├── cardboard/
└── trash/
```

### 6. Train the model

```bash
python3 retrain.py \
  --image_dir ./training_dataset \
  --how_many_training_steps=8000
```

Training takes 30–60 minutes. Expected accuracy: **85–95%**.

### 7. Test the classifier

```bash
python3 classify.py path/to/image.jpg
```

Example output:
```
plastic:   94.4%
glass:      3.3%
metal:      1.5%
paper:      0.7%
trash:      0.1%
cardboard:  0.1%
```

### 8. Start the Flask API

```bash
python3 app.py
```

API runs at `http://localhost:8080`

### 9. Start the React dashboard

```bash
cd dashboard
npm install
npm start
```

Dashboard opens at `http://localhost:3000`

---

## 🌐 API Reference

### Health Check
```
GET /status
→ "Running!"
```

### Detect Pollution
```
POST /detect
Content-Type: application/json

{
  "image": "<base64 encoded image>",
  "lat": 8.5,
  "lng": 72.3
}

→ {
    "plastic": 0.944,
    "glass": 0.033,
    "metal": 0.015,
    "paper": 0.007,
    "trash": 0.001,
    "cardboard": 0.001,
    "lat": 8.5,
    "lng": 72.3
  }
```

---

## 📸 Dashboard

- **Upload any image** of ocean waste
- **Enter GPS coordinates** of where it was captured
- **Get instant classification** with confidence scores
- **See it plotted live** on the ocean map
- **Zoom in** to see pollution hotspots in detail

---

## ⚠️ Important Notes

- `env.py` is gitignored — never commit your Firebase credentials
- The model file (`/tmp/output_graph.pb`) is generated locally after training
- For production deployment, replace the Flask dev server with Gunicorn

---

## 📜 Original License

MIT License — Copyright (c) 2017 Arun Michael Dsouza

This project extends the original work under the same MIT License.
See [LICENSE](LICENSE) for full details.

---

## 🙏 Acknowledgements

- [tensorflow-image-detection](https://github.com/antiplasti/Plastic-Detection-Model) — base model and architecture
- [TrashNet](https://github.com/garythung/trashnet) — dataset by Gary Thung, Stanford University
- [Google Inception v3](https://research.googleblog.com/2016/03/train-your-own-image-classifier-with.html) — pre-trained model