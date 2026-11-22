# Installation & Setup Guide

This guide covers installing dependencies, configuring environment variables, running the Docker stack, and launching both the Application Tier (FastAPI) and Presentation Tier (React).

---

## 1. Prerequisites

- **Python**: Version 3.10+ (Tested on Python 3.13)
- **Node.js**: Version 18+ and npm
- **Docker & Docker Compose** (Optional for Mosquitto & InfluxDB; SQLite works standalone without Docker!)
- **Operating System**: Windows 10/11, Ubuntu/Debian Linux, or macOS

---

## 2. Fast-Track Setup

### Step 1: Clone or Navigate to Project
```bash
cd MEMS-INDUSTRIAL-MONITORING
```

### Step 2: Application Tier (Backend) Setup
```bash
cd application-tier

# 1. Create Virtual Environment
python -m venv .venv

# 2. Activate Virtual Environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# 3. Install Python Dependencies
pip install -r requirements.txt

# 4. Copy Environment File
cp .env.example .env
```

### Step 3: Presentation Tier (Frontend) Setup
Open a second terminal:
```bash
cd MEMS-INDUSTRIAL-MONITORING/presentation-tier

# Install npm dependencies
npm install
```

---

## 3. Running Optional Infrastructure (Mosquitto & InfluxDB)
If Docker is installed on your machine and you want to run physical hardware MQTT with InfluxDB:
```bash
cd MEMS-INDUSTRIAL-MONITORING/infrastructure
docker-compose up -d
```
*Note: If Docker is not running, the application automatically runs in standalone mode using SQLite.*

---

## 4. Starting the Application

### 1. Launch FastAPI Backend
```bash
cd MEMS-INDUSTRIAL-MONITORING/application-tier
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- Swagger API Docs: `http://localhost:8000/docs`
- Health Endpoint: `http://localhost:8000/api/health`
- WebSocket Feed: `ws://localhost:8000/ws/sensors`

### 2. Launch React Dashboard
In your frontend terminal:
```bash
cd MEMS-INDUSTRIAL-MONITORING/presentation-tier
npm run dev
```
- Open browser: `http://localhost:5173`

---

## 5. Verification Commands

Test backend health endpoint:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/health" -Method Get
```

Inject high vibration condition:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/simulation/mode?mode=high_vibration" -Method Post
```

Return to normal condition:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/simulation/mode?mode=normal" -Method Post
```
