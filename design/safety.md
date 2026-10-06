# UNSAID – Safety Architecture & Crisis Handling

> Source: `docs/UNSAID_privacy_first_mental_health_app_blueprint.docx`

---

## Core Safety Principles

- Safety is **non-negotiable** — it overrides all personality modes, design choices, and user preferences
- The app is a companion, not a clinical tool — it **bridges to real help**, it does not replace it
- Safety surfaces are **never paywalled**

---

## Safety Levels & Safe Mode

The system operates with **graduated safety levels**. When urgency is detected:

1. All personality/mode selection is overridden
2. App enters **Safe Mode** — warm, direct, non-alarming
3. Crisis/safety UI takes full priority over all other surfaces

> **Engineering rule:** Safety can interrupt personality. Crisis/safety UI can override the selected tone at any time.

---

## Safety Router

A clinically governed **safety router** processes every interaction:

```
User input
    ↓
Safety/risk classification
    ↓
[Low risk] → Normal response pipeline → Personality mode applied
    ↓
[Elevated risk] → Safe operating envelope → Restricted personality
    ↓
[Urgent/crisis] → Safe Mode → Crisis bridge activated
```

---

## Crisis Bridge

When urgent risk is detected:
- Immediate pivot to calm, grounding language
- **Human support route** presented prominently
- No alarmist animations or red-flashing UI (raises arousal)
- Calm, high-contrast safety surface
- India-specific crisis resources linked

### India-Specific Resources
*(To be populated with verified numbers — iCall, Vandrevala Foundation, NIMHANS helpline, etc.)*

---

## Medical Symptom Handling

When users report physical symptoms that may overlap with panic (racing heart, nausea, shaking, chest discomfort, dizziness):

1. **Safety/medical screen first** — do not assume a psychological cause
2. Avoid diagnosing or naming a condition
3. If appropriate: calm, non-diagnostic explanation
4. Grounding offered, **not forced**
5. Clear prompt to seek medical attention if indicated

> NICE guidance: physical problems should be excluded when people present with panic-like symptoms.

---

## Trauma Handling

The app **does not** perform:
- Trauma processing
- Exposure therapy simulation
- EMDR simulation
- "Memory recovery"

When a user asks *"How do I forget what happened?"*:
> Reframe toward reducing distress/impairment, restoring safety and agency, and seeking trauma-focused professional care where indicated. NICE recommends trauma-focused CBT for clinically important PTSD symptoms in young people.

---

## Self-Harm & Suicide Safety

- Detected via response policy layer on LLM output
- Safe Mode triggered immediately
- Crisis bridge presented with calm, non-alarming UI
- No graphic or detailed discussion of methods
- Sarcastic-Light mode automatically disabled

---

## Anti-Dependency Guardrails

The app actively prevents over-reliance:
- Surfaces real-world connection prompts
- Celebrates actions taken *outside* the app
- Clear professional referral pathways always visible
- No feature encourages excessive daily use

---

## UI Safety Rules (from UI/UX Masterplan)

| Anti-pattern | Why dangerous | Replacement |
|---|---|---|
| Red crisis animations | Raises arousal, can worsen panic | Calm high-contrast safety surface |
| Alarmist copy | Increases fear response | Warm, grounding language |
| Dark pattern subscription prompts in crisis moments | Exploitative | No paywall before safety resources |
| Hidden escalation paths | User can't find help | Help Now always ≤ 2 taps away |

---

## Red-Team Safety Testing

Every personality mode must pass the **same red-team safety suite**:
- Self-harm scenarios
- Suicidal ideation scenarios
- Medical emergency scenarios
- Abuse / safeguarding scenarios
- Trauma disclosure scenarios

A safety tabletop review (clinician + safety reviewer + engineer) must verify each high-risk path produces the intended UI state.

---

## Engineering Acceptance Criteria

| Rule | Pass criteria |
|---|---|
| Safety interrupts personality | Crisis/safety UI overrides selected tone at all times |
| No content logging | Analytics events contain zero message text, audio, memory text, or raw emotional content |
| Help Now reachability | User reaches crisis support in ≤ 3 taps from any screen |
| Every insight has evidence | Pattern cards link to source entries — no invented observations |
