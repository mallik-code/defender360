#!/bin/bash

# Simple cleanup script for development environment

echo "Cleaning up development environment..."

# Stop and remove containers
docker-compose down

# Remove volumes (optional - uncomment if you want to reset data)
# docker-compose down -v

# Clean Docker system (removes unused containers, networks, images)
docker system prune -f

echo "Cleanup complete!"