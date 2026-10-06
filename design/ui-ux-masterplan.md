# UNSAID – UI/UX Masterplan

> Source: `docs/UNSAID_UI_UX_MASTERPLAN_WEB_MOBILE_v2_PERSONALITY_MODES.docx`

---

## Core UX Identity

> UNSAID is a **responsive emotional workspace** — a calm room that changes shape around the user's immediate need, remembers only what the user permits, and can move from conversation to practical help without breaking the emotional thread.

**Not:** "AI therapist with a pretty interface."

### Product Test
> Show the same product to someone who is calm and someone who is overwhelmed. If the overwhelmed user sees the same density, the same number of options, and the same motion — the adaptive design is not working.

---

## Screen Architecture

### Home — Quiet Room
| User feels | Engineer builds |
|---|---|
| "I can enter without performing." | Minimal home with state orb + three actions |

**Must-have:** Need-based actions, privacy state, nav  
**Nice-to-have:** Ambient orb  
**Never:** Mood score / streak pressure

---

### Chat — Conversation Thread
| User feels | Engineer builds |
|---|---|
| "I can talk without figuring out the perfect prompt." | Chat + intent + mode + privacy + composer + contextual quick actions |

**Must-have:** Intent, mode, privacy, composer  
**Nice-to-have:** Context rail  
**Never:** Infinite tool clutter

---

### Blank Mode
| User feels | Engineer builds |
|---|---|
| "Not knowing what to say is supported." | Prompt deck + low-input paths + stay-with-me mode |

**Must-have:** Prompt choices, "stay" option  
**Nice-to-have:** Voice  
**Never:** Open-ended wall of questions

---

### Help Now
| User feels | Engineer builds |
|---|---|
| "I can get grounded and find a human fast." | Grounding tools + human support route |

**Must-have:** Grounding + human support route  
**Nice-to-have:** Haptics  
**Never:** Alarmist animation

---

### Check-in
| User feels | Engineer builds |
|---|---|
| "I can log how I feel quickly and honestly." | State + emotion + context capture |

**Must-have:** State + emotion + context  
**Nice-to-have:** Body map  
**Never:** Diagnosis language

---

### Rehearsal Stage
| User feels | Engineer builds |
|---|---|
| "I can practice before I face the person." | Role-play engine + coach pause + exportable phrasing |

**Must-have:** Role-play engine, coach pause  
**Nice-to-have:** Exportable phrasing  
**Never:** Impersonating a real person deceptively

---

### Pattern Weather
| User feels | Engineer builds |
|---|---|
| "I can notice myself without being scored." | Evidence-linked pattern cards, descriptive language |

**Must-have:** Evidence-linked insight  
**Nice-to-have:** Filters  
**Never:** Causal certainty claims

---

### Memory Vault
| User feels | Engineer builds |
|---|---|
| "The AI does not own my history." | Explicit memory approval + delete/edit controls |

**Must-have:** Approve / edit / delete  
**Nice-to-have:** Categories  
**Never:** Silent storage

---

### Settings
| User feels | Engineer builds |
|---|---|
| "I can control everything." | Privacy / notifications / accessibility controls |

**Must-have:** Privacy / notifications / accessibility  
**Nice-to-have:** Theme customisation  
**Never:** Hidden defaults

---

## Design System

### Design Tokens
- Shared semantic token names across **web and mobile** (no duplicated hex values)
- Token sheet covers: colour, typography, spacing, radius, shadow, motion, breakpoints

### Typography
- Modern typeface (e.g. Inter, Outfit, or similar Google Font)
- Clear type hierarchy: Display → Heading → Body → Caption → Label
- Minimum body size: 16px / 1rem

### Motion
- All motion is **optional** — Reduce Motion / system settings honoured
- Static alternatives exist for every animated element
- No motion used in crisis or Help Now surfaces
- No fake human typing delays (manipulative)

### Colour
- Avoid generic alert colours (e.g. pure red for crisis — raises arousal)
- Calm, high-contrast palette for safety surfaces
- Dark mode first
- Sufficient contrast for WCAG 2.2 AA across all text sizes

