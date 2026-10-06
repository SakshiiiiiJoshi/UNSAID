from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# --- Registration & Auth ---

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: str
    username: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


# --- Preferences ---

class UserPreferencesUpdate(BaseModel):
    """User-controlled settings like companion mode, tone intensity, etc."""
    preferred_mode: Optional[str] = Field(
        None,
        description="Companion mode: soft, straight, coach, fire, sarcastic_light, quiet, rehearsal"
    )
    tone_intensity: Optional[int] = Field(
        None, ge=1, le=5,
        description="1 = very gentle, 5 = very direct"
    )
