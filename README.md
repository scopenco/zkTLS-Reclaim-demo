# zkTLS-Reclaim MVP (Python + React Edition)

## Overview
This MVP demonstrates a flow where a user makes a bank payment, generates a zkTLS-based proof, and a verifier backend checks the proof using the Reclaim Protocol Python SDK. The frontend is a React app that interacts with the backend and triggers the Reclaim proof flow.

## Architecture
- **User**: Interacts with a React frontend to generate and submit a ZK proof.
- **Verifier (Marketplace)**: Receives and verifies the proof (FastAPI backend).
- **Stack**: zkTLS, Python, FastAPI, React, Reclaim Protocol Python SDK, Reclaim JS SDK.

## Directory Structure
```
zktls-reclaim/
├── backend/                # Python backend for verifier
│   ├── app.py              # FastAPI app with /generate-config and /receive-proofs endpoints
│   ├── requirements.txt    # Backend dependencies
│   └── ...
├── frontend/               # React frontend for user interaction
│   ├── package.json        # Frontend dependencies
│   ├── src/
│   │   └── App.jsx         # Main React app
│   └── ...
├── README.md
```

## Setup

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 3000
```
- The backend exposes:
  - `GET /generate-config` — returns a Reclaim proof request config
  - `POST /receive-proofs` — receives and verifies proofs
- CORS is enabled for all origins for local development.

### Frontend
```bash
cd frontend
npm install
npm run start
```
- The frontend runs on [http://localhost:5173](http://localhost:5173) by default (Vite).
- It fetches the config from the backend and triggers the Reclaim proof flow using the JS SDK.

## Flow
1. User opens the React frontend and clicks "Start Verification".
2. The frontend fetches the config from `/generate-config` on the backend.
3. The frontend initializes the Reclaim JS SDK and triggers the proof flow (QR code, extension, or mobile, depending on environment).
4. The user completes the proof flow.
5. The proof is sent to the backend `/receive-proofs` endpoint for verification.
6. The frontend displays the result.

## Troubleshooting
- **CORS errors:** Ensure the backend is running and CORS is enabled (see `app.py`).
- **NPM errors for @reclaimprotocol/js-sdk:** Use the latest available version or install from GitHub if not on npm.
- **404 errors:** Make sure both backend and frontend are running, and you are using the correct URLs.

## Notes
- Get your `APP_ID`, `APP_SECRET`, and `PROVIDER_ID` from the [Reclaim Developer Portal](https://dev.reclaimprotocol.org/my-applications).
- After creating of application and secret don't forget to add provider. In our case is used "Revolut Last Transaction".
- If running locally and testing with mobile, use [ngrok](https://ngrok.com/) to expose your backend to the internet and update `BASE_URL` in `app.py`.
- For more details, see the [Reclaim Protocol Fullstack Guide](https://docs.reclaimprotocol.org/web/frontend/fullstack).
