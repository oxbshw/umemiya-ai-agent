
# Deployment Guide

**Author:** Sayed Allam

### Docker Deployment

1.  **Prerequisites**: Docker and Docker Compose installed.
2.  **Clone the repository** and navigate to the project directory.
3.  **Run `docker-compose up -d`** to build and start the containers.
4.  The application will be available at `http://localhost:3000`.

### Manual Deployment

#### Backend

1.  Navigate to the `backend` directory.
2.  Install dependencies: `pip install -r requirements.txt`
3.  Run the server: `uvicorn main:app --host 0.0.0.0 --port 8000`

#### Frontend

1.  Navigate to the `frontend` directory.
2.  Install dependencies: `npm install`
3.  Start the development server: `npm start`
