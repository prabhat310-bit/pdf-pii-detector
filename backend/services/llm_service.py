import httpx
import json
from config import OPENROUTER_API_KEY, llm1,llm2

PROMPT = """
You are a strict information extraction system.

Extract all PII (Personally Identifiable Information) EXACTLY as it appears in the text.

PII includes:
- Names
- Phone numbers
- Email addresses

STRICT RULES:
- Return ONLY valid JSON (no explanation, no text outside JSON)
- Output must be a JSON array
- Do NOT modify, split, or reformat extracted text
- Extract text EXACTLY as it appears in input
- Do NOT hallucinate or guess missing data
- If nothing found, return []

Allowed types:
- NAME
- PHONE
- EMAIL

Format:
[
  {"text": "John Doe", "type": "NAME"},
  {"text": "9876543210", "type": "PHONE"},
  {"text": "john@gmail.com", "type": "EMAIL"}
]

Text:
"""


async def detect_pii(text):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": llm2,
        "messages": [
            {"role": "user", "content": PROMPT + text}
        ],
        "temperature": 0
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)

    result = response.json()
    #print("FULL RESPONSE:", result)
    return result["choices"][0]["message"]["content"]


def parse_llm_output(output):
    try:
        return json.loads(output)
    except:
        return []