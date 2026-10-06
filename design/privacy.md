# UNSAID – Privacy, Encryption & Data Architecture

> Source: `docs/UNSAID_privacy_first_mental_health_app_blueprint.docx`

---

## Privacy Philosophy

> Privacy is **visible**, not buried in policy text.

UNSAID treats privacy as a **product feature**, not a legal checkbox. Every data action is surfaced to the user in plain language, in the moment it happens.

---

## Memory Architecture

### Memory Dial (Per-sentence control)
Every piece of content that could become a long-term memory is **user-controlled** at capture time:

| Setting | Behaviour |
|---|---|
| **Never remember** | Processed in-session only; not persisted anywhere |
| **Remember for 7 days** | Stored with a TTL; auto-deleted after 7 days |
| **Remember until I delete it** | Persisted in vault; user must explicitly delete |
| **Save to my vault** | Explicitly approved, categorised, editable |

> **Engineering rule:** No automatic persistent memory without a user-visible approval step.

### Memory Vault
- All persisted memories live in the **Memory Vault**
- User can **approve / edit / delete** any item
- Items are categorised for browsability
- No silent storage — ever

---

## Privacy Receipt

After every sensitive session, the app shows a **Privacy Receipt**:

```
Session summary — [date/time]
─────────────────────────────
✓ Stored to vault:      2 items (user-approved)
✓ Deleted:              1 message (you cleared it)
✓ Inference location:   On-device  /  Cloud (model: X)
✓ Encryption key:       Held on this device
✗ Shared externally:    Nothing
─────────────────────────────
View full data log →
```

---

## Encryption & Key Management

- **Client-Side Symmetric Encryption (AES-GCM-256)** — The user's device generates a master symmetric key. When saving a memory, the device encrypts the text *before* sending it to the backend. The server database only stores ciphertext and never holds the decryption keys by default.
- **Multi-Device Sync (Asymmetric Encryption)** — If a user has multiple devices, they generate public/private key pairs (e.g., Elliptic Curve). Devices securely exchange the Vault's symmetric master key by encrypting it with the other device's public key, preventing the server from learning the key.
- **In-Session Transport (TLS 1.3)** — Active chat connections are encrypted in transit. The server temporarily decrypts messages in-memory to send to the cloud LLM, then immediately drops them (unless using on-device inference where messages never leave the device).
- Voice audio transcribed locally; raw audio **deleted immediately** by default.
- Exported content delivered as an **encrypted package** controlled by the user.
- One-tap **crypto-delete**: cryptographic master key discarded from the device, rendering all server data instantly unrecoverable.

---

## Data Retention

| Data type | Default retention | User control |
|---|---|---|
| In-session messages (no-memory mode) | Deleted at session end | Always |
| Vault memories | Until user deletes | Full edit/delete |
| Check-in history | Until user deletes | Can disable entirely |
| Voice audio | Deleted immediately after transcription | Can keep locally |
| Analytics events | Aggregate only; no content | Opt-out available |

---

## What Analytics May NOT Contain

> **Hard engineering rule:** Analytics events must contain **zero** of the following:
- Message text
- Audio content
- Memory text
- Raw emotional content
- Any PII derived from conversations

Permitted analytics: feature interaction counts, session duration (bucketed), error rates, UI events.

---

## Threat Model

| Threat | Mitigation |
|---|---|
| Server breach | Vault content encrypted with device-held keys; server holds ciphertext only |
| Device theft | App lock + biometric; keys tied to device secure enclave |
| Silent memory accumulation | No memory stored without explicit user action |
| Inference data leakage | On-device inference where feasible; cloud inference disclosed in Privacy Receipt |
| Analytics re-identification | No content in events; no session-level PII |
| Third-party SDK leakage | Audit all SDKs for data exfiltration; no third-party analytics in sensitive flows |

---

## Regulatory Compliance

### India — DPDP (Digital Personal Data Protection Act)
- Data minimisation by design
- Explicit, informed consent for each data category
- User right to access, correct, and erase personal data
- Grievance redressal mechanism required
- Data fiduciary obligations documented

### SaMD (Software as a Medical Device)
- Product is framed as a self-help companion, **not** a clinical tool
- If features cross into diagnostic/treatment territory, SaMD classification may apply
- Legal review required before launch if clinical claims are made

---

## Privacy UI Rules (from UI/UX Masterplan)

| Anti-pattern | Why wrong | Replacement |
|---|---|---|
| Silent AI memory | User assumes privacy they don't have | Memory Vault with explicit approval |
| Hidden data defaults | User can't find privacy settings | Transparent settings, surfaced in onboarding |
| Paywall before safety resources | Exploitative | No gate on crisis or escalation content |

---

## Engineering Acceptance Criteria

| Rule | Pass criteria |
|---|---|
| No content logging | Analytics events contain no message text, audio, memory, or raw emotional content |
| Every memory is user-controlled | No automatic persistent memory without user-visible approval step |
| Device-held keys | Server cannot decrypt vault content independently |
| Crypto-delete works | After crypto-delete, data is unrecoverable even from server backups |
| Privacy Receipt shown | After every sensitive session, receipt is displayed and accessible in history |
