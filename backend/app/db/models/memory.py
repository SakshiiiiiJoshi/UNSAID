from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from .user import Base

class Memory(Base):
    __tablename__ = "memories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # We store the ciphertext, not the plaintext.
    # This string should contain the Base64 encoded AES-GCM ciphertext,
    # which includes the IV (Initialization Vector), the encrypted payload, and the Auth Tag.
    encrypted_data = Column(String, nullable=False)
    
    # Optional category or mood, also encrypted so the server can't profile the user
    encrypted_category = Column(String, nullable=True)
    
    # Memory Dial setting: "7_days", "until_delete", "vault"
    retention = Column(String, nullable=False, default="until_delete")
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    owner_id = Column(String, ForeignKey("users.id"))
    owner = relationship("User", back_populates="memories")
