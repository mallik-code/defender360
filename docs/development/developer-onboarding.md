# Developer Onboarding Guide

## Welcome to the Agentic SOC Framework

This guide will help you get up and running with the Agentic SOC Framework development environment. The framework is a distributed, AI-powered cybersecurity platform that uses multiple specialized agents to automate threat detection, analysis, and response.

## Quick Start (5 Minutes)

### Prerequisites Check
1. Ensure your system meets the [system requirements](system-requirements.md)
2. Follow the platform-specific installation guide:
   - [Windows Setup](installation-guides/windows-setup.md)
   - [macOS Setup](installation-guides/macos-setup.md)
   - [Linux Setup](installation-guides/linux-setup.md)

### Environment Setup
```bash
# 1. Clone the repository
git clone <repository-url>
cd agentic-soc-framework

# 2. Validate your system
make validate
# or: python scripts/validate-dependencies.py

# 3. Set up the development environment
make setup
# or: python scripts/setup-dev-environment.py

# 4. Start the development environment
make start

# 5. Verify everything is running
make health
```

### Access Development Tools
Once started, you can access:
- **Kafka UI**: http://localhost:8081 (Message queue management)
- **Kibana**: http://localhost:5601 (Elasticsearch data visualization)
- **Redis Commander**: http://localhost:8082 (Redis cache management)
- **pgAdmin**: http://localhost:8083 (PostgreSQL database management)

## Project Structure

```
agentic-soc-framework/
├── agents/                     # AI Agent implementations
│   ├── orchestrator/          # Central coordination agent
│   ├── anomaly-detection/     # ML-based anomaly detection
│   ├── threat-intelligence/   # Threat intel correlation
│   ├── alert-prioritization/  # Risk scoring and prioritization
│   ├── response-automation/   # Automated response actions
│   ├── forensics/            # Deep-dive incident analysis
│   ├── learning/             # Continuous improvement
│   └── human-collaboration/   # Human-AI interaction
├── services/                  # Infrastructure services
│   ├── log-ingestion/        # High-performance log processing (Java)
│   └── shared-libs/          # Shared libraries
│       ├── python/           # Python shared components
│       └── java/             # Java shared components
├── infrastructure/           # Deployment and infrastructure
│   ├── docker/              # Docker configurations
│   ├── kubernetes/          # K8s manifests
│   └── terraform/           # Infrastructure as Code
├── docs/                    # Documentation
│   ├── api/                 # API documentation
│   ├── development/         # Development guides
│   └── deployment/          # Deployment guides
├── tests/                   # Test suites
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── e2e/                # End-to-end tests
├── data/                   # Data and configurations
│   ├── test-data/          # Sample data for testing
│   ├── models/             # ML models
│   └── sql/                # Database schemas
├── config/                 # Configuration files
│   ├── development/        # Development configs
│   └── production/         # Production configs
└── scripts/                # Utility scripts
    ├── deployment/         # Deployment scripts
    └── testing/            # Testing utilities
```

## Development Workflow

### 1. Feature Development Process

#### Starting a New Feature
```bash
# 1. Create a feature branch
git checkout -b feature/your-feature-name

# 2. Ensure environment is clean and up-to-date
make clean
git pull origin main
make setup
make start

# 3. Run tests to ensure baseline
make test
```

#### Development Cycle
```bash
# 1. Make your changes
# 2. Run relevant tests
make test-unit          # Fast unit tests
make test-integration   # Integration tests
make test-e2e          # Full end-to-end tests

# 3. Check code quality
make lint              # Check code style
make format            # Auto-format code
make type-check        # Type checking

# 4. Commit your changes
git add .
git commit -m "feat: add new feature description"

# 5. Push and create PR
git push origin feature/your-feature-name
```

### 2. Working with Agents

#### Python Agent Development
```bash
# Navigate to agent directory
cd agents/your-agent-name

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run agent locally
python main.py

# Run agent tests
pytest tests/ -v

# Debug agent
python -m debugpy --listen 5678 --wait-for-client main.py
```

