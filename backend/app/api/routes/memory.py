from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.memory import MemoryCreate, MemoryOut, MemoryDelete, PrivacyReceipt
from app.db.session import get_db
from app.db.models.user import User
from app.api.dependencies import get_current_user
from app.services.memory_vault import (
    create_memory,
    get_memories,
    get_memory,
    delete_memory,
    build_privacy_receipt,
)
from app.core.exceptions import MemoryNotFound

router = APIRouter()


@router.post("/", response_model=MemoryOut, status_code=201)
async def save_memory(
    memory_in: MemoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Store an encrypted memory in the vault.
    The server receives ciphertext only — it cannot read the content.
    """
    return create_memory(db, memory_in, current_user.id)


@router.get("/", response_model=List[MemoryOut])
async def list_memories(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return all encrypted memories for the authenticated user."""
    return get_memories(db, current_user.id, skip, limit)


@router.get("/{memory_id}", response_model=MemoryOut)
async def read_memory(
    memory_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Fetch a single encrypted memory by ID."""
    memory = get_memory(db, memory_id, current_user.id)
    if not memory:
        raise MemoryNotFound()
    return memory


@router.delete("/{memory_id}", status_code=204)
async def remove_memory(
    memory_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a memory (server-side).
    Client should also perform crypto-delete (destroy the local AES key).
    """
    if not delete_memory(db, memory_id, current_user.id):
        raise MemoryNotFound()


@router.get("/receipt/latest", response_model=PrivacyReceipt)
async def latest_privacy_receipt(
    current_user: User = Depends(get_current_user),
):
    """Return a Privacy Receipt for the most recent session."""
    # In production, this would aggregate real session data
    return build_privacy_receipt(stored=0, deleted=0)
