"""
Voice chatbot API: STT (faster-whisper) -> Cohere chat -> TTS (gTTS)

Endpoint:
  POST /voice-chat
    form-data field name: "audio" (webm/ogg/wav/mp3)
Response JSON:
  {
    "transcript": "...",
    "reply_text": "...",
    "reply_audio_b64": "..."  # MP3 as base64
  }

Env vars:
  COHERE_API_KEY              (required)
  WHISPER_MODEL_SIZE          [default: "small"]  # tiny/base/small/medium/large-v3
  WHISPER_DEVICE              [default: "cpu"]    # "cpu" or "cuda"
  WHISPER_COMPUTE_TYPE        [default: "int8"]   # e.g., int8, int8_float16, float16
"""

import os
import io
import base64
import tempfile
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from gtts import gTTS
import cohere
from faster_whisper import WhisperModel

# ---------- Config ----------
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise RuntimeError("COHERE_API_KEY is not set")

WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "small")
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
WHISPER_COMPUTE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")

SYSTEM_PROMPT = (
    "You are a helpful Arabic conversational assistant. "
    "Keep answers concise, clear, and actionable."
)

# ---------- App ----------
app = FastAPI(title="Voicebot (faster-whisper + Cohere + gTTS)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Load models/clients once (cold start may download the Whisper model)
stt_model = WhisperModel(
    WHISPER_MODEL_SIZE, device=WHISPER_DEVICE, compute_type=WHISPER_COMPUTE
)
co = cohere.ClientV2(api_key=COHERE_API_KEY)

# ---------- Schemas ----------
class ChatResponse(BaseModel):
    transcript: str
    reply_text: str
    reply_audio_b64: str

# ---------- Helpers ----------
def cohere_chat(user_text: str) -> str:
    """Call Cohere Chat v2 and return plain text."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_text},
    ]
    resp = co.chat(model="command-a-03-2025", messages=messages)

    chunks: List[str] = []
    if getattr(resp, "message", None) and getattr(resp.message, "content", None):
        for block in resp.message.content:
            if getattr(block, "type", "") == "text" and getattr(block, "text", ""):
                chunks.append(block.text)
    text = "\n".join(chunks).strip()
    return text or "تم."

def tts_mp3_b64(text: str, lang: str = "ar") -> str:
    """Synthesize MP3 with gTTS and return base64 string."""
    buf = io.BytesIO()
    gTTS(text, lang=lang).write_to_fp(buf)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

# ---------- Routes ----------
@app.post("/voice-chat", response_model=ChatResponse)
async def voice_chat(audio: UploadFile = File(...)):
    # Save uploaded audio to a temp file
    suffix = "." + (audio.filename.split(".")[-1].lower() if audio.filename and "." in audio.filename else "webm")
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        raw = await audio.read()
        tmp.write(raw)
        tmp_path = tmp.name

    # Transcribe (Arabic)
    try:
        segments, info = stt_model.transcribe(
            tmp_path, language="ar", vad_filter=True, beam_size=5
        )
        transcript = "".join(seg.text for seg in segments).strip()
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

    # LLM reply
    user_text = transcript or "لم يصل نص واضح."
    reply_text = cohere_chat(user_text)

    # TTS
    reply_audio_b64 = tts_mp3_b64(reply_text, lang="ar")

    return JSONResponse(
        content=ChatResponse(
            transcript=transcript,
            reply_text=reply_text,
            reply_audio_b64=reply_audio_b64,
        ).model_dump()
    )