#### Java Service Development
```bash
# Navigate to service directory
cd services/your-service-name

# Build and test
mvn clean compile
mvn test

# Run service locally
mvn spring-boot:run

# Debug service
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"
```

### 3. Testing Strategy

#### Test Types and When to Use Them

**Unit Tests** - Fast, isolated tests
```bash
# Run specific unit tests
pytest tests/unit/agents/test_orchestrator.py -v
pytest tests/unit/services/test_log_ingestion.py -v

# Run with coverage
pytest tests/unit/ --cov=src/ --cov-report=html
```

**Integration Tests** - Test component interactions
```bash
# Start test infrastructure
docker-compose -f docker-compose.test.yml up -d

# Run integration tests
pytest tests/integration/ -v

# Cleanup
docker-compose -f docker-compose.test.yml down
```

**End-to-End Tests** - Full system tests
```bash
# Run complete E2E test suite
make test-e2e

# Run specific E2E scenarios
pytest tests/e2e/test_threat_detection_workflow.py -v
```

### 4. Debugging and Troubleshooting

#### Common Development Issues

**Docker Issues**
```bash
# Check Docker status
docker system info

# View container logs
docker-compose logs service-name

# Restart specific service
docker-compose restart service-name

# Clean up Docker resources
make clean
```

**Database Issues**
```bash
# Connect to PostgreSQL
make shell-postgres

# Reset database
docker-compose down -v
docker-compose up -d postgresql
```

**Kafka Issues**
```bash
# Check Kafka topics
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --list

# Monitor Kafka messages
make shell-kafka

# Reset Kafka
docker-compose restart kafka
```

#### Debugging Techniques

**Python Agent Debugging**
```python
# Add to your Python code
import debugpy
debugpy.listen(5678)
debugpy.wait_for_client()  # Pauses execution
```

**Java Service Debugging**
```bash
# Start with debug port
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"
```

**Log Analysis**
```bash
# Follow all logs
make logs-f

# Filter specific service logs
docker-compose logs -f service-name

# Search logs
docker-compose logs | grep "ERROR"
```

### 5. Code Quality Standards

#### Python Code Standards
- **Formatting**: Black with 88-character line length
- **Import Sorting**: isort with specific grouping
- **Type Hints**: Mandatory for all functions
- **Docstrings**: Google-style for all public functions
- **Testing**: pytest with minimum 80% coverage

```bash
# Format Python code
black agents/ services/ --line-length 88
isort agents/ services/

# Type checking
mypy agents/ services/ --ignore-missing-imports

# Linting
flake8 agents/ services/
```

#### Java Code Standards
- **Formatting**: Google Java Format
- **Code Quality**: Checkstyle, SpotBugs, PMD
- **Documentation**: Javadoc for all public APIs
- **Testing**: JUnit 5 with minimum 80% coverage

```bash
# Format Java code (in service directory)
mvn com.coveo:fmt-maven-plugin:format

# Run quality checks
mvn checkstyle:check
mvn spotbugs:check
mvn pmd:check

# Run tests with coverage
mvn test jacoco:report
```

### 6. Performance Optimization

#### Local Development Performance
```bash
# Optimize Docker resource usage
# Edit docker-compose.override.yml to reduce memory limits

# Use specific service startup
make infra-start  # Start only infrastructure
# Then start specific agents as needed

# Monitor resource usage
docker stats
htop  # or top on macOS/Linux
```

#### Code Performance
```python
# Python profiling
import cProfile
cProfile.run('your_function()')

# Memory profiling
from memory_profiler import profile
@profile
def your_function():
    pass
```

```java
// Java profiling with JProfiler or async-profiler
// Add JVM arguments for profiling
-XX:+FlightRecorder -XX:StartFlightRecording=duration=60s,filename=profile.jfr
```

## IDE Configuration

### Visual Studio Code Setup

