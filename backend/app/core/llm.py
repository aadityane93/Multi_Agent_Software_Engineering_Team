import asyncio

import httpx
from google import genai

from app.core.config import settings


async def generate_text(prompt: str) -> str:
    provider = settings.llm_provider.lower().strip()

    if provider == "fake":
        return fake_response(prompt)

    if provider == "ollama":
        return await generate_with_ollama(prompt)

    if provider == "gemini":
        return await generate_with_gemini(prompt)

    raise ValueError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")


def fake_response(prompt: str) -> str:
    preview = prompt.strip().replace("\n", " ")[:180]
    return (
        "FAKE LLM OUTPUT\n\n"
        "This is a deterministic placeholder response for local development.\n\n"
        f"Prompt preview:\n{preview}"
    )


async def generate_with_ollama(prompt: str) -> str:
    url = f"{settings.ollama_base_url.rstrip('/')}/api/chat"

    payload = {
        "model": settings.ollama_model,
        "messages": [
            {
                "role": "system",
                "content": "You are a senior software engineering agent. Be precise, structured, and practical.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=180) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

    return data["message"]["content"]


async def generate_with_gemini(prompt: str) -> str:
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is required when LLM_PROVIDER=gemini")

    def _call_gemini() -> str:
        client = genai.Client(api_key=settings.gemini_api_key)
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )
        return response.text or ""

    return await asyncio.to_thread(_call_gemini)