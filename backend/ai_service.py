import os
from google import genai
from dotenv import load_dotenv
from models import DemoPitch

# Load environment variables from .env
load_dotenv()

# Initialize the Gemini SDK client
client = genai.Client()

def generate_demo_pitch(repo_context: str) -> DemoPitch:
    """
    Sends the extracted GitHub repository data to Gemini 
    using the verified gemini-3.5-flash model.
    """
    
    # The System Instruction sets the persona and rules for the AI
    system_instruction = """
    You are an elite Developer Advocate and Hackathon Pitch Coach. 
    Your job is to transform raw repository data (README and file structures) into a winning 2-minute live demo script.
    
    CRITICAL RULES FOR THE PITCH:
    1. The presentation must take exactly 2 minutes when spoken at a normal pace.
    2. Focus on WHAT the project does, WHY it matters, and HOW it works technically.
    3. The 'timeline' must cover a complete 120-second breakdown.
    4. Highlight a 'wow_moment'—this should be the most technically impressive or visually striking feature.
    5. Provide 'demo_warnings' specifically targeting hackathon dangers (e.g., avoiding authentication delays, local database crashes, or exposing API keys).
    """

    try:
        # Calling the exact model found in your system scan
        response = client.models.generate_content(
            model='models/gemini-3.5-flash',
            contents=f"Analyze this repository and generate a hackathon demo pitch script:\n\n{repo_context}",
            config={
                'system_instruction': system_instruction,
                'response_mime_type': 'application/json',
                'response_schema': DemoPitch,
                'temperature': 0.7,
            }
        )
        
        # The SDK automatically converts the JSON string from Gemini into our Pydantic Object
        return response.parsed

    except Exception as e:
        raise RuntimeError(f"Gemini AI generation failed: {str(e)}")

if __name__ == "__main__":
    print("Testing AI Service...")
    
    # Mock data to simulate what github_service.py will send
    mock_context = """
    REPOSITORY: test-user/quick-share
    =========================================
    TOP-LEVEL FILE STRUCTURE:
    📁 src/
    📄 package.json
    📄 README.md
    =========================================
    README CONTENT:
    # QuickShare
    An end-to-end encrypted file sharing application built in 36 hours for a hackathon.
    Uses WebRTC for peer-to-peer fast transfers without storing files on a server.
    Built with React, Node.js, and Tailwind CSS.
    """
    
    try:
        pitch = generate_demo_pitch(mock_context)
        print("\n--- AI GENERATION SUCCESS ---")
        print(f"Project Name: {pitch.project_name}")
    except Exception as e:
        print(f"Error during AI test: {e}")