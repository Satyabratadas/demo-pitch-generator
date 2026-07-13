from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import uvicorn

from backend.github_service import fetch_repository_context
from backend.ai_service import generate_demo_pitch
from backend.models import DemoPitch

app = FastAPI(
    title="Hackathon Demo Pitch Generator API",
    description="An AI-powered agentic workflow that generates 2-minute pitch scripts from GitHub repos.",
    version="1.0.0"
)

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows access from any origin (fine for a demo project)
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

class PitchRequest(BaseModel):
    repo_url: str

@app.get("/")
def read_root():
    """Simple health check endpoint."""
    return {"status": "online", "message": "The Pitch Generator API is running smoothly!"}

@app.post("/generate-pitch", response_model=DemoPitch)
def create_pitch(request: PitchRequest):
    """
    Main endpoint: Takes a GitHub URL, extracts repo data, 
    and returns a structured pitch script via Gemini.
    """
    url = str(request.repo_url).strip()
    
    if not url:
        raise HTTPException(status_code=400, detail="Repository URL cannot be empty.")
    
    try:
        print(f"Received request for URL: {url}")
        
        # Step 1: Run the GitHub service to download README and file structures
        print("Fetching data from GitHub...")
        repo_context = fetch_repository_context(url)
        
        # Step 2: Run the AI service to parse the context and generate the script
        print("Invoking Gemini AI to write the pitch...")
        pitch_output = generate_demo_pitch(repo_context)
        
        print("Pitch successfully generated!")
        return pitch_output

    except ValueError as ve:
        # Handles bad URL formatting errors raised by our parser
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        # Handles API connection failures from GitHub or Gemini
        raise HTTPException(status_code=502, detail=str(re))
    except Exception as e:
        # Catch-all for any unexpected failures
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Allows you to start the server directly by running `python main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)