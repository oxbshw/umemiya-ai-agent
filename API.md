
# API Documentation

**Author:** Sayed Allam

### Base URL

`http://localhost:8000`

### Endpoints

#### `GET /api/health`

- **Description**: Health check endpoint to verify that the server is running.
- **Response**: `200 OK`
  ```json
  {
    "status": "ok"
  }
  ```

#### `GET /api/status`

- **Description**: Endpoint to get the current status of the AI agent.
- **Response**: `200 OK`
  ```json
  {
    "status": "running",
    "personality_traits": 9
  }
  ```

#### `GET /api/voices`

- **Description**: Endpoint to retrieve the available voices for text-to-speech.
- **Response**: `200 OK`
  ```json
  {
    "1": "Female Voice 1",
    "2": "Male Voice 1",
    "3": "Female Voice 2"
  }
  ```

#### `POST /api/conversation`

- **Description**: Endpoint to handle conversation with the AI agent.
- **Request Body**:
  ```json
  {
    "text": "Hello, how are you?",
    "personality": {
      "warmth": 0.8,
      "wit": 0.5,
      "humor": 0.6,
      "empathy": 0.9,
      "conscientiousness": 0.7,
      "openness": 0.6,
      "agreeableness": 0.8,
      "neuroticism": 0.2,
      "extroversion": 0.7
    }
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "response_text": "I am doing well, thank you for asking!",
    "audio_url": "/audio/response.wav"
  }
  ```

#### `POST /api/synthesize`

- **Description**: Endpoint for text-to-speech synthesis.
- **Request Body**:
  ```json
  {
    "text": "Hello, world!",
    "voice_id": "1"
  }
  ```
- **Response**: `200 OK`
  - Returns the synthesized audio file.

#### `WS /ws`

- **Description**: WebSocket endpoint for real-time audio streaming.
- **Client to Server**: Send audio bytes.
- **Server to Client**: Send JSON with transcript.
  ```json
  {
    "transcript": "This is a simulated transcript."
  }
  ```
