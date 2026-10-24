from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import uuid
from datetime import datetime, timezone

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
from app.services.llm_service import (
    generate_chat_response,
    stream_llm,
    classify_safety,
    resolve_mode,
    MODE_SYSTEM_PROMPTS,
    SAFE_MODE_PREAMBLE,
    UNIVERSAL_GUARDRAIL,
)

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat_interaction(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Main companion chat endpoint.
    Pipeline: Safety Router → Mode Selector → Gemini LLM → Response Policy → Reply

    Privacy: store=False — Gemini does not store or train on this conversation.
    The client must show a "Cloud AI used for this reply" label per the privacy architecture.
    """
    return await generate_chat_response(request)


@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Streaming companion chat — returns Server-Sent Events.
    Suitable for real-time typing-style UI where the reply builds incrementally.

    Privacy: same guarantee as /chat — store=False, no training.
    """
    safety = classify_safety(request.message)
    effective_mode = resolve_mode(request.mode, safety)

    system_prompt = MODE_SYSTEM_PROMPTS[effective_mode]
    if safety.level == "urgent":
        system_prompt = SAFE_MODE_PREAMBLE + system_prompt

    history = request.conversation_history if request.remember_session else []

    async def event_generator():
        async for chunk in stream_llm(system_prompt, history, request.message):
            # SSE format
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )


@router.post("/checkin", response_model=CheckInResponse)
async def emotional_checkin(
    checkin: CheckInRequest,
    current_user: User = Depends(get_current_user),
):
    """
    10-20 second emotional check-in.
    Measures current state — never produces diagnostic labels.

    TODO: persist check-in to DB for weekly pattern tracking.
    """
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
    The AI simulates the other person with a visible '[Simulation]' label.

    Privacy: store=False — Gemini does not retain this.
    """
    # Build a tailored rehearsal prompt
    intensity_desc = {1: "very calm", 2: "calm", 3: "neutral", 4: "defensive", 5: "emotionally heightened"}
    intensity_label = intensity_desc.get(setup.emotional_intensity, "neutral")

    rehearsal_system = (
        f"You are simulating {setup.person} in a difficult conversation. "
        f"The user's goal is: {setup.goal}. "
        f"Emotional intensity: {intensity_label} (1=calm, 5=intense). "
        f"Always start your reply with '[Simulation — {setup.person}]'. "
        f"Never break character to give advice. Stay realistic but not cruel."
    )
    if setup.feared_response:
        rehearsal_system += (
            f" The user fears you might say: '{setup.feared_response}'. "
            f"You may or may not say something like this — be realistic, not predictable."
        )

    # One opening line from the simulated person
    from app.services.llm_service import _client, COMPANION_MODEL
    from google.genai import errors as genai_errors

    simulated_reply = f"[Simulation — {setup.person}] Hey, what did you want to talk about?"

    if _client is not None:
        try:
            interaction = _client.interactions.create(
                model=COMPANION_MODEL,
                system_instruction=rehearsal_system + UNIVERSAL_GUARDRAIL,
                input=(
                    f"Open the conversation as {setup.person}. "
                    f"Give one realistic opening response (2-3 sentences max)."
                ),
                store=False,
            )
            simulated_reply = interaction.output_text or simulated_reply
        except genai_errors.APIError:
            pass  # fall back to default

    return RehearsalResponse(
        simulated_reply=simulated_reply,
        what_i_can_control=[
            "How I phrase my opening",
            "When and where I have this conversation",
            "How I respond to their reaction",
            "Whether I continue or pause the conversation",
            "Setting and holding my own boundaries",
        ],
        what_i_cannot_control=[
            "Their emotional reaction",
            "Whether they agree with me",
            "How they interpret my words",
            "What they choose to do with what I say",
        ],
    )
