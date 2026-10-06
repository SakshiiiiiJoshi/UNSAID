from fastapi import APIRouter, Depends

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    CheckInRequest,
    CheckInResponse,
    RehearsalSetup,
    RehearsalResponse,
)
from app.db.models.user import User
from app.api.dependencies import get_current_user
from app.services.llm_service import generate_chat_response

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat_interaction(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Main companion chat endpoint.
    Pipeline: Safety Router → Mode Selector → LLM → Response Policy → Reply
    """
    return await generate_chat_response(request)


@router.post("/checkin", response_model=CheckInResponse)
async def emotional_checkin(
    checkin: CheckInRequest,
    current_user: User = Depends(get_current_user),
):
    """
    10-20 second emotional check-in.
    Measures current state — never produces diagnostic labels.
    """
    from datetime import datetime, timezone
    import uuid

    # TODO: persist check-in to DB for pattern tracking
    return CheckInResponse(
        id=str(uuid.uuid4()),
        mind=checkin.mind,
        body=checkin.body,
        need=checkin.need,
        safety=checkin.safety,
        created_at=datetime.now(timezone.utc),
    )


@router.post("/rehearsal", response_model=RehearsalResponse)
async def conversation_rehearsal(
    setup: RehearsalSetup,
    current_user: User = Depends(get_current_user),
):
    """
    Conversation Gym — rehearse a difficult conversation.
    The AI simulates the other person with a visible 'simulation' label.
    """
    # TODO: use LLM to generate a realistic simulated reply
    return RehearsalResponse(
        simulated_reply=(
            f"[Simulation — {setup.person}] "
            f"I understand you want to talk about this. Tell me more."
        ),
        what_i_can_control=[
            "How I phrase my message",
            "When I choose to have this conversation",
            "Setting my own boundaries",
        ],
        what_i_cannot_control=[
            "Their emotional reaction",
            "Whether they agree with me",
            "How they interpret my words",
        ],
    )
