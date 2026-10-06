from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime


# --- Safety levels from safety.md ---
SafetyLevel = Literal["low", "elevated", "urgent"]

# --- Companion modes from blueprint.md ---
CompanionMode = Literal[
    "soft", "straight", "coach", "fire",
    "sarcastic_light", "quiet", "rehearsal"
]


class ChatMessage(BaseModel):
    """A single message in the conversation."""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Incoming chat request from the client."""
    message: str = Field(..., min_length=1, max_length=5000)
    mode: CompanionMode = Field("soft", description="Active companion personality")
    tone_intensity: int = Field(3, ge=1, le=5, description="1=gentle, 5=direct")
    conversation_history: List[ChatMessage] = Field(
        default_factory=list,
        description="Recent messages for context (client-managed, not server-stored)"
    )
    remember_session: bool = Field(
        True, description="False = 'Do not remember this chat' toggle"
    )


class SafetyClassification(BaseModel):
    """Output of the safety router — evaluated before every response."""
    level: SafetyLevel
    triggered_flags: List[str] = Field(default_factory=list)
    override_mode: Optional[CompanionMode] = Field(
        None, description="If urgent → forced to 'soft' Safe Mode"
    )
    show_crisis_bridge: bool = False


class ChatResponse(BaseModel):
    """Response returned to the client."""
    reply: str
    mode_used: CompanionMode
    safety: SafetyClassification
    privacy_receipt: Optional[dict] = Field(
        None, description="Populated after sensitive sessions"
    )


# --- Check-in (from blueprint section 4.2) ---

class CheckInRequest(BaseModel):
    """10-20 second emotional check-in. Measures state, not identity."""
    mind: Literal["heavy", "restless", "numb", "okay"]
    body: Literal["tight", "shaky", "nauseous", "tired", "okay"]
    need: Literal["comfort", "clarity", "action", "company", "space"]
    safety: Literal["safe", "unsure", "unsafe"]
    note: Optional[str] = Field(None, max_length=500, description="Optional free text")

class CheckInResponse(BaseModel):
    id: str
    mind: str
    body: str
    need: str
    safety: str
    created_at: datetime


# --- Rehearsal (Conversation Gym from features.md) ---

class RehearsalSetup(BaseModel):
    """Setup for the Conversation Gym / Rehearsal mode."""
    person: str = Field(..., description="e.g. friend, parent, professor, partner")
    goal: str = Field(..., description="What the user wants to achieve")
    emotional_intensity: int = Field(3, ge=1, le=5)
    feared_response: Optional[str] = Field(
        None, description="What they fear the other person will say"
    )

class RehearsalResponse(BaseModel):
    simulated_reply: str
    what_i_can_control: List[str]
    what_i_cannot_control: List[str]
