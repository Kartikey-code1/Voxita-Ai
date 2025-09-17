Voxita - AI Voice Assistant (Groq Version)

A futuristic AI voice assistant with streaming chat capabilities powered by Groq API and featuring a stunning neon-blue UI design.

Features

🎤 Voice Input: Web Speech Recognition API for hands-free interaction

🔊 Voice Output: Text-to-Speech synthesis for AI responses

💬 Streaming Chat: Real-time streaming responses via Server-Sent Events

⚡ Groq Integration: Ultra-fast responses using Groq-hosted models

🎨 Futuristic UI: Neon blue-style 

🐳 Docker Ready: Easy deployment with Docker Compose

Quick Start
Prerequisites

Groq API Key – Get it from console.groq.com

Node.js 18+ and Python 3.11+

Docker & Docker Compose (for containerized backend)

Option 1: Using Docker (Recommended)

Clone and setup:

git clone <your-repo>
cd ai-voxita-voice
cp .env.example .env


Add Groq API key to .env:

GROQ_API_KEY=your_api_key_here


Run the project:

chmod +x start.sh
./start.sh


Access the app:

Frontend: http://localhost:3000

Backend API: http://localhost:8000

Option 2: Manual Setup
Backend Setup

Navigate to backend:

cd backend


Create virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Configure environment:

cp .env.example .env
# Edit .env with your Groq API key
GROQ_API_KEY=your_api_key_here


Start backend:

python main.py

Frontend Setup

Navigate to frontend (new terminal):

cd frontend


Install dependencies:

npm install


Start development server:

npm run dev

API Endpoints (Port 8000)

GET / - Health check

POST /api/chat - Non-streaming chat (Groq)

GET /api/stream-chat - Streaming chat via SSE (Groq)

GET /api/health - System health status

Example API Usage

Non-streaming chat:

curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'


Streaming chat:

curl -N http://localhost:8000/api/stream-chat?message=Hello

Configuration
Environment Variables

Create .env file in the root directory:

# Groq Configuration
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama3-8b-8192   # or mistral-7b, mixtral-8x7b, llama3-70b

# API Configuration
DEBUG=true

# Server Configuration
HOST=0.0.0.0
PORT=8000

Voice Features

Voice Input: Web Speech API for hands-free interaction

Voice Output: Adjustable TTS (rate, pitch, volume)

Multi-voice support (browser dependent)

UI Features

Responsive Design (desktop + mobile)

Dark Theme (cyberpunk neon blue)

Animations (Framer Motion)

Streaming UI (real-time Groq responses)

Voice Indicators

Development
Project Structure
ai-voxita-voice/
├── backend/                 # FastAPI backend
│   ├── main.py              # Main server application
│   ├── groq_client.py       # Groq API client
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Backend container
│   └── .env.example         # Environment template
├── frontend/                # React frontend
│   ├── src/
│   │   ├── App.jsx          # Main application
│   │   ├── components/      # React components
│   │   └── styles.css       # Tailwind styles
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
├── docker-compose.yml       # Container orchestration
├── start.sh                 # Quick start script (Groq)
└── README.md                # This file

Troubleshooting

Groq Authentication Failed

Ensure GROQ_API_KEY is set correctly in .env

Voice Input Not Working

Use HTTPS or localhost (Web Speech API requirement)

Allow microphone permissions

CORS Errors

Backend has CORS middleware

Check frontend proxy config

Port Conflicts

Frontend default: 3000

Backend default: 8000

Performance Tips

Use streaming endpoints for real-time Groq responses

Choose smaller models (llama3-8b) for faster replies

Use larger models (llama3-70b) for complex reasoning
