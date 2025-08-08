import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

async def test_connection():
    try:
        # Set default environment variables if .env doesn't exist
        if not os.path.exists('.env'):
            os.environ.setdefault('APP_NAME', 'RAG-Full-Project')
            os.environ.setdefault('APP_VERSION', '1.0.0')
            os.environ.setdefault('FILE_ALLOWED_TYPE', '["application/pdf","text/plain"]')
            os.environ.setdefault('FILE_MAX_SIZE', '10')
            os.environ.setdefault('FILE_DEFAULT_CHUNK_SIZE', '8192')
            os.environ.setdefault('MONGO_URI', 'mongodb://localhost:27017')
            os.environ.setdefault('MONGODB_DATABASE', 'rag_project')
        
        settings = get_settings()
        print(f"Settings loaded: {settings.APP_NAME}")
        print(f"MongoDB URI: {settings.MONGO_URI}")
        print(f"Database: {settings.MONGODB_DATABASE}")
        
        # Test MongoDB connection
        client = AsyncIOMotorClient(settings.MONGO_URI)
        db = client[settings.MONGODB_DATABASE]
        
        # Test connection
        await client.admin.command('ping')
        print("MongoDB connection successful!")
        
        # Test collection operations
        collections = db.list_collection_names()
        print(f"Existing collections: {collections}")
        
        client.close()
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())
