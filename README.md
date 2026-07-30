# 🎵 MatchMusic AI

An AI-powered web application that analyzes the vibe of an image and recommends music that matches its atmosphere.

Users can upload a photo, and artificial intelligence analyzes the visual mood, detects emotions/styles, and generates personalized music recommendations.

---

## ✨ Features

- 📷 Upload images
- 🤖 AI-powered image analysis
- 🎨 Detect image mood and vibe
- 🎵 Automatic music recommendations
- ▶️ YouTube search links for recommended tracks
- 🌐 User-friendly web interface

## 🛠 Technologies

### Backend

- Python
- FastAPI
- Uvicorn

### Artificial Intelligence

- PyTorch
- Hugging Face Transformers
- CLIP model

### Frontend

- HTML
- CSS
- JavaScript

### APIs

- iTunes Search API
- YouTube search integration


---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/MatchMusic.git
Navigate to the project folder:

cd MatchMusic

Create a virtual environment:

python -m venv .venv

Activate the virtual environment:

macOS / Linux
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt
▶️ Run Locally

Start the FastAPI server:

uvicorn app.main:app --reload

Open your browser:

http://127.0.0.1:8000