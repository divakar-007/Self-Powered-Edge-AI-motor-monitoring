# MEMS Industrial Monitoring System - Unified Startup Script
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " MEMS Industrial Monitoring System - Three-Tier Startup  " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$root = $PSScriptRoot

# 1. Start Application Tier (FastAPI Backend)
Write-Host "[1/2] Launching Application Tier (FastAPI) on http://localhost:8000..." -ForegroundColor Green
$backendProc = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root/application-tier'; .\.venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload" -PassThru

Start-Sleep -Seconds 3

# 2. Start Presentation Tier (React + Vite)
Write-Host "[2/2] Launching Presentation Tier (React Dashboard) on http://localhost:5173..." -ForegroundColor Green
$frontendProc = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root/presentation-tier'; npm run dev" -PassThru

Write-Host "`nAll tiers started successfully!" -ForegroundColor Cyan
Write-Host "• Frontend Dashboard : http://localhost:5173" -ForegroundColor Yellow
Write-Host "• Backend API Docs   : http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "• Health Diagnostic  : http://localhost:8000/api/health" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan
