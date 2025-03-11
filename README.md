# MongoDB Docker Setup

This guide explains how to set up MongoDB using Docker.

## Prerequisites

- Docker installed on your system
- Basic understanding of Docker commands

## Quick Start

Run MongoDB container with the following command:

```bash
docker run -d --name mongodb -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=appchat \
  -v mongo_data:/data/db \
  mongodb/mongodb-community-server
```

### Command Explanation

- `-d`: Run container in detached mode (background)
- `--name mongodb`: Name the container "mongodb"
- `-p 27017:27017`: Map container port 27017 to host port 27017
- `-e MONGO_INITDB_ROOT_USERNAME=admin`: Set root username
- `-e MONGO_INITDB_ROOT_PASSWORD=appchat`: Set root password
- `-v mongo_data:/data/db`: Create persistent volume for data storage

## Connection Details

- **Host**: localhost
- **Port**: 27017
- **Username**: admin
- **Password**: appchat

## Useful Commands

```bash
# Check container status
docker ps

# Stop MongoDB container
docker stop mongodb

# Start MongoDB container
docker start mongodb

# Remove MongoDB container
docker rm mongodb

# View container logs
docker logs mongodb
```

## Connection String

Use this connection string in your applications: