# arabic-voice-chatbot
Voice chatbot in **Arabic**: local **STT** via `faster-whisper`, conversational **LLM** via **Cohere Chat v2**, and **TTS** via `gTTS`.  
Frontend: a minimal HTML page to record → send → play the reply.

---

## Demo

<!-- Option A: video in repo root -->
![Demo video](https://raw.githubusercontent.com/s1ara1h/arabic-voice-chatbo/main/demo.mp4)


---

## Features
- 🎤 **Speech-to-Text** (Arabic) locally with **faster-whisper** (+ VAD, beam search)
- 🤖 **Cohere** conversational replies (model: `command-a-03-2025`)
- 🔊 **Text-to-Speech** using **gTTS** (Arabic)
- ⚡ **FastAPI** backend + plain HTML frontend
- 🔐 `.env` support (no secrets in code)


