import logging
from contextlib import contextmanager
from typing import List, Any, Optional, Generator
from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from src.db.interfaces.base import BaseDatabase

logger = logging.getLogger(__name__)

class PostgreSQLSettings(BaseSettings):
    """Postgresql Configuration"""
    # In Pydantic, Field is used to provide additional 
    # metadata, validation rules, constraints, and default values for model fields.
    database_url: str = Field(
        default = "postgresql://prod_rag:prodrag_password@localhost:5002/prodrag_db"
    )
    echo_sql: bool = Field(default=False, description="Enable SQL query logging")
    pool_size: int = Field(default=20, description="Database connection pool size") #How many database connections SQLAlchemy keeps ready.
    max_overflow: int = Field(default=0, description="Maximum pool overflow")
    
    class Config:
        env_prefix = "POSTGRES_"
    
Base = declarative_base()

class PostgreSQLDatabase(BaseDatabase):
    """PostgreSQL database implementation"""
    
    def __init__(self, config:PostgreSQLSettings):
        self.config = config
        self.engine:Optional[Engine] = None
        self.session_factory: Optional[sessionmaker] = None
    
    def startup(self) -> None:
        """Initialize the database connection"""
        try:
            logger.info(
                f"PostgreSQL Connection Attempt at {self.config.database_url.split("@")[1] if "@" in self.config.database_url else "localhost"}"
                )
            
            self.engine = create_engine(
                self.config.database_url,
                echo = self.config.echo_sql,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_pre_ping=True # Verify connections before use
            )
            assert self.engine is not None
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("Database Connection Successful")
            
            # Check which tables exist before creating
            inspector = inspect(self.engine)
            existing_tables = inspector.get_table_names()

            # Create tables if they don't exist (idempotent operation)
            Base.metadata.create_all(bind=self.engine)

            # Check if any new tables were created
            updated_tables = inspector.get_table_names()
            new_tables = set(updated_tables) - set(existing_tables)

            if new_tables:
                logger.info(f"Created new tables: {', '.join(new_tables)}")
            else:
                logger.info("All tables already exist - no new tables created")

            logger.info("PostgreSQL database initialized successfully")
            assert self.engine is not None
            logger.info(f"Database: {self.engine.url.database}")
            logger.info(f"Total tables: {', '.join(updated_tables) if updated_tables else 'None'}")
            logger.info("Database connection established")

        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL database: {e}")
            raise
    
    def teardown(self) -> None:
        """Close the database connection."""
        if self.engine:
            self.engine.dispose()
            logger.info("PostgreSQL database connections closed")
      
            
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get a database session."""
        if not self.session_factory:
            raise RuntimeError("Database not initialized. Call startup() first.")

        session = self.session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
