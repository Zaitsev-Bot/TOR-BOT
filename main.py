import json
import requests
from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class TORRequest(BaseModel):
    project_title: str
    objectives: str
    scope: str
    qualifications: str

# Hugging Face API Key (Securely Loaded from Environment Variable)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY is not set. Please configure it as an environment variable.")

@app.get("/")
def read_root():
    return {"message": "Welcome to the TOR-BOT API"}

@app.post("/generate-tor/")
async def generate_tor(request: TORRequest):
    prompt = f"""
    Generate a professional Terms of Reference (TOR) document.
    - Project Title: {request.project_title}
    - Objectives: {request.objectives}
    - Scope: {request.scope}
    - Required Qualifications: {request.qualifications}
    Ensure it follows a structured TOR format.
    """

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct",
        headers=headers,
        json={"inputs": prompt, "parameters": {"max_new_tokens": 500}}
    )

    generated_text = response.json().get("generated_text", "Error generating TOR")

    return {"message": "TOR generated successfully!", "text": generated_text}