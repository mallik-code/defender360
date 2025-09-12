#!/usr/bin/env python3
"""
Automated Development Environment Setup Script
Sets up the complete development environment for the Agentic SOC Framework.
"""

import os
import sys
import subprocess
import platform
import shutil
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class SetupStep:
    name: str
    description: str
    command: Optional[str] = None
    function: Optional[callable] = None
    required: bool = True
    platform_specific: Optional[List[str]] = None

class EnvironmentSetup:
    """Handles automated development environment setup."""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.project_root = Path.cwd()
        self.setup_steps: List[SetupStep] = []
        
    def run_command(self, command: str, shell: bool = True, cwd: Optional[Path] = None) -> bool:
        """Run a system command and return success status."""
        try:
            print(f"  Running: {command}")
            result = subprocess.run(
                command,
                shell=shell,
                cwd=cwd or self.project_root,
                check=True,
                capture_output=False
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Command failed with exit code {e.returncode}")
            return False
        except Exception as e:
            print(f"  ❌ Command failed: {e}")
            return False
    
    def create_directory_structure(self) -> bool:
        """Create the project directory structure."""
        directories = [
            "agents/orchestrator",
            "agents/anomaly-detection",
            "agents/threat-intelligence", 
            "agents/alert-prioritization",
            "agents/response-automation",
            "agents/forensics",
            "agents/learning",
            "agents/human-collaboration",
            "services/log-ingestion",
            "services/shared-libs/python",
            "services/shared-libs/java",
            "infrastructure/docker",
            "infrastructure/kubernetes",
            "infrastructure/terraform",
            "docs/api",
            "docs/deployment",
            "tests/unit",
            "tests/integration",
            "tests/e2e",
            "data/test-data",
            "data/models",
            "config/development",
            "config/production",
            "scripts/deployment",
            "scripts/testing",
            ".github/workflows"
        ]
        
        try:
            for directory in directories:
                dir_path = self.project_root / directory
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"  ✅ Created directory: {directory}")
            return True
        except Exception as e:
            print(f"  ❌ Failed to create directories: {e}")
            return False
    
    def create_docker_compose_files(self) -> bool:
        """Create Docker Compose configuration files."""
        try:
            # Main docker-compose.yml for development
            docker_compose_content = self.get_docker_compose_content()
            docker_compose_path = self.project_root / "docker-compose.yml"
            with open(docker_compose_path, 'w') as f:
                f.write(docker_compose_content)
            print(f"  ✅ Created: docker-compose.yml")
            
            # Docker Compose override for development
            override_content = self.get_docker_compose_override_content()
            override_path = self.project_root / "docker-compose.override.yml"
            with open(override_path, 'w') as f:
                f.write(override_content)
            print(f"  ✅ Created: docker-compose.override.yml")
            
            # Test environment
            test_content = self.get_docker_compose_test_content()
            test_path = self.project_root / "docker-compose.test.yml"
            with open(test_path, 'w') as f:
                f.write(test_content)
            print(f"  ✅ Created: docker-compose.test.yml")
            
            return True
        except Exception as e:
            print(f"  ❌ Failed to create Docker Compose files: {e}")
            return False
    
    def get_docker_compose_content(self) -> str:
        """Generate the main Docker Compose configuration."""
        return '''version: '3.8'

services:
  # Infrastructure Services
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    hostname: zookeeper
    container_name: agentic-soc-zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    volumes:
      - zookeeper_data:/var/lib/zookeeper/data
      - zookeeper_logs:/var/lib/zookeeper/log
    networks:
      - agentic-soc-network

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    hostname: kafka
    container_name: agentic-soc-kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
      - "9101:9101"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_JMX_PORT: 9101
      KAFKA_JMX_HOSTNAME: localhost
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
    volumes:
      - kafka_data:/var/lib/kafka/data
    networks:
      - agentic-soc-network
    healthcheck:
      test: ["CMD", "kafka-broker-api-versions", "--bootstrap-server", "localhost:9092"]
      interval: 30s
      timeout: 10s
      retries: 3

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.3
    container_name: agentic-soc-elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms1g -Xmx2g"
      - bootstrap.memory_lock=true
    ulimits:
      memlock:
        soft: -1
        hard: -1
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - agentic-soc-network
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7.2-alpine
    container_name: agentic-soc-redis
    command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - agentic-soc-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgresql:
    image: postgres:16-alpine
    container_name: agentic-soc-postgresql
    environment:
      POSTGRES_DB: agentic_soc
      POSTGRES_USER: soc_user
      POSTGRES_PASSWORD: dev_password_123
      POSTGRES_INITDB_ARGS: "--encoding=UTF-8 --lc-collate=C --lc-ctype=C"
    ports:
      - "5432:5432"
    volumes:
      - postgresql_data:/var/lib/postgresql/data
      - ./data/sql/init:/docker-entrypoint-initdb.d
    networks:
      - agentic-soc-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U soc_user -d agentic_soc"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Development Tools
  kafka-ui:
    image: provectuslabs/kafka-ui:v0.7.1
    container_name: agentic-soc-kafka-ui
    depends_on:
      - kafka
    ports:
      - "8081:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:29092
      KAFKA_CLUSTERS_0_ZOOKEEPER: zookeeper:2181
    networks:
      - agentic-soc-network

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.3
    container_name: agentic-soc-kibana
    depends_on:
      - elasticsearch
    ports:
      - "5601:5601"
    environment:
      ELASTICSEARCH_HOSTS: http://elasticsearch:9200
      XPACK_SECURITY_ENABLED: false
    networks:
      - agentic-soc-network

  redis-commander:
    image: rediscommander/redis-commander:latest
    container_name: agentic-soc-redis-commander
    depends_on:
      - redis
    ports:
      - "8082:8081"
    environment:
      REDIS_HOSTS: local:redis:6379
    networks:
      - agentic-soc-network

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: agentic-soc-pgadmin
    depends_on:
      - postgresql
    ports:
      - "8083:80"
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@agentic-soc.local
      PGADMIN_DEFAULT_PASSWORD: admin123
      PGADMIN_CONFIG_SERVER_MODE: 'False'
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    networks:
      - agentic-soc-network

volumes:
  zookeeper_data:
  zookeeper_logs:
  kafka_data:
  elasticsearch_data:
  redis_data:
  postgresql_data:
  pgadmin_data:

networks:
  agentic-soc-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
'''

    def get_docker_compose_override_content(self) -> str:
        """Generate Docker Compose override for development."""
        return '''version: '3.8'

# Development overrides for hot reload and debugging
services:
  # Python Agent Services will be added here as they are developed
  # Each agent will have:
  # - Volume mounts for hot reload
  # - Debug port exposure
  # - Development environment variables
  
  # Java Services will be added here as they are developed
  # Each service will have:
  # - Volume mounts for hot reload
  # - Debug port exposure (5005, 5006, etc.)
  # - Development profiles activated

  # Example structure for future agents:
  # orchestrator-agent:
  #   build:
  #     context: ./agents/orchestrator
  #     dockerfile: Dockerfile.dev
  #   volumes:
  #     - ./agents/orchestrator:/app
  #   ports:
  #     - "8000:8000"  # API port
  #     - "5678:5678"  # Debug port
  #   environment:
  #     - PYTHONPATH=/app
  #     - DEBUG=true
  #   depends_on:
  #     - kafka
  #     - redis
  #     - postgresql
  #   networks:
  #     - agentic-soc-network

  # Reduce resource limits for development
  elasticsearch:
    environment:
      - "ES_JAVA_OPTS=-Xms512m -Xmx1g"
  
  kafka:
    environment:
      KAFKA_HEAP_OPTS: "-Xmx512m -Xms512m"
'''

    def get_docker_compose_test_content(self) -> str:
        """Generate Docker Compose configuration for testing."""
        return '''version: '3.8'

# Test environment with minimal resources and test data
services:
  zookeeper-test:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    tmpfs:
      - /var/lib/zookeeper/data
      - /var/lib/zookeeper/log

  kafka-test:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper-test
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper-test:2181'
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-test:29092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
    tmpfs:
      - /var/lib/kafka/data

  elasticsearch-test:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.3
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms256m -Xmx512m"
    tmpfs:
      - /usr/share/elasticsearch/data

  redis-test:
    image: redis:7.2-alpine
    command: redis-server --maxmemory 128mb --maxmemory-policy allkeys-lru
    tmpfs:
      - /data

  postgresql-test:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: agentic_soc_test
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
    tmpfs:
      - /var/lib/postgresql/data

  # Test runner service
  test-runner:
    build:
      context: .
      dockerfile: Dockerfile.test
    depends_on:
      - kafka-test
      - elasticsearch-test
      - redis-test
      - postgresql-test
    environment:
      - TEST_MODE=true
      - KAFKA_BOOTSTRAP_SERVERS=kafka-test:29092
      - ELASTICSEARCH_URL=http://elasticsearch-test:9200
      - REDIS_URL=redis://redis-test:6379
      - DATABASE_URL=postgresql://test_user:test_password@postgresql-test:5432/agentic_soc_test
    volumes:
      - .:/app
      - ./tests:/app/tests
      - ./data/test-data:/app/test-data
    command: pytest tests/ -v --cov=src/ --cov-report=html --cov-report=term
'''

    def create_environment_files(self) -> bool:
        """Create environment configuration files."""
        try:
            # Development .env file
            dev_env_content = '''# Development Environment Configuration
# Database
DATABASE_URL=postgresql://soc_user:dev_password_123@localhost:5432/agentic_soc
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=agentic_soc
DATABASE_USER=soc_user
DATABASE_PASSWORD=dev_password_123

# Redis
REDIS_URL=redis://localhost:6379
REDIS_HOST=localhost
REDIS_PORT=6379

# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_SECURITY_PROTOCOL=PLAINTEXT

# Elasticsearch
ELASTICSEARCH_URL=http://localhost:9200
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200

# Application Settings
DEBUG=true
LOG_LEVEL=DEBUG
ENVIRONMENT=development

# AI/ML Settings
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Security
JWT_SECRET_KEY=dev_jwt_secret_key_change_in_production
ENCRYPTION_KEY=dev_encryption_key_change_in_production

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
'''
            
            env_path = self.project_root / ".env.development"
            with open(env_path, 'w') as f:
                f.write(dev_env_content)
            print(f"  ✅ Created: .env.development")
            
            # Test environment file
            test_env_content = '''# Test Environment Configuration
DATABASE_URL=postgresql://test_user:test_password@localhost:5433/agentic_soc_test
REDIS_URL=redis://localhost:6380
KAFKA_BOOTSTRAP_SERVERS=localhost:9093
ELASTICSEARCH_URL=http://localhost:9201
DEBUG=true
LOG_LEVEL=DEBUG
ENVIRONMENT=test
'''
            
            test_env_path = self.project_root / ".env.test"
            with open(test_env_path, 'w') as f:
                f.write(test_env_content)
            print(f"  ✅ Created: .env.test")
            
            # Example production environment file
            prod_env_content = '''# Production Environment Configuration Template
# Copy to .env.production and update with actual values

# Database
DATABASE_URL=postgresql://username:password@host:port/database
DATABASE_HOST=your_db_host
DATABASE_PORT=5432
DATABASE_NAME=agentic_soc_prod
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_secure_password

# Redis
REDIS_URL=redis://your_redis_host:6379
REDIS_HOST=your_redis_host
REDIS_PORT=6379

# Kafka
KAFKA_BOOTSTRAP_SERVERS=your_kafka_host:9092
KAFKA_SECURITY_PROTOCOL=SASL_SSL
KAFKA_SASL_MECHANISM=PLAIN
KAFKA_SASL_USERNAME=your_kafka_user
KAFKA_SASL_PASSWORD=your_kafka_password

# Elasticsearch
ELASTICSEARCH_URL=https://your_elasticsearch_host:9200
ELASTICSEARCH_USERNAME=your_es_user
ELASTICSEARCH_PASSWORD=your_es_password

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
ENVIRONMENT=production

# AI/ML Settings
OPENAI_API_KEY=your_production_openai_key
ANTHROPIC_API_KEY=your_production_anthropic_key

# Security
JWT_SECRET_KEY=your_secure_jwt_secret
ENCRYPTION_KEY=your_secure_encryption_key

# Monitoring
PROMETHEUS_ENDPOINT=your_prometheus_endpoint
GRAFANA_ENDPOINT=your_grafana_endpoint
'''
            
            prod_env_path = self.project_root / ".env.production.template"
            with open(prod_env_path, 'w') as f:
                f.write(prod_env_content)
            print(f"  ✅ Created: .env.production.template")
            
            return True
        except Exception as e:
            print(f"  ❌ Failed to create environment files: {e}")
            return False
    
    def create_makefile(self) -> bool:
        """Create Makefile for common development tasks."""
        makefile_content = '''# Agentic SOC Framework - Development Makefile

.PHONY: help setup start stop restart logs clean test lint format validate

# Default target
help:
	@echo "Agentic SOC Framework - Development Commands"
	@echo "============================================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  setup          - Set up development environment"
	@echo "  validate       - Validate system dependencies"
	@echo ""
	@echo "Development Commands:"
	@echo "  start          - Start all services"
	@echo "  stop           - Stop all services"
	@echo "  restart        - Restart all services"
	@echo "  logs           - Show logs for all services"
	@echo "  logs-f         - Follow logs for all services"
	@echo ""
	@echo "Infrastructure Commands:"
	@echo "  infra-start    - Start infrastructure services only"
	@echo "  infra-stop     - Stop infrastructure services"
	@echo "  infra-logs     - Show infrastructure logs"
	@echo ""
	@echo "Testing Commands:"
	@echo "  test           - Run all tests"
	@echo "  test-unit      - Run unit tests"
	@echo "  test-integration - Run integration tests"
	@echo "  test-e2e       - Run end-to-end tests"
	@echo ""
	@echo "Code Quality Commands:"
	@echo "  lint           - Run linting on all code"
	@echo "  format         - Format all code"
	@echo "  type-check     - Run type checking"
	@echo ""
	@echo "Cleanup Commands:"
	@echo "  clean          - Clean up containers and volumes"
	@echo "  clean-all      - Clean everything including images"
	@echo "  reset          - Reset development environment"

# Setup and validation
setup:
	@echo "Setting up development environment..."
	python scripts/setup-dev-environment.py

validate:
	@echo "Validating system dependencies..."
	python scripts/validate-dependencies.py

# Development commands
start:
	@echo "Starting all services..."
	docker-compose up -d
	@echo "Services started. Access points:"
	@echo "  - Kafka UI: http://localhost:8081"
	@echo "  - Kibana: http://localhost:5601"
	@echo "  - Redis Commander: http://localhost:8082"
	@echo "  - pgAdmin: http://localhost:8083"

stop:
	@echo "Stopping all services..."
	docker-compose down

restart:
	@echo "Restarting all services..."
	docker-compose restart

logs:
	docker-compose logs

logs-f:
	docker-compose logs -f

# Infrastructure only
infra-start:
	@echo "Starting infrastructure services..."
	docker-compose up -d zookeeper kafka elasticsearch redis postgresql

infra-stop:
	@echo "Stopping infrastructure services..."
	docker-compose stop zookeeper kafka elasticsearch redis postgresql

infra-logs:
	docker-compose logs zookeeper kafka elasticsearch redis postgresql

# Testing
test:
	@echo "Running all tests..."
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

test-unit:
	@echo "Running unit tests..."
	pytest tests/unit/ -v

test-integration:
	@echo "Running integration tests..."
	pytest tests/integration/ -v

test-e2e:
	@echo "Running end-to-end tests..."
	pytest tests/e2e/ -v

# Code quality
lint:
	@echo "Running linting..."
	@echo "Python linting..."
	find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" | xargs black --check
	find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" | xargs isort --check-only
	find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" | xargs flake8

format:
	@echo "Formatting code..."
	@echo "Python formatting..."
	find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" | xargs black
	find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" | xargs isort

type-check:
	@echo "Running type checking..."
	mypy agents/ services/ --ignore-missing-imports

# Cleanup
clean:
	@echo "Cleaning up containers and volumes..."
	docker-compose down -v
	docker system prune -f

clean-all:
	@echo "Cleaning everything including images..."
	docker-compose down -v --rmi all
	docker system prune -a -f

reset: clean-all setup
	@echo "Development environment reset complete"

# Development helpers
shell-postgres:
	docker-compose exec postgresql psql -U soc_user -d agentic_soc

shell-redis:
	docker-compose exec redis redis-cli

shell-kafka:
	docker-compose exec kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic test-topic --from-beginning

# Health checks
health:
	@echo "Checking service health..."
	@echo "PostgreSQL:"
	@docker-compose exec postgresql pg_isready -U soc_user -d agentic_soc || echo "  ❌ PostgreSQL not ready"
	@echo "Redis:"
	@docker-compose exec redis redis-cli ping || echo "  ❌ Redis not ready"
	@echo "Elasticsearch:"
	@curl -s http://localhost:9200/_cluster/health | jq '.status' || echo "  ❌ Elasticsearch not ready"
	@echo "Kafka:"
	@docker-compose exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092 > /dev/null 2>&1 && echo "  ✅ Kafka ready" || echo "  ❌ Kafka not ready"
'''
        
        try:
            makefile_path = self.project_root / "Makefile"
            with open(makefile_path, 'w') as f:
                f.write(makefile_content)
            print(f"  ✅ Created: Makefile")
            return True
        except Exception as e:
            print(f"  ❌ Failed to create Makefile: {e}")
            return False
    
    def create_test_data_generators(self) -> bool:
        """Create test data generation scripts."""
        try:
            # Create test data directory structure
            test_data_dir = self.project_root / "data" / "test-data"
            test_data_dir.mkdir(parents=True, exist_ok=True)
            
            # Sample security events generator
            sample_events_content = '''#!/usr/bin/env python3
"""
Sample Security Events Generator
Generates realistic test security events for development and testing.
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List
import ipaddress

class SecurityEventGenerator:
    """Generates sample security events for testing."""
    
    def __init__(self):
        self.event_types = [
            "authentication_failure",
            "malware_detection",
            "network_intrusion",
            "data_exfiltration",
            "privilege_escalation",
            "suspicious_process",
            "dns_tunneling",
            "lateral_movement"
        ]
        
        self.severities = ["low", "medium", "high", "critical"]
        self.sources = ["siem", "edr", "ndr", "email_security", "cloud_security"]
        
    def generate_ip(self) -> str:
        """Generate a random IP address."""
        return str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))
    
    def generate_event(self) -> Dict:
        """Generate a single security event."""
        event_id = str(uuid.uuid4())
        timestamp = datetime.utcnow() - timedelta(
            minutes=random.randint(0, 1440)  # Last 24 hours
        )
        
        event = {
            "id": event_id,
            "timestamp": timestamp.isoformat() + "Z",
            "source": random.choice(self.sources),
            "event_type": random.choice(self.event_types),
            "severity": random.choice(self.severities),
            "raw_data": {
                "source_ip": self.generate_ip(),
                "destination_ip": self.generate_ip(),
                "user_id": f"user_{random.randint(1000, 9999)}",
                "asset_id": f"asset_{random.randint(100, 999)}",
                "action": random.choice(["login", "file_access", "network_connection", "process_execution"]),
                "outcome": random.choice(["success", "failure", "blocked"])
            },
            "normalized_data": {},
            "enrichment": {},
            "processing_history": []
        }
        
        return event
    
    def generate_batch(self, count: int = 100) -> List[Dict]:
        """Generate a batch of security events."""
        return [self.generate_event() for _ in range(count)]
    
    def save_to_file(self, events: List[Dict], filename: str):
        """Save events to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(events, f, indent=2)

if __name__ == "__main__":
    generator = SecurityEventGenerator()
    
    # Generate different sized batches
    small_batch = generator.generate_batch(10)
    medium_batch = generator.generate_batch(100)
    large_batch = generator.generate_batch(1000)
    
    generator.save_to_file(small_batch, "data/test-data/sample_events_small.json")
    generator.save_to_file(medium_batch, "data/test-data/sample_events_medium.json")
    generator.save_to_file(large_batch, "data/test-data/sample_events_large.json")
    
    print("✅ Generated test security events:")
    print(f"  - Small batch: 10 events")
    print(f"  - Medium batch: 100 events") 
    print(f"  - Large batch: 1000 events")
'''
            
            generator_path = self.project_root / "scripts" / "generate-test-data.py"
            with open(generator_path, 'w') as f:
                f.write(sample_events_content)
            print(f"  ✅ Created: scripts/generate-test-data.py")
            
            # SQL initialization script
            sql_init_content = '''-- Agentic SOC Framework Database Initialization
-- Creates initial database schema and test data

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS security_events;
CREATE SCHEMA IF NOT EXISTS agents;
CREATE SCHEMA IF NOT EXISTS threat_intel;

-- Security Events table
CREATE TABLE IF NOT EXISTS security_events.events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMPTZ NOT NULL,
    source VARCHAR(100) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    raw_data JSONB NOT NULL,
    normalized_data JSONB DEFAULT '{}',
    enrichment JSONB DEFAULT '{}',
    processing_history JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Agents state table
CREATE TABLE IF NOT EXISTS agents.agent_state (
    agent_id VARCHAR(100) PRIMARY KEY,
    agent_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    version VARCHAR(20) NOT NULL,
    capabilities JSONB DEFAULT '[]',
    current_load INTEGER DEFAULT 0,
    max_capacity INTEGER DEFAULT 100,
    health_metrics JSONB DEFAULT '{}',
    last_heartbeat TIMESTAMPTZ DEFAULT NOW(),
    configuration JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Threat Intelligence table
CREATE TABLE IF NOT EXISTS threat_intel.indicators (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type VARCHAR(50) NOT NULL,
    value TEXT NOT NULL,
    confidence DECIMAL(3,2) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    source VARCHAR(100) NOT NULL,
    first_seen TIMESTAMPTZ NOT NULL,
    last_seen TIMESTAMPTZ NOT NULL,
    tags TEXT[] DEFAULT '{}',
    context JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON security_events.events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_type ON security_events.events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_severity ON security_events.events(severity);
CREATE INDEX IF NOT EXISTS idx_events_source ON security_events.events(source);
CREATE INDEX IF NOT EXISTS idx_events_raw_data_gin ON security_events.events USING gin(raw_data);

CREATE INDEX IF NOT EXISTS idx_agent_state_type ON agents.agent_state(agent_type);
CREATE INDEX IF NOT EXISTS idx_agent_state_status ON agents.agent_state(status);
CREATE INDEX IF NOT EXISTS idx_agent_state_heartbeat ON agents.agent_state(last_heartbeat);

CREATE INDEX IF NOT EXISTS idx_indicators_type ON threat_intel.indicators(type);
CREATE INDEX IF NOT EXISTS idx_indicators_value ON threat_intel.indicators(value);
CREATE INDEX IF NOT EXISTS idx_indicators_severity ON threat_intel.indicators(severity);

-- Insert sample data
INSERT INTO agents.agent_state (agent_id, agent_type, status, version, capabilities) VALUES
('orchestrator-001', 'orchestrator', 'active', '1.0.0', '["coordination", "workflow_management"]'),
('anomaly-detection-001', 'anomaly_detection', 'active', '1.0.0', '["ml_detection", "behavioral_analysis"]'),
('threat-intel-001', 'threat_intelligence', 'active', '1.0.0', '["ioc_correlation", "attribution"]'),
('alert-priority-001', 'alert_prioritization', 'active', '1.0.0', '["risk_scoring", "asset_context"]'),
('response-automation-001', 'response_automation', 'active', '1.0.0', '["containment", "playbook_execution"]')
ON CONFLICT (agent_id) DO NOTHING;

-- Insert sample threat intelligence
INSERT INTO threat_intel.indicators (type, value, confidence, severity, source, first_seen, last_seen, tags) VALUES
('ip', '192.168.1.100', 0.85, 'high', 'internal_analysis', NOW() - INTERVAL '7 days', NOW(), ARRAY['malware', 'c2']),
('domain', 'malicious-domain.com', 0.92, 'critical', 'threat_feed', NOW() - INTERVAL '3 days', NOW(), ARRAY['phishing', 'apt']),
('hash', 'a1b2c3d4e5f6789012345678901234567890abcd', 0.95, 'critical', 'malware_analysis', NOW() - INTERVAL '1 day', NOW(), ARRAY['ransomware']),
('url', 'http://suspicious-site.net/payload', 0.78, 'medium', 'web_crawler', NOW() - INTERVAL '5 days', NOW(), ARRAY['exploit_kit'])
ON CONFLICT DO NOTHING;

COMMIT;
'''
            
            sql_dir = self.project_root / "data" / "sql" / "init"
            sql_dir.mkdir(parents=True, exist_ok=True)
            sql_init_path = sql_dir / "01-init-schema.sql"
            with open(sql_init_path, 'w') as f:
                f.write(sql_init_content)
            print(f"  ✅ Created: data/sql/init/01-init-schema.sql")
            
            return True
        except Exception as e:
            print(f"  ❌ Failed to create test data generators: {e}")
            return False
    
    def create_cleanup_scripts(self) -> bool:
        """Create environment cleanup and reset scripts."""
        try:
            # Cleanup script
            cleanup_content = '''#!/usr/bin/env python3
"""
Development Environment Cleanup Script
Cleans up Docker containers, volumes, and temporary files.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"  {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"    ✅ {description} completed")
            return True
        else:
            print(f"    ⚠️  {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"    ❌ {description} error: {e}")
        return False

def main():
    """Main cleanup function."""
    print("🧹 Cleaning up development environment...")
    print()
    
    # Stop all containers
    run_command("docker-compose down", "Stopping containers")
    
    # Remove volumes
    run_command("docker-compose down -v", "Removing volumes")
    
    # Clean up Docker system
    run_command("docker system prune -f", "Cleaning Docker system")
    
    # Remove temporary files
    temp_patterns = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/.pytest_cache",
        "**/node_modules",
        "**/.coverage",
        "**/htmlcov",
        "**/*.log"
    ]
    
    project_root = Path.cwd()
    for pattern in temp_patterns:
        for path in project_root.glob(pattern):
            try:
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    import shutil
                    shutil.rmtree(path)
                print(f"    ✅ Removed: {path}")
            except Exception as e:
                print(f"    ⚠️  Could not remove {path}: {e}")
    
    print()
    print("✅ Cleanup completed!")

if __name__ == "__main__":
    main()
'''
            
            cleanup_path = self.project_root / "scripts" / "cleanup-dev-environment.py"
            with open(cleanup_path, 'w') as f:
                f.write(cleanup_content)
            print(f"  ✅ Created: scripts/cleanup-dev-environment.py")
            
            # Reset script
            reset_content = '''#!/usr/bin/env python3
"""
Development Environment Reset Script
Completely resets the development environment to a clean state.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Main reset function."""
    print("🔄 Resetting development environment...")
    print()
    
    # Run cleanup first
    print("Step 1: Cleaning up existing environment")
    result = subprocess.run([sys.executable, "scripts/cleanup-dev-environment.py"])
    if result.returncode != 0:
        print("❌ Cleanup failed")
        sys.exit(1)
    
    print()
    print("Step 2: Rebuilding environment")
    result = subprocess.run([sys.executable, "scripts/setup-dev-environment.py"])
    if result.returncode != 0:
        print("❌ Setup failed")
        sys.exit(1)
    
    print()
    print("✅ Environment reset completed!")
    print("You can now run 'make start' to start the services.")

if __name__ == "__main__":
    main()
'''
            
            reset_path = self.project_root / "scripts" / "reset-dev-environment.py"
            with open(reset_path, 'w') as f:
                f.write(reset_content)
            print(f"  ✅ Created: scripts/reset-dev-environment.py")
            
            return True
        except Exception as e:
            print(f"  ❌ Failed to create cleanup scripts: {e}")
            return False
    
    def run_setup(self):
        """Run the complete setup process."""
        print("🚀 Agentic SOC Framework - Development Environment Setup")
        print("=" * 60)
        print()
        
        setup_steps = [
            ("Creating project directory structure", self.create_directory_structure),
            ("Creating Docker Compose configuration", self.create_docker_compose_files),
            ("Creating environment configuration files", self.create_environment_files),
            ("Creating Makefile for development tasks", self.create_makefile),
            ("Creating test data generators", self.create_test_data_generators),
            ("Creating cleanup and reset scripts", self.create_cleanup_scripts),
        ]
        
        success_count = 0
        total_steps = len(setup_steps)
        
        for step_name, step_function in setup_steps:
            print(f"📋 {step_name}...")
            if step_function():
                success_count += 1
                print(f"  ✅ Completed")
            else:
                print(f"  ❌ Failed")
            print()
        
        # Summary
        print("📊 Setup Summary")
        print("-" * 40)
        print(f"✅ Completed: {success_count}/{total_steps}")
        print(f"❌ Failed: {total_steps - success_count}/{total_steps}")
        print()
        
        if success_count == total_steps:
            print("🎉 Development environment setup completed successfully!")
            print()
            print("Next steps:")
            print("1. Run 'make validate' to check system dependencies")
            print("2. Run 'make start' to start the development environment")
            print("3. Access the services:")
            print("   - Kafka UI: http://localhost:8081")
            print("   - Kibana: http://localhost:5601")
            print("   - Redis Commander: http://localhost:8082")
            print("   - pgAdmin: http://localhost:8083")
            print()
            print("For more commands, run 'make help'")
            return True
        else:
            print("❌ Setup completed with errors. Please check the output above.")
            return False

def main():
    """Main setup function."""
    setup = EnvironmentSetup()
    success = setup.run_setup()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()