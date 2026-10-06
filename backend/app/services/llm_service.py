"""
LLM Service — Orchestrates the companion personality engine and safety router.

Architecture:
    User message → Safety Router → Mode Selector → LLM Call → Response Policy → Reply

Key rules from the blueprint:
  - Personality changes delivery style only, never safety policy or factual content.
  - If safety level is urgent → enter Safe Mode regardless of chosen personality.
  - Sarcastic-Light is auto-disabled for grief, trauma, self-harm, abuse, or medical risk.
"""

from typing import List

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ChatMessage,
    SafetyClassification,
    CompanionMode,
)


# ---------------------------------------------------------------------------
# Safety Router
# ---------------------------------------------------------------------------

URGENT_KEYWORDS = [
    "kill myself", "want to die", "suicide", "self-harm",
    "end my life", "hurt myself", "not worth living",
]

ELEVATED_KEYWORDS = [
    "panic", "can't breathe", "heart racing", "chest pain",
    "dissociate", "numb", "blank", "overwhelmed", "hopeless",
]

SARCASM_BLOCKED_CONTEXTS = {"grief", "trauma", "self_harm", "abuse", "medical_risk"}


def classify_safety(message: str) -> SafetyClassification:
    """
    Classify user message into safety levels.
    Production version should use a fine-tuned classifier model.
    """
    lower = message.lower()

    # Urgent — crisis bridge
    for kw in URGENT_KEYWORDS:
        if kw in lower:
            return SafetyClassification(
                level="urgent",
                triggered_flags=[kw],
                override_mode="soft",
                show_crisis_bridge=True,
            )

    # Elevated — restricted personality
    flags = [kw for kw in ELEVATED_KEYWORDS if kw in lower]
    if flags:
        return SafetyClassification(
            level="elevated",
            triggered_flags=flags,
            override_mode=None,
            show_crisis_bridge=False,
        )

    return SafetyClassification(level="low")


# ---------------------------------------------------------------------------
# Mode Selector
# ---------------------------------------------------------------------------

def resolve_mode(requested: CompanionMode, safety: SafetyClassification) -> CompanionMode:
    """Apply safety overrides to the companion mode."""
    # Urgent → force Safe Mode (soft)
    if safety.level == "urgent":
        return "soft"

    # Sarcastic-Light disabled for elevated contexts
    if requested == "sarcastic_light" and safety.level == "elevated":
        return "soft"

    return requested


# ---------------------------------------------------------------------------
# System Prompts per Mode
# ---------------------------------------------------------------------------

MODE_SYSTEM_PROMPTS: dict[CompanionMode, str] = {
    "soft": (
        "You are UNSAID, a warm and gentle mental-health companion. "
        "Speak in a low-pressure, caring tone. No false promises or overclaiming."
    ),
    "straight": (
        "You are UNSAID, a direct and concise companion. "
        "Get to the point without being harsh or judgmental."
    ),
    "coach": (
        "You are UNSAID, an action-focused, structured, energetic companion. "
        "Help the user get unstuck. Never use coercive 'you must' language."
    ),
    "fire": (
        "You are UNSAID, an assertive companion that validates the user's anger "
        "without feeding it. Never insult, threaten, encourage revenge, or escalate."
    ),
    "sarcastic_light": (
        "You are UNSAID, using light humour and playful phrasing. "
        "Only for low-risk everyday frustration."
    ),
    "quiet": (
        "You are UNSAID in Quiet Companion mode. Use minimal words, one prompt at a time, "
        "grounding first. No interrogation."
    ),
    "rehearsal": (
        "You are UNSAID in Rehearsal Partner mode. Role-play as the person the user "
        "chooses. Always clearly label this as a simulation."
    ),
}

SAFE_MODE_PREAMBLE = (
    "The user may be in distress. Respond with calm, grounding language. "
    "Present human support routes. Do not alarm or escalate. "
    "Do not discuss methods of self-harm. Prioritise safety above all."
)


# ---------------------------------------------------------------------------
# LLM Call (placeholder — swap for real provider)
# ---------------------------------------------------------------------------

async def call_llm(
    system_prompt: str,
    messages: List[ChatMessage],
    user_message: str,
) -> str:
    """
    Placeholder for the actual LLM call.
    Replace with OpenAI / Gemini / local model integration.
    """
    # TODO: integrate with real LLM provider
    return (
        f"[LLM placeholder] I hear you. "
        f"(mode context: {system_prompt[:40]}…)"
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def generate_chat_response(request: ChatRequest) -> ChatResponse:
    """Full pipeline: safety → mode → LLM → response."""

    # 1. Safety classification
    safety = classify_safety(request.message)

    # 2. Resolve effective mode
    effective_mode = resolve_mode(request.mode, safety)

    # 3. Build system prompt
    system_prompt = MODE_SYSTEM_PROMPTS[effective_mode]
    if safety.level == "urgent":
        system_prompt = f"{SAFE_MODE_PREAMBLE}\n\n{system_prompt}"

    # 4. Call LLM
    reply = await call_llm(system_prompt, request.conversation_history, request.message)

    # 5. Build response
    return ChatResponse(
        reply=reply,
        mode_used=effective_mode,
        safety=safety,
    )
