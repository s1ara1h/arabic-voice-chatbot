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
- 🔐 `.env` support (no secrets in code)