#### Recommended Extensions
```bash
# Install all recommended extensions
code --install-extension ms-python.python
code --install-extension vscjava.vscode-java-pack
code --install-extension ms-vscode.vscode-typescript-next
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
code --install-extension eamodio.gitlens
code --install-extension esbenp.prettier-vscode
code --install-extension dbaeumer.vscode-eslint
```

#### Workspace Settings
Create `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "./agents/orchestrator/.venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.testing.pytestEnabled": true,
  "java.configuration.updateBuildConfiguration": "automatic",
  "java.format.settings.url": "https://raw.githubusercontent.com/google/styleguide/gh-pages/eclipse-java-google-style.xml",
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/node_modules": true,
    "**/target": true
  }
}
```

#### Debug Configurations
Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Orchestrator Agent",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/agents/orchestrator/main.py",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}/agents/orchestrator",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/agents/orchestrator"
      }
    },
    {
      "name": "Java: Log Ingestion Service",
      "type": "java",
      "request": "launch",
      "mainClass": "com.agentic.soc.LogIngestionApplication",
      "projectName": "log-ingestion-service",
      "cwd": "${workspaceFolder}/services/log-ingestion"
    }
  ]
}
```

### IntelliJ IDEA Setup

#### Project Configuration
1. Open project root directory
2. Configure Project SDK: Java 21
3. Set up Python interpreter for each agent
4. Configure Maven for Java services
5. Install recommended plugins:
   - Python Plugin
   - Docker Plugin
   - Kubernetes Plugin

#### Code Style Settings
1. Import Google Java Style: Settings → Editor → Code Style → Java
2. Configure Python formatting: Settings → Tools → External Tools → Black

## Common Development Tasks

### Adding a New Agent
```bash
# 1. Create agent directory structure
mkdir -p agents/new-agent/{src,tests,config}

# 2. Initialize Python project
cd agents/new-agent
poetry init
poetry add fastapi uvicorn pydantic

# 3. Create basic agent structure
# See existing agents for templates

# 4. Add to docker-compose.override.yml
# 5. Update documentation
```

### Adding a New Service
```bash
# 1. Create service directory
mkdir -p services/new-service

# 2. Initialize Maven project
cd services/new-service
mvn archetype:generate -DgroupId=com.agentic.soc -DartifactId=new-service

# 3. Add Spring Boot dependencies
# 4. Create service implementation
# 5. Add to docker-compose.yml
```

### Database Migrations
```bash
# 1. Create migration script
# data/sql/migrations/V2__add_new_table.sql

# 2. Test migration locally
make shell-postgres
\i /docker-entrypoint-initdb.d/V2__add_new_table.sql

# 3. Update schema documentation
```

### Adding New Dependencies

#### Python Dependencies
```bash
cd agents/agent-name
poetry add new-package
poetry add --group dev new-dev-package
```

#### Java Dependencies
```xml
<!-- Add to pom.xml -->
<dependency>
    <groupId>com.example</groupId>
    <artifactId>new-dependency</artifactId>
    <version>1.0.0</version>
</dependency>
```

## Getting Help

### Documentation Resources
- [System Requirements](system-requirements.md)
- [Installation Guides](installation-guides/)
- [API Documentation](../api/)
- [Deployment Guide](../deployment/)

### Troubleshooting Resources
- [Common Issues](troubleshooting.md)
- [Performance Tuning](performance-tuning.md)
- [Security Guidelines](security-guidelines.md)

### Community and Support
- **Internal Wiki**: [Link to internal documentation]
- **Slack Channel**: #agentic-soc-dev
- **Issue Tracker**: [Link to issue tracker]
- **Code Reviews**: All PRs require review

### Emergency Contacts
- **Tech Lead**: [Contact information]
- **DevOps Team**: [Contact information]
- **Security Team**: [Contact information]

## Next Steps

After completing this onboarding:

1. **Complete the setup**: Ensure all validation checks pass
2. **Run the test suite**: Verify your environment works correctly
3. **Explore the codebase**: Start with the orchestrator agent
4. **Pick up a starter task**: Look for "good first issue" labels
5. **Join the team**: Introduce yourself in the team channel

Welcome to the team! 🚀