### Spacing & Layout
- Responsive grid (web + mobile)
- **One primary action per screen** — ≤ 3 visible primary choices in critical flows
- Every interactive element: minimum touch target 44×44pt (Apple HIG) / 48dp (Android)

### Accessibility
- WCAG 2.2 compliance
- Focus order, labels, contrast, target size, motion all checked
- Every gesture has a **fallback** — no core feature depends on swipe, long press, or multi-finger

---

## Anti-Patterns Banned from UNSAID

| Anti-pattern | Why it is wrong | Replacement |
|---|---|---|
| Mood score out of 100 | Looks clinical; users chase a number | Descriptive state + patterns |
| Streaks for emotional check-ins | Converts care into compliance or guilt | Gentle routines with no loss framing |
| Infinite wellness feed | Increases browsing and cognitive load | Contextual tool recommendations |
| Fake human typing delays | Manipulative and theatrical | Transparent streaming / response state |
| Overly cute mascot everywhere | Feels childish to older young adults | Mature, abstract visual companion system |
| Red crisis animations | Raises arousal | Calm high-contrast safety surface |
| Dark pattern subscription prompts | Inappropriate in vulnerable moments | Transparent pricing; no paywall before safety |
| Silent AI memory | User assumes privacy they don't have | Memory Vault with explicit approval |

---

## Core UX Metrics

| Metric | What it measures |
|---|---|
| Time-to-first-useful-action | Speed from open → value |
| Blank-mode completion rate | Low-energy experience success |
| Users who correctly understand privacy mode | Privacy comprehension |
| Tool abandonment rate | UX friction |
| Notification opt-in and disable rates | Notification design quality |
| Rehearsal completion and export/save rate | Differentiating feature engagement |
| Accessibility task completion | Inclusion quality |
| Clicks before reaching intended support action | Navigation efficiency |

---

## 8-Week UI Build Roadmap

| Week | Focus | Deliverable |
|---|---|---|
| **1** | Design tokens + Figma foundation + responsive grid | Token sheet + navigation + typography |
| **2** | Quiet Room + onboarding + privacy choice | Clickable first-run prototype |
| **3** | Conversation Thread + modes + composer | Realistic chat shell with adaptive quick actions |
| **4** | Blank Mode + Help Now + tool sheets | Core "low-energy" experience |
| **5** | Check-in + emotion map + body/context capture | Fast check-in loop |
| **6** | Rehearsal + Patterns + Memory Vault | Differentiating feature layer |
| **7** | Accessibility + motion + privacy UI + notification settings | Production-quality interaction pass |
| **8** | Usability tests + polish + responsive/mobile QA | Release candidate UI kit + component library |

### Build Rules
- ❌ Do not build every tool before core flows work
- ❌ Do not start with animation
- ❌ Do not build an analytics dashboard before privacy and safety surfaces are stable

---

## Engineering Acceptance Criteria (Full)

| Rule | Pass criteria |
|---|---|
| Design tokens are shared | Web and mobile use same semantic token names — no duplicated hex values |
| No content logging | Analytics events contain no message text, audio, memory text, or raw emotional content |
| One action per screen | Critical flows completable with ≤ 3 primary visible choices |
| Every gesture has a fallback | No core feature depends on swipe, long press, or multi-finger interaction |
| Every insight has evidence | Pattern cards link to entries/context used to generate them |
| Every memory is user-controlled | No automatic persistent memory without user-visible approval step |
| Safety can interrupt personality | Crisis/safety UI can override selected tone/personality |
| Motion is optional | Reduce Motion / system settings honoured; static alternatives exist |

---

## References

- Apple Human Interface Guidelines — Accessibility, Motion, Layout
- Android Developers — Accessibility / touch targets, Adaptive App Quality Tier 2
- W3C — WCAG 2.2
- Competitor patterns reviewed: Wysa, How We Feel, Finch, Daylio

> Note: Competitor references are used only to identify interaction patterns. UNSAID should create **original** visual assets, copy, illustrations, and interaction details.
