# api_client.py
import os
import json
import httpx
from typing import AsyncGenerator

GROQ_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


async def call_groq(messages, timeout: float = 60.0):
    """
    Non-streaming call to Groq chat completions.
    Returns parsed JSON response.
    """
    if not GROQ_KEY:
        raise RuntimeError("Missing GROQ_API_KEY in environment")
    headers = {"Authorization": f"Bearer {GROQ_KEY}"}
    payload = {"model": GROQ_MODEL, "messages": messages}

    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(GROQ_URL, headers=headers, json=payload)
        r.raise_for_status()
        return r.json()


async def stream_groq(messages) -> AsyncGenerator[str, None]:
    """
    Stream deltas from Groq's streaming response.
    Yields content text fragments (strings).
    Note: This expects Groq to send SSE-like `data:` lines or chunked JSON lines.
    """
    if not GROQ_KEY:
        raise RuntimeError("Missing GROQ_API_KEY in environment")
    headers = {"Authorization": f"Bearer {GROQ_KEY}"}
    payload = {"model": GROQ_MODEL, "messages": messages, "stream": True}

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", GROQ_URL, headers=headers, json=payload) as response:
            response.raise_for_status()
            async for raw_line in response.aiter_lines():
                if not raw_line:
                    continue
                # Groq streaming format may emit lines starting with "data: "
                line = raw_line.strip()
                if line.startswith("data: "):
                    raw = line[len("data: "):]
                else:
                    raw = line
                if raw == "[DONE]":
                    break
                try:
                    data = json.loads(raw)
                    # try to access delta content
                    choices = data.get("choices") or []
                    if choices:
                        # support OpenAI-like streaming: choices[0]["delta"].get("content")
                        delta = choices[0].get("delta", {}).get("content")
                        if delta:
                            yield delta
                        else:
                            # fallback: full message content
                            msg = choices[0].get("message", {}).get("content")
                            if msg:
                                yield msg
                    else:
                        # fallback: try top-level content
                        cont = data.get("content")
                        if cont:
                            yield cont
                except Exception:
                    # ignore parse errors (can happen if partial JSON)
                    continue
