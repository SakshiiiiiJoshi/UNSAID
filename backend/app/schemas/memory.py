from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class MemoryCreate(BaseModel):
    """Client sends already-encrypted data. Server never sees plaintext."""
    encrypted_data: str = Field(..., description="Base64-encoded AES-GCM ciphertext")
    encrypted_category: Optional[str] = Field(None, description="Encrypted category/tag")
    retention: Literal["7_days", "until_delete", "vault"] = Field(
        ..., description="Memory dial setting chosen by user"
    )

class MemoryOut(BaseModel):
    id: str
    encrypted_data: str
    encrypted_category: Optional[str]
    retention: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MemoryDelete(BaseModel):
    """For crypto-delete: client confirms key destruction on their side."""
    memory_id: str
    crypto_deleted: bool = Field(
        ..., description="Client confirms the local AES key for this item was destroyed"
    )

class PrivacyReceipt(BaseModel):
    """Returned after a sensitive session summarising all data actions."""
    stored_count: int = Field(0, description="Items saved to vault (user-approved)")
    deleted_count: int = Field(0, description="Messages user cleared")
    inference_location: Literal["on_device", "cloud"] = "cloud"
    encryption_key_holder: str = "this_device"
    shared_externally: bool = False
