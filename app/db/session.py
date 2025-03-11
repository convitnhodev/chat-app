from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
import asyncio


client = AsyncIOMotorClient(settings.DATABASE_URL)
database = client.get_database(settings.DATABASE_NAME)

async def get_db():
    return database


async def test_connection():
    try:
        # Test the connection by listing collections
        collections = await database.list_collection_names()
        print("Successfully connected to MongoDB!")
        print(f"Available collections: {collections}")
        print(f"Database name: {settings.DATABASE_NAME}")
        return True
    except Exception as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
        return False

# Run the test
if __name__ == "__main__":
    asyncio.run(test_connection())