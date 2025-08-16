from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    FILE_ALLOWED_TYPE: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int
    MONGO_URI: str
    MONGODB_DATABASE: str
    GENERATION_BACKEND:str
    EMBEDDING_BACKEND:str
    OPENAI_API_KEY:str = None
    OPENAI_API_URL:str = None
    COHERE_API_KEY:str = None
    GENERATION_MODEL_ID:str = None
    EMBEDDING_MODEL_ID:str = None
    EMBEDDING_MODEL_SIZE:int = None
    DEFAULT_INPUT_MAX_CHARACTERS:int = None
    DEFAULT_GENERATATION_OUTPUT_TOKENS:int = None
    DEFAULT_TEMPRATURE:float = None

    
    model_config = SettingsConfigDict(env_file=".env")

def get_settings():
    return Settings()