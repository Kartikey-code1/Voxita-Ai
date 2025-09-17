# Voxita - AI Voice Assistant

A futuristic AI voice assistant with streaming chat capabilities powered by Ollama and featuring a stunning neon-blue UI design.

## Features

- 🎤 **Voice Input**: Web Speech Recognition API for hands-free interaction
- 🔊 **Voice Output**: Text-to-Speech synthesis for AI responses
- 💬 **Streaming Chat**: Real-time streaming responses via Server-Sent Events
- 🤖 **Ollama Integration**: Compatible with Mistral and other Ollama models
- 🎨 **Futuristic UI**: Neon blue cyberpunk-style interface with animations
- 🐳 **Docker Ready**: Easy deployment with Docker Compose

## Quick Start

### Prerequisites

1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai)
2. **Pull Mistral Model**:
   ```bash
   ollama pull mistral
   ```
3. **Node.js 18+** and **Python 3.11+**

### Option 1: Using Docker (Recommended)

1. **Clone and setup**:
   ```bash
   git clone <your-repo>
   cd ai-voxita-voice
   cp .env.example .env
   ```

2. **Start Ollama** (in separate terminal):
   ```bash
   ollama serve
   ```

3. **Run the project**:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

4. **Access the app**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your Ollama URL (default: http://localhost:11434)
   ```

5. **Start backend**:
   ```bash
   python main.py
   ```

#### Frontend Setup

1. **Navigate to frontend** (new terminal):
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

## API Endpoints

### Backend API (Port 8000)

- `GET /` - Health check
- `POST /api/chat` - Non-streaming chat
- `GET /api/stream-chat` - Streaming chat via SSE
- `GET /api/health` - System health status

### Example API Usage

**Non-streaming chat**:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

**Streaming chat**:
```bash
curl -N http://localhost:8000/api/stream-chat?message=Hello
```

## Configuration

### Environment Variables

Create `.env` file in the root directory:

```env
# Ollama Configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# API Configuration
API_KEY=your_api_key_here
DEBUG=true

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

### Ollama Models

Supported models (install with `ollama pull <model>`):
- `mistral` (default)
- `llama2`
- `codellama`
- `vicuna`
- `orca-mini`

## Voice Features

### Voice Input
- Click the microphone button or use keyboard shortcut
- Supports continuous speech recognition
- Automatically sends message when speech ends

### Voice Output
- Toggle voice output with the speaker button
- Adjustable speech rate, pitch, and volume
- Supports multiple voice engines (browser dependent)

## UI Features

- **Responsive Design**: Works on desktop and mobile
- **Dark Theme**: Cyberpunk-inspired neon blue design
- **Animations**: Smooth transitions and hover effects
- **Real-time Streaming**: Live message updates
- **Voice Indicators**: Visual feedback for voice states

## Development

### Project Structure

```
ai-voxita-voice/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main server application
│   ├── ollama_client.py    # Ollama API client
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Backend container
│   └── .env.example        # Environment template
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx         # Main application
│   │   ├── components/     # React components
│   │   └── styles.css      # Tailwind styles
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
├── docker-compose.yml      # Container orchestration
├── start.sh               # Quick start script
└── README.md              # This file
```

### Building for Production

**Frontend**:
```bash
cd frontend
npm run build
```

**Backend Docker**:
```bash
cd backend
docker build -t voxita-backend .
```

## Troubleshooting

### Common Issues

1. **Ollama Connection Failed**:
   - Ensure Ollama is running: `ollama serve`
   - Check OLLAMA_URL in .env file
   - Verify model is installed: `ollama list`

2. **Voice Input Not Working**:
   - Use HTTPS or localhost (required for Web Speech API)
   - Check browser permissions for microphone
   - Supported browsers: Chrome, Edge, Safari

3. **CORS Errors**:
   - Backend includes CORS middleware
   - Check frontend proxy configuration in vite.config.js

4. **Port Conflicts**:
   - Frontend: Change port in vite.config.js
   - Backend: Set PORT in .env file

### Performance Tips

- Use streaming endpoints for better responsiveness
- Adjust Ollama model parameters in ollama_client.py
- Enable browser hardware acceleration for smooth animations

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- [Ollama](https://ollama.ai) - Local AI model runtime
- [FastAPI](https://fastapi.tiangolo.com) - Modern Python web framework
- [React](https://reactjs.org) - Frontend framework
- [Tailwind CSS](https://tailwindcss.com) - Utility-first CSS
- [Framer Motion](https://framer.com/motion) - Animation library