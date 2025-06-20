
![Umemiya AI](https://raw.githubusercontent.com/oxbshw/umemiya-ai-agent/main/docs/images/banner.png)

# Umemiya AI Agent

[![Build Status](https://img.shields.io/travis/com/oxbshw/umemiya-ai-agent.svg)](https://travis-ci.com/oxbshw/umemiya-ai-agent)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Author:** Sayed Allam

Umemiya AI is a sophisticated conversational AI system with a React-based frontend and a FastAPI backend. This project provides a complete implementation of the Umemiya AI Agent, including real-time audio streaming, a 9-trait personality system, and text-to-speech capabilities.

### Key Features

- **FastAPI Backend**: A robust backend with API endpoints for health checks, status, voice selection, and conversation handling.
- **React Frontend**: A user-friendly interface for interacting with the AI agent.
- **Real-time Audio Streaming**: WebSocket communication for real-time audio streaming between the frontend and backend.
- **9-Trait Personality System**: A personality system that allows users to customize the AI's personality.
- **Text-to-Speech**: Multiple voice options for the AI's responses.
- **Dockerized Deployment**: A complete Docker setup for easy deployment.

### Tech Stack

- **Backend**: FastAPI, Python, Uvicorn, WebSockets
- **Frontend**: React, JavaScript, WebSockets
- **Deployment**: Docker, Nginx

### Getting Started

#### Prerequisites

- Docker and Docker Compose

#### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/oxbshw/umemiya-ai-agent.git
   cd umemiya-ai-agent
   ```

2. **Run the application using Docker Compose:**
   ```sh
   docker-compose up -d
   ```

3. **Access the application:**
   - **Frontend**: [http://localhost:3000](http://localhost:3000)
   - **Backend API**: [http://localhost:8000/docs](http://localhost:8000/docs)
