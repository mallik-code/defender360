# Development Environment Connection Details

## Web UI Access Points

### Kafka UI
- **URL**: http://localhost:8081
- **Purpose**: Monitor Kafka topics, messages, and cluster health

### Kibana (Elasticsearch UI)
- **URL**: http://localhost:5602
- **Purpose**: Search and visualize Elasticsearch data

### Redis Commander
- **URL**: http://localhost:8082
- **Purpose**: Browse and manage Redis data

### pgAdmin (PostgreSQL UI)
- **URL**: http://localhost:8083
- **Login Credentials**:
  - Email: `admin@example.com`
  - Password: `admin123`

## Database Connection Details

### PostgreSQL
- **Host**: `localhost` (or `agentic-soc-postgresql` from containers)
- **Port**: `5432`
- **Database**: `agentic_soc`
- **Username**: `soc_user`
- **Password**: `dev_password_123`
- **Connection String**: `postgresql://soc_user:dev_password_123@localhost:5432/agentic_soc`

### Redis
- **Host**: `localhost`
- **Port**: `6379`
- **No authentication required**
- **Connection String**: `redis://localhost:6379`

### Elasticsearch
- **Host**: `localhost`
- **Port**: `9201`
- **URL**: http://localhost:9201
- **No authentication required**

### Kafka
- **Bootstrap Servers**: `localhost:9093`
- **No authentication required**
- **Protocol**: PLAINTEXT

### Zookeeper
- **Host**: `localhost`
- **Port**: `2182`

## pgAdmin Server Configuration

When adding a server in pgAdmin:

### General Tab
- **Name**: `Agentic SOC Database`

### Connection Tab
- **Host name/address**: `agentic-soc-postgresql`
- **Port**: `5432`
- **Maintenance database**: `agentic_soc`
- **Username**: `soc_user`
- **Password**: `dev_password_123`

## Command Line Access

### PostgreSQL CLI
```bash
# From host machine
docker exec -it agentic-soc-postgresql psql -U soc_user -d agentic_soc

# Direct connection
psql -h localhost -p 5432 -U soc_user -d agentic_soc
```

### Redis CLI
```bash
# From host machine
docker exec -it agentic-soc-redis redis-cli

# Direct connection
redis-cli -h localhost -p 6379
```

### Kafka CLI Examples
```bash
# List topics
docker exec -it agentic-soc-kafka kafka-topics --bootstrap-server localhost:9092 --list

# Create topic
docker exec -it agentic-soc-kafka kafka-topics --bootstrap-server localhost:9092 --create --topic test-topic --partitions 3 --replication-factor 1

# Produce messages
docker exec -it agentic-soc-kafka kafka-console-producer --bootstrap-server localhost:9092 --topic test-topic

# Consume messages
docker exec -it agentic-soc-kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic test-topic --from-beginning
```

### Elasticsearch CLI
```bash
# Check cluster health
curl http://localhost:9201/_cluster/health

# List indices
curl http://localhost:9201/_cat/indices

# Create index
curl -X PUT http://localhost:9201/security-events
```

## Environment Variables

For application configuration:

```bash
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
KAFKA_BOOTSTRAP_SERVERS=localhost:9093

# Elasticsearch
ELASTICSEARCH_URL=http://localhost:9201
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9201
```

## Docker Container Names

- **PostgreSQL**: `agentic-soc-postgresql`
- **Redis**: `agentic-soc-redis`
- **Kafka**: `agentic-soc-kafka`
- **Zookeeper**: `agentic-soc-zookeeper`
- **Elasticsearch**: `agentic-soc-elasticsearch`
- **Kibana**: `agentic-soc-kibana`
- **Kafka UI**: `agentic-soc-kafka-ui`
- **Redis Commander**: `agentic-soc-redis-commander`
- **pgAdmin**: `agentic-soc-pgadmin`