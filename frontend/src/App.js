
import React, { useState, useEffect, useRef } from 'react';
import './App.css';

// Author: Sayed Allam
function App() {
    const [personality, setPersonality] = useState({
        warmth: 0.5,
        wit: 0.5,
        humor: 0.5,
        empathy: 0.5,
        conscientiousness: 0.5,
        openness: 0.5,
        agreeableness: 0.5,
        neuroticism: 0.5,
        extroversion: 0.5,
    });
    const [voices, setVoices] = useState([]);
    const [selectedVoice, setSelectedVoice] = useState('1');
    const [socket, setSocket] = useState(null);
    const [isRecording, setIsRecording] = useState(false);
    const mediaRecorder = useRef(null);
    const [transcript, setTranscript] = useState("");
    const [responseText, setResponseText] = useState("");
    const [audioUrl, setAudioUrl] = useState("");
    const [status, setStatus] = useState("Ready");
    const [error, setError] = useState("");

    useEffect(() => {
        // Fetch voices from the backend
        fetch('http://localhost:8000/api/voices')
            .then(response => response.json())
            .then(data => setVoices(data))
            .catch(err => setError("Failed to fetch voices."));

        // Establish WebSocket connection
        const ws = new WebSocket('ws://localhost:8000/ws');
        setSocket(ws);

        ws.onopen = () => setStatus("Ready");
        ws.onclose = () => setStatus("Disconnected");
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.transcript) {
                setTranscript(data.transcript);
                setStatus("Processing...");
                // Send transcript to conversation endpoint
                fetch('http://localhost:8000/api/conversation', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: data.transcript, personality }),
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    setResponseText(data.response_text);
                    setAudioUrl(`http://localhost:8000${data.audio_url}`);
                    setStatus("Ready");
                })
                .catch(err => {
                    setError("Failed to get response from AI.");
                    setStatus("Ready");
                });
            } else if (data.error) {
                setError(data.error);
                setStatus("Ready");
            }
        };

        return () => {
            if (ws) {
                ws.close();
            }
        };
    }, [personality]);

    const handlePersonalityChange = (trait, value) => {
        setPersonality(prev => ({ ...prev, [trait]: parseFloat(value) }));
    };

    const handleVoiceChange = (event) => {
        setSelectedVoice(event.target.value);
    };

    const toggleRecording = () => {
        if (isRecording) {
            mediaRecorder.current.stop();
            setIsRecording(false);
            setStatus("Processing...");
        } else {
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(stream => {
                    mediaRecorder.current = new MediaRecorder(stream);
                    mediaRecorder.current.ondataavailable = (event) => {
                        if (socket && socket.readyState === WebSocket.OPEN) {
                            socket.send(event.data);
                        }
                    };
                    mediaRecorder.current.start(1000); // Send data every second
                    setIsRecording(true);
                    setStatus("Recording...");
                    setError("");
                })
                .catch(err => {
                    setError("Could not start recording. Please check your microphone permissions.");
                });
        }
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Umemiya AI Agent</h1>
                <p>Author: Sayed Allam</p>
            </header>
            <main>
                <div className="status">{status}</div>
                {error && <div className="error">{error}</div>}
                <div className="personality-controls">
                    <h2>Personality Traits</h2>
                    {Object.keys(personality).map(trait => (
                        <div key={trait}>
                            <label>{trait}</label>
                            <input
                                type="range"
                                min="0"
                                max="1"
                                step="0.1"
                                value={personality[trait]}
                                onChange={(e) => handlePersonalityChange(trait, e.target.value)}
                            />
                        </div>
                    ))}
                </div>
                <div className="voice-controls">
                    <h2>Voice Selection</h2>
                    <select onChange={handleVoiceChange} value={selectedVoice}>
                        {Object.entries(voices).map(([id, name]) => (
                            <option key={id} value={id}>{name}</option>
                        ))}
                    </select>
                </div>
                <div className="conversation-controls">
                    <button onClick={toggleRecording} disabled={status === "Processing..." || status === "Recording..."}>
                        {isRecording ? 'Stop Recording' : 'Start Recording'}
                    </button>
                    <p>Transcript: {transcript}</p>
                    <p>AI Response: {responseText}</p>
                    {audioUrl && <audio controls src={audioUrl} />}
                </div>
            </main>
        </div>
    );
}

export default App;
