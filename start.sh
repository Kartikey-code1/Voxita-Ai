#!/bin/bash

# Voxita AI Voice Assistant - Quick Start Script (Groq Version)

echo "🚀 Starting Voxita AI Voice Assistant (Groq)..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    if [ -f .env.example ]; then
        cp .env.example .env
    else
        echo "❌ .env.example not found. Please create a .env file manually with your Groq API key:"
        echo "GROQ_API_KEY=your_api_key_here"
        exit 1
    fi
fi

# Check if GROQ_API_KEY is set
if ! grep -q "GROQ_API_KEY" .env; then
    echo "❌ GROQ_API_KEY not found in .env file."
    echo "Please add your Groq API key like this:"
    echo "GROQ_API_KEY=your_api_key_here"
    exit 1
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
cd frontend || { echo "❌ frontend directory not found"; exit 1; }

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
echo "🎉 Voxita (Groq) is now running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "💡 Tips:"
echo "   • Add your Groq API key in .env"
echo "   • Click the microphone button for voice input"
echo "   • Toggle the speaker button for voice output"
echo "   • Use Ctrl+C to stop the services"
echo ""

wait
