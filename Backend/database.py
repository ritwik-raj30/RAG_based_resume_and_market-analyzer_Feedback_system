from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv
import os
import logging
from threading import Lock

load_dotenv()

logger = logging.getLogger(__name__)

class DatabaseSingleton:
    """
    Singleton pattern for MongoDB connection with proper connection pooling
    Ensures only one database connection instance exists
    """
    _instance = None
    _lock = Lock()
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseSingleton, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._connect()
    
    def _connect(self):
        """Initialize MongoDB connection with proper configuration"""
        MONGO_URI = os.getenv("MONGODB_URI")
        if not MONGO_URI:
            raise ValueError("MONGODB_URI not found in environment variables")
        
        try:
            # Connection pooling configuration for production
            self._client = MongoClient(
                MONGO_URI,
                maxPoolSize=50,  # Maximum number of connections in pool
                minPoolSize=10,  # Minimum number of connections in pool
                maxIdleTimeMS=45000,  # Close connections after 45s of inactivity
                serverSelectionTimeoutMS=5000,  # Timeout for server selection
                connectTimeoutMS=10000,  # Connection timeout
                socketTimeoutMS=20000,  # Socket timeout
                retryWrites=True,  # Retry write operations on network errors
                retryReads=True    # Retry read operations on network errors
            )
            
            # Test connection
            self._client.admin.command('ping')
            logger.info("✅ MongoDB connection established successfully")
            
            # Get database
            self._db = self._client.resume_db
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected database error: {e}")
            raise
    
    @property
    def client(self):
        """Get MongoDB client instance"""
        if self._client is None:
            self._connect()
        return self._client
    
    @property
    def db(self):
        """Get database instance"""
        if self._db is None:
            self._connect()
        return self._db
    
    @property
    def collection(self):
        """Get user_data collection"""
        return self.db["user_data"]
    
    @property
    def resume_collection(self):
        """Get resumes collection"""
        return self.db.resumes
    
    def close(self):
        """Close database connection"""
        if self._client:
            self._client.close()
            logger.info("MongoDB connection closed")

# Create singleton instance
_db_singleton = DatabaseSingleton()

# Export collections for backward compatibility (so existing imports still work)
collection = _db_singleton.collection
resume_collection = _db_singleton.resume_collection
client = _db_singleton.client
db = _db_singleton.db
