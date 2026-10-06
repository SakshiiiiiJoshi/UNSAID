"""
Memory Vault Service — CRUD for encrypted memories.

The server NEVER decrypts data. It stores and returns ciphertext only.
Encryption/decryption is the client's responsibility using AES-GCM-256 keys
held on the user's device.
"""

from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

from app.db.models.memory import Memory
from app.schemas.memory import MemoryCreate, MemoryOut, PrivacyReceipt


def create_memory(db: Session, memory_in: MemoryCreate, owner_id: str) -> Memory:
    """Store a new encrypted memory."""
    db_memory = Memory(
        encrypted_data=memory_in.encrypted_data,
        encrypted_category=memory_in.encrypted_category,
        owner_id=owner_id,
    )
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory


def get_memories(db: Session, owner_id: str, skip: int = 0, limit: int = 50) -> list[Memory]:
    """Return all encrypted memories for a user (server returns ciphertext)."""
    return (
        db.query(Memory)
        .filter(Memory.owner_id == owner_id)
        .order_by(Memory.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_memory(db: Session, memory_id: str, owner_id: str) -> Memory | None:
    """Get a single memory, scoped to the owner."""
    return (
        db.query(Memory)
        .filter(Memory.id == memory_id, Memory.owner_id == owner_id)
        .first()
    )


def delete_memory(db: Session, memory_id: str, owner_id: str) -> bool:
    """
    Delete memory from the database.
    The client should also destroy the local AES key (crypto-delete)
    so even server backups become unrecoverable.
    """
    memory = get_memory(db, memory_id, owner_id)
    if not memory:
        return False
    db.delete(memory)
    db.commit()
    return True


def purge_expired_memories(db: Session) -> int:
    """
    Delete memories past their 7-day TTL.
    Should be called by a scheduled background task.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    count = (
        db.query(Memory)
        .filter(Memory.created_at < cutoff)
        .delete(synchronize_session="fetch")
    )
    db.commit()
    return count


def build_privacy_receipt(stored: int = 0, deleted: int = 0) -> PrivacyReceipt:
    """Generate a Privacy Receipt for the end of a sensitive session."""
    return PrivacyReceipt(
        stored_count=stored,
        deleted_count=deleted,
        inference_location="cloud",
        encryption_key_holder="this_device",
        shared_externally=False,
    )
