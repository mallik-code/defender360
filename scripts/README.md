# Development Scripts

Simple scripts for development environment management.

## Setup Scripts

**Linux/macOS:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

**Windows:**
```powershell
.\scripts\setup.ps1
```

## Sample Data

Generate test security events:
```bash
pip install kafka-python  # if not already installed
python scripts/sample-data.py
```

## Cleanup

Reset development environment:
```bash
# Linux/macOS
./scripts/cleanup.sh

# Windows  
docker-compose down
docker system prune -f
```

That's it - keep it simple!