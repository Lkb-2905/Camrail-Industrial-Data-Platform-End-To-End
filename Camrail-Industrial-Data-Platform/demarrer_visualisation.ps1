# Script de demarrage - Visualisation Streamlit + Grafana + Prometheus
# Tout tourne dans Docker SAUF Streamlit (sur la machine)

$projectDir = "C:\Users\pc\Desktop\projet CAMRAIL\Camrail-Industrial-Data-Platform"
$pythonExe = "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CAMRAIL - Demarrage Visualisation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Docker Compose (API, Grafana, Prometheus, Kafka, Postgres)
Write-Host "[1/2] Demarrage Docker (API + Grafana + Prometheus + Kafka + Postgres)..." -ForegroundColor Yellow
Set-Location $projectDir
docker-compose up -d --build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erreur Docker. Verifiez que Docker Desktop est demarre." -ForegroundColor Red
    exit 1
}
Write-Host "      Attente que l'API soit prete (15 sec)..." -ForegroundColor Gray
Start-Sleep -Seconds 15

# 2. Streamlit
Write-Host "[2/2] Demarrage Streamlit (nouvelle fenetre)..." -ForegroundColor Yellow
$streamlitCmd = "Set-Location '$projectDir'; Write-Host 'Streamlit demarre!' -ForegroundColor Green; & '$pythonExe' -m streamlit run dashboard/app.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $streamlitCmd

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  TOUT EST PRET !" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Ouvrez ces 3 onglets :" -ForegroundColor White
Write-Host "  1. STREAMLIT : " -NoNewline; Write-Host "http://localhost:8501" -ForegroundColor Cyan
Write-Host "  2. GRAFANA  : " -NoNewline; Write-Host "http://localhost:3000" -ForegroundColor Cyan
Write-Host "  3. PROMETHEUS : " -NoNewline; Write-Host "http://localhost:9090" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pour remplir Grafana : faites 5-10 predictions sur Streamlit !" -ForegroundColor Yellow
Write-Host "Grafana : admin / camrail_admin_2026" -ForegroundColor Gray
Write-Host ""
