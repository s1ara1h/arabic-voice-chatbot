# arabic-voice-chatbot
Voice chatbot in **Arabic**: local **STT** via `faster-whisper`, conversational **LLM** via **Cohere Chat v2**, and **TTS** via `gTTS`.  
Frontend: a minimal HTML page to record → send → play the reply.

---

## Demo
The demo video is included in this repository

---

## Features
- 🎤 **Speech-to-Text** (Arabic) locally with **faster-whisper** (+ VAD, beam search)
- 🤖 **Cohere** conversational replies (model: `command-a-03-2025`)
- 🔊 **Text-to-Speech** using **gTTS** (Arabic)
- ⚡ **FastAPI** backend + plain HTML frontend

---

## 🚀 How to Run

### 1. Setup Environment
Create and activate virtual environment, then install dependencies:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Update pip and install dependencies
pip install -U pip
pip install -r voicebot-app/requirements.txt
```

### 2. Environment Configuration
Create `.env` file next to `server.py`:
```env
COHERE_API_KEY=YOUR_COHERE_API_KEY
```

### 3. Run Backend Server
```bash
cd voicebot-app
uvicorn server:app --reload --port 8000
```

### 4. Serve Frontend
In a new terminal window:
```bash
cd voicebot-app
python -m http.server 5500
```

Then open your browser and navigate to: `http://localhost:5500/index.html`

---

**Note:** Make sure both backend (port 8000) and frontend (port 5500) are running simultaneously.



