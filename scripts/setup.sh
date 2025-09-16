#!/bin/bash

# Simple setup script for Agentic SOC Framework

echo "Setting up Agentic SOC Framework..."

# Run the comprehensive setup script
echo "Running development environment setup..."
python scripts/setup-dev-environment.py

# Start Docker containers
echo "Starting Docker containers..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 30

echo "Setup complete!"
echo "Access points:"
echo "- Kafka UI: http://localhost:8081"
echo "- Kibana: http://localhost:5601"
echo "- Redis Commander: http://localhost:8082"
echo "- pgAdmin: http://localhost:8083"