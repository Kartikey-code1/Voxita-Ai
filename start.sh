#!/bin/bash

# Voxita AI Voice Assistant - Quick Start Script

echo "🚀 Starting Voxita AI Voice Assistant..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install it from https://ollama.ai"
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "⚠️  Ollama is not running. Starting Ollama server..."
    echo "Please run 'ollama serve' in another terminal, then run this script again."
    exit 1
fi

# Check if Mistral model is available
if ! ollama list | grep -q "mistral"; then
    echo "📥 Mistral model not found. Pulling model..."
    ollama pull mistral
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
fi

# Start backend with Docker Compose
echo "🐳 Starting backend services..."
docker-compose up -d

# Wait for backend to be ready
echo "⏳ Waiting for backend to start..."
sleep 10

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ from https://nodejs.org"
    exit 1
fi

# Start frontend
echo "🎨 Starting frontend..."
cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Start development server
echo "✨ Starting Voxita frontend..."
npm run dev &

# Wait a moment for servers to start
sleep 5

echo ""
echo "🎉 Voxita is now running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "💡 Tips:"
echo "   • Click the microphone button for voice input"
echo "   • Toggle the speaker button for voice output"
echo "   • Use Ctrl+C to stop the services"
echo ""

# Keep script running
wait