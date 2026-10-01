import json
import logging
import httpx
from typing import Type, TypeVar, Optional, Dict, Any
from pydantic import BaseModel
from app.config import settings

logger = logging.getLogger("bharatresolve.llm")

T = TypeVar("T", bound=BaseModel)

async def call_llm(
    prompt: str,
    system_instruction: str = "You are an AI Assistant for BharatResolve AI.",
    response_schema: Optional[Type[T]] = None,
    temperature: float = 0.2,
) -> str:
    """
    Resilient multi-provider LLM caller.
    Tries Gemini API -> Groq API -> Ollama Local (11434) fallback.
    """
    if settings.GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": f"{system_instruction}\n\n{prompt}"}]
                    }
                ],
                "generationConfig": {
                    "temperature": temperature,
                }
            }
            if response_schema:
                payload["generationConfig"]["responseMimeType"] = "application/json"

            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        return candidates[0]["content"]["parts"][0]["text"]
        except Exception as e:
            logger.warning(f"Gemini API call failed: {e}")

    if settings.GROQ_API_KEY:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}"}
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature
            }
            if response_schema:
                payload["response_format"] = {"type": "json_object"}

            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(url, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.warning(f"Groq API call failed: {e}")

    try:
        url = f"{settings.OLLAMA_BASE_URL}/api/generate"
        full_prompt = f"System: {system_instruction}\nUser: {prompt}\nReturn strict raw JSON object with fields: domain, intent, normalized_problem, urgency, missing_information, detected_language."
        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": full_prompt,
            "stream": False,
            "options": {"temperature": temperature}
        }
        if response_schema:
            payload["format"] = "json"

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("response", "")
    except Exception as e:
        logger.error(f"Ollama local LLM call failed: {e}")

    if response_schema:
        return schema_default_json(response_schema)
    return "LLM service currently unreachable."

def schema_default_json(schema: Type[T]) -> str:
    try:
        return schema().model_dump_json()
    except Exception:
        return "{}"

async def call_llm_structured(
    prompt: str,
    schema: Type[T],
    system_instruction: str = "Extract structured output matching JSON schema precisely.",
) -> T:
    raw_text = await call_llm(
        prompt=prompt,
        system_instruction=system_instruction + f"\nUse JSON keys: {list(schema.model_fields.keys())}.",
        response_schema=schema,
        temperature=0.1
    )
    
    cleaned = raw_text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
        # Unwrap nested wrapper object e.g. {"CaseIntent": {...}}
        if isinstance(data, dict) and len(data) == 1:
            first_val = list(data.values())[0]
            if isinstance(first_val, dict):
                data = first_val

        # Map common capitalized or alternate keys if needed
        key_mappings = {
            "Category": "domain", "Domain": "domain",
            "Intent": "intent", "Goal": "intent",
            "ProblemStatement": "normalized_problem", "Problem": "normalized_problem",
            "Urgency": "urgency",
            "MissingInformation": "missing_information",
            "Language": "detected_language"
        }
        mapped_data = {}
        for k, v in data.items():
            mapped_key = key_mappings.get(k, k)
            mapped_data[mapped_key] = v

        return schema.model_validate(mapped_data)
    except Exception as e:
        logger.warning(f"JSON parsing/validation error: {e}. Falling back to default schema instance.")
        try:
            return schema()
        except Exception:
            return schema.model_construct()
