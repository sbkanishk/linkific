import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

class Settings:
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "fastapi_practice")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")


    
    def DATABASE_URL_SQLALCHEMY(self) -> str:
        # Import the quoting tool
        from urllib.parse import quote_plus
        
        # Safely encode the password characters
        safe_password = quote_plus(self.DB_PASSWORD)
        
        # Generates the safe connection string
        return f"postgresql://{self.DB_USER}:{safe_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
settings = Settings()