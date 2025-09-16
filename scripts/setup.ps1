# Simple setup script for Agentic SOC Framework (Windows)

Write-Host "Setting up Agentic SOC Framework..." -ForegroundColor Green

# Run the comprehensive setup script
Write-Host "Running development environment setup..." -ForegroundColor Yellow
python scripts/setup-dev-environment.py

# Start Docker containers
Write-Host "Starting Docker containers..." -ForegroundColor Yellow
docker-compose up -d

# Wait for services to be ready
Write-Host "Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "=== WEB UI ACCESS POINTS ===" -ForegroundColor Cyan
Write-Host "- Kafka UI: http://localhost:8081" -ForegroundColor White
Write-Host "- Kibana: http://localhost:5602" -ForegroundColor White
Write-Host "- Redis Commander: http://localhost:8082" -ForegroundColor White
Write-Host "- pgAdmin: http://localhost:8083" -ForegroundColor White
Write-Host "  Login: admin@example.com / admin123" -ForegroundColor Gray
Write-Host ""
Write-Host "=== SERVICE PORTS ===" -ForegroundColor Cyan
Write-Host "- Kafka: localhost:9093" -ForegroundColor White
Write-Host "- Elasticsearch: localhost:9201" -ForegroundColor White
Write-Host "- Redis: localhost:6379" -ForegroundColor White
Write-Host "- PostgreSQL: localhost:5432" -ForegroundColor White
Write-Host "  DB: agentic_soc / User: soc_user / Pass: dev_password_123" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 Full connection details: docs/development/connection-details.md" -ForegroundColor Yellow