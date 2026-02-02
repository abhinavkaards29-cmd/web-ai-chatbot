from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import requests, json

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    history: list = []

def stream_ai(prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )

    for line in r.iter_lines():
        if line:
            data = json.loads(line)
            yield data.get("response", "")

@app.post("/chat")
def chat(req: ChatRequest):
    prompt = ""
    for h in req.history:
        prompt += f"User: {h['user']}\nAssistant: {h['bot']}\n"
    prompt += f"User: {req.message}\nAssistant:"

    return StreamingResponse(stream_ai(prompt), media_type="text/plain")
