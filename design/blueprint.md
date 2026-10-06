# UNSAID – Product & Technical Blueprint

> Prepared: 4 October 2026  
> Source: `docs/UNSAID_privacy_first_mental_health_app_blueprint.docx`

---

## 1. Executive Summary

UNSAID is a **web + mobile mental-health support platform** for teenagers and young adults. It is deliberately framed as an **evidence-informed companion and self-help system**, not an autonomous therapist or diagnostician.

The scientific backbone is **stepped care** and **structured psychological skills**, aligned with NICE guidance:
- Digital CBT and psychological approaches for mild adolescent depression
- CBT-based self-help for anxiety and panic disorder
- Trauma-focused CBT under appropriate professional care

### Three Core Differentiators
1. **User-controlled encrypted Memory Vault** — no silent psychological profiling
2. **Mode-based companion** — personality changes tone, never safety rules
3. **Blank Mode / Conversation Rehearsal** — turns mental blankness into concrete language and practice

---

## 2. Product Vision & User Problem

### Target Users
Teenagers and young adults experiencing:
- Anxiety and panic-like episodes
- Low mood and emotional overload
- Difficulty expressing themselves / "going blank"
- Dissociation-like experiences
- Rumination and intrusive thoughts
- Relationship stress, loneliness
- Academic pressure
- Unresolved distress

### Working Thesis
> Young people often need a low-friction place to put the thing they cannot say out loud.

---

## 3. Product Principles

| Principle | Meaning |
|---|---|
| Not a therapist | Evidence-informed companion, never diagnostician |
| North star | Make users more capable outside the app — not more dependent |
| Safety first | Clinical safety router overrides all personality modes |
| Privacy visible | Privacy receipts shown to user, not buried in policy text |
| Anti-dependency | Guardrails prevent over-reliance on the app |

---

## 4. Evidence-Informed Therapeutic Backbone

### 4.1 Therapy Modalities

| Approach | UNSAID can safely implement | Hard boundary |
|---|---|---|
| CBT | Thought-feeling-behaviour links; reframing; behavioural experiments; coping plans | Don't present a single interpretation as truth |
| Behavioural Activation | Tiny, scheduled, value-linked activities; energy vs action planning | Don't prescribe rigid routines as medical treatment |
| DBT-informed | Distress tolerance, emotion naming, grounding, interpersonal effectiveness, urge surfing | Skills education only — not a full DBT programme |
| ACT-informed | Values clarification; defusion language; acceptance of internal experience | Never tell users to "accept" serious danger or abuse |
| Mindfulness / Grounding | Attention anchoring, sensory grounding, breath/relaxation, present-moment orientation | Don't force during every crisis — some find body focus distressing |
| Interpersonal approaches | Communication rehearsal, boundary language, conflict prep, repair attempts | Don't act as judge in interpersonal disputes |
| Trauma-informed | Psychoeducation, grounding, stabilisation, safety planning, professional referral | Never do trauma processing, exposure, EMDR simulation, or "memory recovery" |

> **Trauma distinction:** If user asks "How do I forget what happened?" — reframe toward *reducing distress/impairment*, restoring safety and agency, and seeking trauma-focused professional care where indicated. NICE recommends trauma-focused CBT for clinically important PTSD symptoms in young people.

### 4.2 Check-ins: Measure State, Not Diagnose Identity

Short check-ins collect current experience, not diagnostic labels.

| Dimension | Example states |
|---|---|
| Mind | Heavy / Restless / Numb / Okay |
| Body | Tight / Shaky / Nauseous / Tired / Okay |
| Need | Comfort / Clarity / Action / Company / Space |
| Safety | I feel safe / Unsure / Unsafe |

Trends shown back as **patterns**, not diagnoses. Validated questionnaires only after clinician/legal review.

---

## 5. Companion Modes & Personalities

> Personality changes **delivery style only** — never the safety policy, evidence base, or factual content.

| Mode | Voice | Good for | Hard safety rule |
|---|---|---|---|
| Soft / Safe | Warm, gentle, low-pressure | Panic, sadness, shame, late-night overwhelm | No false promises or overclaiming |
| Straight | Direct, concise, practical | Tired of long explanations | Never becomes harsh or judgmental |
| Coach | Action-focused, structured, energetic | Study stress, routines, avoidance, getting unstuck | No coercive "you must" language |
| Fire / Protective | Assertive, validates anger without feeding it | Bullying, disrespect, breakup anger, boundary-setting | Never insults, threatens, encourages revenge, or escalates |
| Sarcastic-Light | Light humour, playful phrasing | Low-risk everyday frustration | Auto-disabled for grief, trauma, self-harm, abuse, or medical risk |
| Quiet Companion | Minimal words, one prompt at a time, grounding first | Blank mind, panic, sensory overload | No interrogation |
| Rehearsal Partner | Role-play of another person; user chooses difficulty | Hard conversations, communication practice | Clearly labelled simulation; never impersonates real people deceptively |

### Personality Engine Rules
1. Detect emotional/safety context first → select safe operating envelope → then select style
2. If safety level is **urgent** → enter **Safe Mode** regardless of chosen personality
3. Store preferred style as a preference, not a therapeutic trait
4. Keep a "tone intensity" slider separate from emotional mode (e.g. "gentle but direct")
5. Test every persona against the same red-team safety suite

---

## 6. User Experience & App Screens

See [ui-ux-masterplan.md](./ui-ux-masterplan.md) for full screen specifications.

---

## 7. Tech Stack

- **Frontend:** Web + Mobile (responsive)
- **Backend:** API layer with LLM + RAG pipeline
- **AI/Memory:** Response policy layer; user-controlled memory; no silent persistence

See [privacy.md](./privacy.md) for encryption and data architecture.

---

## 8. Roadmap

Phased build — see [ui-ux-masterplan.md](./ui-ux-masterplan.md) for the 8-week UI roadmap.

**Overall build order:**
1. Tokens → 2. Primitives → 3. Quiet Room → 4. Chat → 5. Blank Mode → 6. Help Now → 7. Check-in → 8. Rehearsal → 9. Patterns → 10. Memory/Privacy → 11. Responsive polish → 12. Accessibility + test suite

---

## 9. Regulatory Considerations

- India **DPDP (Digital Personal Data Protection)** framework compliance
- Possible **SaMD (Software as a Medical Device)** implications reviewed
- NICE guidance alignment documented throughout

---

## References

1. NICE — Digital CBT / stepped care for mild adolescent depression
2. NICE — CBT-based self-help for anxiety
3. NICE — CBT for panic disorder; physical problems should be excluded for panic-like symptoms
4. NICE — Trauma-focused CBT for young people with PTSD symptoms
5. WHO — Towards Responsible AI for Mental Health and Well-being (March 2026)
6. NIMH — Teen Depression, GAD, Social Anxiety Disorder
7. Mayo Clinic — Panic attacks / physical symptoms
