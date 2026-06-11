from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List,Union
from pydantic import Field, field_validator


class DefaultSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra = "ignore",
        frozen=True,
        env_nested_delimiter="__"
    )
    
class Settings(DefaultSettings):
    """All Application's URL and Config"""
    
    app_version: str = "0.1.0"
    debug: bool = True
    environment:str = "dev"
    service_name: str = "RAG"
    
    #Postgres config
    postgres_database_url: str = "postgresql://prod_rag:prodrag_password@localhost:5002/prodrag_db"
    postgres_echo_sql: bool = False
    postgres_pool_size: int = 20 #How many database connections SQLAlchemy keeps ready.
    postgres_max_overflow: int = 0
    
    # OpenSearch configuration
    opensearch_host: str = "http://localhost:9200"
    
    # Ollama configuration
    ollama_host: str = "http://localhost:11434"
    ollama_models: Union[str, List[str]] = Field(default=["gpt-oss:20b", "llama3.2:1b"])
    ollama_default_model: str = "llama3.2:1b"
    ollama_timeout: int = 300  # 5 minutes for large model operations

    @field_validator("ollama_models", mode="before")
    @classmethod
    def parse_ollama_models(cls, v):
        """Parse comma-separated string into list of models.
        Environment variables are read as strings. The validator runs before Pydantic validation 
        and converts a comma-separated string such as 'gpt-oss:20b,llama3.2:1b' into a Python list.
        This allows the application to accept both string and 
        list formats while storing a consistent structure internally."""
        
        if isinstance(v, str):
            return [model.strip() for model in v.split(",") if model.strip()]
        return v


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()