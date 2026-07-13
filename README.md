## PitchEngine AI 🎤

Transform your GitHub repository into a winning 2-minute pitch script.

PitchEngine AI is an automated tool designed for hackathons and developers. It analyzes your GitHub repository's structure and README content, then leverages Google's Gemini AI to generate a structured, professional, and engaging pitch presentation.

## 📂 Project Structure

We use a modular architecture to keep the backend and frontend services separated:
```
.
├── backend/            # FastAPI Backend
│   ├── main.py         # API Endpoints
│   ├── ai_service.py   # Gemini AI logic
│   ├── github_service.py # GitHub API integration
│   ├── models.py       # Data structures
│   └── requirements.txt
├── frontend/           # Streamlit Frontend
│   ├── app.py          # UI logic & High-Contrast CSS
│   └── requirements.txt
└── README.md
```


## 🛠️ Local Development Setup

### 1. Backend Setup

- Open your terminal and navigate to the backend folder:

```
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

- Create a .env file in the backend/ folder and add your Google AI API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```


- Start the server:

```
uvicorn main:app --reload
```


### 2. Frontend Setup

- Open a new terminal tab and navigate to the frontend folder:

```
cd frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Launch the app:

```
streamlit run app.py
```


## 🌐 Deployment Instructions

### Backend (Render)

- Root Directory: ```backend```
- Build Command: ```pip install -r requirements.txt```
- Start Command: ```uvicorn main:app --host 0.0.0.0 --port $PORT```

### Frontend (Streamlit Community Cloud)

- App Folder: ```frontend```
- Main File Path: ```app.py```

## 💡 How it works

1. Repository Analysis: We use PyGithub to safely fetch README content and file structures.
2. AI Synthesis: Context is sent to the Gemini 1.5-Flash model, acting as an elite Hackathon Pitch Coach.
3. Structured Response: The backend returns a structured JSON object containing your hook, wow-moment, and demo warnings.

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Streamlit](https://streamlit.io/) - Frontend dashboard
- [Google Gemini API](https://ai.google.dev/) - AI engine
- [Render](https://render.com/) - Cloud hosting
