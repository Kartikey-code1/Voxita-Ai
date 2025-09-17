# main.py
print("✅ Voxita backend (Groq + streaming + commands) booting...")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv
from typing import AsyncGenerator, Optional

# Local commands (PC control)
from commands import handle_command

# Groq client wrapper
import api_client

load_dotenv()

app = FastAPI(title="Voxita AI Backend (Groq)", version="3.0.0")

# CORS (frontend on same machine can connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


class ChatRequest(BaseModel):
    message: str
    conversation_history: list = []


class ChatResponse(BaseModel):
    response: str
    executed: Optional[bool] = False
    status: str = "success"


@app.get("/")
async def root():
    return {"message": "Voxita AI Backend is running with Groq", "status": "active"}


# --------------------- CHAT (non-streaming) ---------------------
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    - Checks for local PC commands first via commands.handle_command()
    - If no local command, handles "who created you" override
    - Otherwise calls Groq API for a normal response
    """
    try:
        # 1) local commands (executed locally, e.g., notepad/type)
        cmd_result = handle_command(request.message)
        if cmd_result:
            return ChatResponse(response=cmd_result.get("response", ""), executed=True)

        # 2) manual override for "who created you"
        lower_msg = request.message.lower().strip()
        if any(k in lower_msg for k in ["who created you", "kisne banaya", "who made you", "tumhe kisne banaya"]):
            return ChatResponse(response="I was created by Kartikey Singh.", executed=False)

        # 3) call Groq API
        if not GROQ_API_KEY:
            raise HTTPException(status_code=500, detail="Missing GROQ_API_KEY in environment (.env)")

        # Build messages with optional system instruction
        system_msg = {
            "role": "system",
            "content": "You are Voxita, a helpful assistant. If the user speaks Hindi, reply in Hindi; otherwise use English. Be concise."
        }
        messages = [system_msg] + request.conversation_history + [{"role": "user", "content": request.message}]

        data = await api_client.call_groq(messages=messages)
        # adapt to Groq response format
        resp_text = ""
        try:
            resp_text = data["choices"][0]["message"]["content"]
        except Exception:
            resp_text = json.dumps(data)

        return ChatResponse(response=resp_text, executed=False)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------- STREAMING (SSE) ---------------------
@app.get("/api/stream-chat")
async def stream_chat(message: str, history: str = "[]"):
    """
    Streaming endpoint that provides Server-Sent Events (SSE) chunks.
    If the message is a local command or the creator question, return a small fake stream.
    Otherwise stream from Groq's streaming interface (if supported).
    """
    try:
        # local command check (we stream a small fake response to keep UI consistent)
        cmd_result = handle_command(message)
        if cmd_result:
            async def _fake_cmd_stream() -> AsyncGenerator[str, None]:
                yield f"data: {json.dumps({'chunk': cmd_result.get('response',''), 'status': 'streaming'})}\n\n"
                yield f"data: {json.dumps({'chunk': '', 'status': 'complete'})}\n\n"
            return StreamingResponse(_fake_cmd_stream(), media_type="text/event-stream")

        # manual override for creator streaming
        lower_msg = message.lower().strip()
        if any(k in lower_msg for k in ["who created you", "kisne banaya", "who made you", "tumhe kisne banaya"]):
            async def _creator_stream() -> AsyncGenerator[str, None]:
                yield f"data: {json.dumps({'chunk': 'I was created by Kartikey Singh.', 'status': 'streaming'})}\n\n"
                yield f"data: {json.dumps({'chunk': '', 'status': 'complete'})}\n\n"
            return StreamingResponse(_creator_stream(), media_type="text/event-stream")

        # parse conversation history
        conversation_history = json.loads(history) if history and history != "[]" else []
        system_msg = {
            "role": "system",
            "content": "You are Voxita, a helpful assistant. If the user speaks Hindi, reply in Hindi; otherwise use English. Keep responses clear and concise."
        }
        messages = [system_msg] + conversation_history + [{"role": "user", "content": message}]

        # Streaming generator that yields SSE-formatted lines
        async def generate_stream() -> AsyncGenerator[str, None]:
            async for delta in api_client.stream_groq(messages=messages):
                # delta should be small text fragments
                yield f"data: {json.dumps({'chunk': delta, 'status': 'streaming'})}\n\n"
            # final completion
            yield f"data: {json.dumps({'chunk': '', 'status': 'complete'})}\n\n"

        return StreamingResponse(generate_stream(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------- HEALTH ---------------------
@app.get("/api/health")
async def health_check():
    try:
        if not GROQ_API_KEY:
            return {"status": "unhealthy", "error": "Missing GROQ_API_KEY", "groq_connected": False}
        # quick ping
        system_msg = {"role": "system", "content": "health check"}
        messages = [system_msg, {"role": "user", "content": "ping"}]
        data = await api_client.call_groq(messages=messages)
        return {"status": "healthy", "model": GROQ_MODEL, "groq_connected": True, "sample": (data.get("choices") or [])[:1]}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e), "groq_connected": False}


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Voxita backend with Groq...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
