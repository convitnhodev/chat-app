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

## Test Connection

### Using Python Motor (Async)

1. First, ensure you have the required dependencies:
```bash
pip install motor pymongo
```

2. The connection test is implemented in `app/db/session.py`:
```python
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

from app.core.config import settings

client = AsyncIOMotorClient(settings.DATABASE_URL)
database = client.get_database(settings.DATABASE_NAME)

async def test_connection():
    try:
        collections = await database.list_collection_names()
        print("Successfully connected to MongoDB!")
        print(f"Available collections: {collections}")
        print(f"Database name: {settings.DATABASE_NAME}")
        return True
    except Exception as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
        return False
```

3. Run the test:
```bash
# From project root directory
python -m app.db.session
```

If the connection is successful, you should see output similar to:


### Running the Application

You can run the application using one of the following commands:

#### Development mode (with auto-reload)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Production mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Command options explained:
- `app.main:app` - Path to your FastAPI application instance
- `--reload` - Enable auto-reload on code changes (development only)
- `--host 0.0.0.0` - Make server accessible from external machines
- `--port 8000` - Run server on port 8000

The API will be available at:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc