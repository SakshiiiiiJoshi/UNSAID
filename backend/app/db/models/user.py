from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # In a privacy-first app, we might avoid emails entirely, or keep them optional
    username = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True) # Could be null if using device-based auth
    
    # For Multi-Device Sync Asymmetric Cryptography:
    # We store the user's PUBLIC key here. The private key never leaves their device.
    public_key = Column(String, nullable=True) 
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)

    memories = relationship("Memory", back_populates="owner")
