@echo off
title MEMS Industrial Monitoring System
echo ==========================================================
echo  MEMS Industrial Monitoring System - Three-Tier Startup
echo ==========================================================

echo [1/2] Launching Application Tier (FastAPI Backend)...
start "MEMS Backend (FastAPI)" cmd /k "cd application-tier && .venv\Scripts\activate && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak > nul

echo [2/2] Launching Presentation Tier (React Frontend)...
start "MEMS Frontend (React Dashboard)" cmd /k "cd presentation-tier && npm run dev"

echo.
echo All tiers launched in separate windows!
echo - Presentation Dashboard: http://localhost:5173
echo - Swagger API Docs:      http://localhost:8000/docs
echo ==========================================================
pause
