from abc import ABC, abstractmethod
from typing import Any, ContextManager, Dict, List, Optional

from sqlalchemy.orm import Session


class BaseDatabase(ABC):
# An abstract method is a method that is declared but not implemented in a base class. 
# It defines what a subclass must do, but not how it should do it.
    """Base class for database operation"""
    
    @abstractmethod
    def startup(self) -> None:
        """Initialize the database connection."""

    @abstractmethod
    def teardown(self) -> None:
        """Close the database connection."""

    @abstractmethod
    def get_session(self) -> ContextManager[Session]:
        """Get a database session."""
        
