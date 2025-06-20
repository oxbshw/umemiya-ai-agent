
import asyncio
import json
import os
import uuid
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment

# Create a FastAPI application
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the 9-trait personality system
class Personality(BaseModel):
    warmth: float
    wit: float
    humor: float
    empathy: float
    conscientiousness: float
    openness: float
    agreeableness: float
    neuroticism: float
    extroversion: float

# Define the request body for the conversation endpoint
class ConversationRequest(BaseModel):
    text: str
    personality: Personality

# Define the request body for the synthesize endpoint
class SynthesizeRequest(BaseModel):
    text: str
    voice_id: str

# In-memory store for voices
voices = {
    "1": "en",
    "2": "fr",
    "3": "es",
}

# Create a directory for audio files
if not os.path.exists("audio"):
    os.makedirs("audio")

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint to verify that the server is running.
    Author: Sayed Allam
    """
    return JSONResponse(content={"status": "ok"})

@app.get("/api/status")
async def get_status():
    """
    Endpoint to get the current status of the AI agent.
    Author: Sayed Allam
    """
    return JSONResponse(content={"status": "running", "personality_traits": 9})

@app.get("/api/voices")
async def get_voices():
    """
    Endpoint to retrieve the available voices for text-to-speech.
    Author: Sayed Allam
    """
    return JSONResponse(content=voices)

@app.post("/api/conversation")
async def conversation(request: ConversationRequest):
    """
    Endpoint to handle conversation with the AI agent.
    Author: Sayed Allam
    """
    p = request.personality
    response_text = f"Received: '{request.text}'. "

    personality_responses = {
        "extroversion": {
            0.7: "I'm so excited to talk to you! ",
        },
        "humor": {
            0.7: "That's a funny thing to say. ",
        },
        "empathy": {
            0.8: "I understand how you feel. ",
        },
        "conscientiousness": {
            0.8: "Let me think about that carefully. ",
        },
    }

    for trait, thresholds in personality_responses.items():
        for threshold, response in thresholds.items():
            if getattr(p, trait) > threshold:
                response_text += response

    try:
        tts = gTTS(response_text, lang='en')
        audio_file_path = f"audio/{uuid.uuid4()}.mp3"
        tts.save(audio_file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {e}")
        
    return JSONResponse(content={"response_text": response_text, "audio_url": f"/{audio_file_path}"})

@app.post("/api/synthesize")
async def synthesize(request: SynthesizeRequest):
    """
    Endpoint for text-to-speech synthesis.
    Author: Sayed Allam
    """
    try:
        tts = gTTS(request.text, lang=voices.get(request.voice_id, 'en'))
        audio_file_path = f"audio/{uuid.uuid4()}.mp3"
        tts.save(audio_file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {e}")
    return FileResponse(audio_file_path)


@app.get("/audio/{file_name}")
async def get_audio(file_name: str):
    return FileResponse(f"audio/{file_name}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time audio streaming.
    Author: Sayed Allam
    """
    await websocket.accept()
    r = sr.Recognizer()
    try:
        while True:
            data = await websocket.receive_bytes()
            with open("audio/temp.wav", "wb") as f:
                f.write(data)
            
            try:
                # Convert webm to wav
                audio = AudioSegment.from_file("audio/temp.wav")
                audio.export("audio/temp_converted.wav", format="wav")

                with sr.AudioFile("audio/temp_converted.wav") as source:
                    audio_data = r.record(source)
                transcript = r.recognize_google(audio_data)
                await websocket.send_json({"transcript": transcript})
            except sr.UnknownValueError:
                await websocket.send_json({"error": "Could not understand audio"})
            except sr.RequestError as e:
                await websocket.send_json({"error": f"Could not request results; {e}"})
            except Exception as e:
                await websocket.send_json({"error": f"An unexpected error occurred: {e}"})

    except WebSocketDisconnect:
        print("WebSocket disconnected")

# Author: Sayed Allam
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
