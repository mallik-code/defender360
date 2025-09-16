# Development Setup

Simple setup for developers.

## Prerequisites

Install these on your machine:
- Docker & Docker Compose
- Python 3.12+
- Java 21+ 
- Node.js 18+
- Git

## Setup

1. **Start infrastructure**:
   ```bash
   docker-compose up -d
   ```

2. **Install dependencies**:
   ```bash
   # Python agents
   cd agents && pip install -r requirements.txt

   # Java services  
   cd services && mvn install

   # Frontend
   cd frontend && npm install
   ```

## Development URLs

- Kafka UI: http://localhost:8081
- Kibana: http://localhost:5601
- Frontend: http://localhost:3000 (when running)

## Project Structure

```
agents/          # Python FastAPI agents
services/        # Java Spring Boot services
frontend/        # React TypeScript frontend
```

That's it! Keep it simple.