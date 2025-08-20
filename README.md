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

## TL;DR — How to run

1) Create & activate venv (or conda), then install deps:
```bash
pip install -U pip
pip install -r voicebot-app/requirements.txt

2) Create .env next to server.py
COHERE_API_KEY=YOUR_COHERE_API_KEY

3) Run backend:
cd voicebot-app
uvicorn server:app --reload --port 8000

4) In a new terminal, serve the frontend:
cd voicebot-app
python -m http.server 5500
# open http://localhost:5500/index.html



