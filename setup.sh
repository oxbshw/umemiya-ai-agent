#!/bin/bash

# Umemiya AI Agent - Setup Script
# Author: Sayed Allam
# Repository: https://github.com/oxbshw/umemiya-ai-agent

set -e

echo "🚀 Setting up Umemiya AI Agent..."
echo "👨‍💻 Author: Sayed Allam"
echo "📁 Repository: https://github.com/oxbshw/umemiya-ai-agent"
echo ""

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if Python and Node.js are available for local development
echo "🔍 Checking development dependencies..."

if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found: $(python3 --version)"
else
    echo "⚠️  Python 3 not found (needed for local development)"
fi

if command -v node &> /dev/null; then
    echo "✅ Node.js found: $(node --version)"
else
    echo "⚠️  Node.js not found (needed for local development)"
fi

if command -v npm &> /dev/null; then
    echo "✅ npm found: $(npm --version)"
else
    echo "⚠️  npm not found (needed for local development)"
fi

echo ""

# Ask user for setup preference
echo "🛠️  Setup Options:"
echo "1. Docker setup (Recommended - requires Docker)"
echo "2. Local development setup (requires Python 3.9+ and Node.js 16+)"
echo "3. Both setups"

read -p "Choose setup option (1-3): " setup_choice

case $setup_choice in
    1|3)
        echo ""
        echo "🐳 Setting up Docker environment..."
        
        # Build and start Docker containers
        echo "📦 Building Docker images..."
        docker-compose build

        echo "🏃‍♂️ Starting services..."
        docker-compose up -d

        echo "⏳ Waiting for services to be ready..."
        sleep 10

        # Check if services are running
        if docker-compose ps | grep -q "Up"; then
            echo "✅ Docker services are running!"
            echo ""
            echo "🌐 Access the application:"
            echo "   • Main Application: http://localhost:3000"
            echo "   • Testing Platform: http://localhost:3001"
            echo "   • Backend API: http://localhost:8000"
            echo "   • API Documentation: http://localhost:8000/docs"
        else
            echo "❌ Some services failed to start. Check logs with: docker-compose logs"
        fi
        ;;&
    2|3)
        echo ""
        echo "💻 Setting up local development environment..."
        
        # Backend setup
        echo "🔧 Setting up backend..."
        cd backend
        
        if command -v python3 &> /dev/null; then
            echo "📦 Installing Python dependencies..."
            pip3 install -r requirements.txt
            echo "✅ Backend dependencies installed"
        else
            echo "❌ Python 3 not available. Skipping backend setup."
        fi
        
        cd ..
        
        # Frontend setup
        echo "🔧 Setting up frontend..."
        cd frontend
        
        if command -v npm &> /dev/null; then
            echo "📦 Installing Node.js dependencies..."
            npm install
            echo "✅ Frontend dependencies installed"
        else
            echo "❌ npm not available. Skipping frontend setup."
        fi
        
        cd ..
        
        echo ""
        echo "🚀 To start local development:"
        echo "   Backend: cd backend && python main.py"
        echo "   Frontend: cd frontend && npm start"
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "🎉 Setup completed!"
echo ""
echo "📚 Next steps:"
echo "   • Read the README.md for detailed usage instructions"
echo "   • Check the API documentation at /docs endpoint"
echo "   • Review the testing guide in the documentation"
echo ""
echo "💡 For troubleshooting:"
echo "   • Check Docker logs: docker-compose logs"
echo "   • View service status: docker-compose ps"
echo "   • Restart services: docker-compose restart"
echo ""
echo "👨‍💻 Created by: Sayed Allam"
echo "🔗 Repository: https://github.com/oxbshw/umemiya-ai-agent"
