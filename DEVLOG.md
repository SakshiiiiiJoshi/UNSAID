# UNSAID — Dev Log & Technical Summary

> Last updated: 25 Oct 2026  
> Stack: FastAPI · PostgreSQL (asyncpg) · SQLAlchemy 2.0 async · Alembic · Gemini API (`google-genai`)

---

## What UNSAID Is

A **privacy-first mental health companion** for teenagers and young adults.  
Core principle: make users more capable *outside* the app — not more dependent on it.

---

## Project Structure

```
UNSAID/
├── README.md
├── DEVLOG.md                        ← this file
├── design/                          ← all product design docs (complete)
│   ├── blueprint.md                 ← product vision, therapeutic backbone, roadmap
│   ├── modes.md                     ← 7 companion personalities with safety rules
│   ├── features.md                  ← core features + 6 signature differentiators
│   ├── safety.md                    ← safety architecture, crisis escalation
│   ├── privacy.md                   ← encryption architecture, DPDP compliance
│   └── ui-ux-masterplan.md          ← screen specs, design system, 8-week roadmap
└── backend/
    ├── .env.example                 ← copy → .env, fill in keys
    ├── requirements.txt
    ├── Dockerfile
    ├── alembic.ini
    ├── alembic/
    │   ├── env.py                   ← async Alembic config, reads from app settings
    │   └── versions/
    │       └── 9107b52d5e53_initial_tables.py  ← users + memories tables
    └── app/
        ├── main.py                  ← FastAPI app, CORS, route registration
        ├── core/
        │   ├── config.py            ← Pydantic settings (reads .env)
        │   ├── security.py          ← bcrypt + JWT
        │   └── exceptions.py        ← custom HTTP exceptions
        ├── db/
        │   ├── session.py           ← async SQLAlchemy engine (asyncpg)
        │   └── models/
        │       ├── user.py          ← User model
        │       └── memory.py        ← Memory model (stores ciphertext only)
        ├── schemas/
        │   ├── chat.py              ← ChatRequest/Response, CheckIn, Rehearsal schemas
        │   ├── user.py              ← UserCreate, UserLogin, UserOut, Token
        │   └── memory.py            ← MemoryCreate, MemoryOut, PrivacyReceipt
        ├── api/
        │   ├── dependencies.py      ← get_current_user (JWT → async DB lookup)
        │   └── routes/
        │       ├── chat.py          ← /chat, /chat/stream, /checkin, /rehearsal
        │       ├── memory.py        ← Memory Vault CRUD + privacy receipt
        │       └── user.py          ← /register, /login, /me
        └── services/
            ├── llm_service.py       ← Gemini integration (real, with streaming)
            ├── memory_vault.py      ← async Memory Vault service
            └── rag_pipeline.py      ← empty (Phase 4)
```

---

## Session Log

### Session 1 — Design & Docs
- Created all 6 design documents in `/design/`
- Blueprint, modes, features, safety, privacy, UI/UX masterplan
- Defined 7 companion modes, 3-path privacy architecture, DPDP checklist

### Session 2 — Backend Skeleton
- Initialized FastAPI project with `app/` structure
- Set up SQLite (temporary), SQLAlchemy sync engine
- Created `User` and `Memory` models
- Wrote all Pydantic schemas (chat, user, memory)
- Implemented user auth: register / login / JWT / `get_current_user`
- Implemented Memory Vault CRUD routes
- Wrote `llm_service.py` shell — safety router, 7 mode prompts, pipeline structure — but `call_llm()` was a placeholder returning a hardcoded string

### Session 3 — PostgreSQL Migration
**Dropped SQLite. Switched to PostgreSQL + asyncpg (async driver).**

| What changed | How |
|---|---|
| `session.py` | Replaced sync `create_engine` + `Session` with `create_async_engine` + `AsyncSession` |
| `config.py` | `DATABASE_URL` → `postgresql+asyncpg://user:pass@host:5432/db` |
| `main.py` | Removed `create_tables()` from lifespan — Alembic owns schema now |
| All routes | Converted every DB call to `async`/`await` + `select()` (SQLAlchemy 2.0 style) |
| `dependencies.py` | `get_current_user` now fully async |
| `memory_vault.py` | All functions async; `purge_expired_memories` uses `delete()` not `query()` |
| `requirements.txt` | Added `asyncpg`, `alembic`, `psycopg2-binary`, `pytest-asyncio`, `httpx` |
| Alembic | Initialized + configured async env; first migration with `users` + `memories` tables |

### Session 4 — Real LLM Integration (Gemini)
**Replaced the `call_llm()` placeholder with a real Gemini API call.**

**Key decisions:**
- SDK: `google-genai >= 2.25.0` (new Interactions API, not the deprecated `google-generativeai`)
- Model: `gemini-3.8-flash` — fast, 1M context window, configurable via `GEMINI_MODEL` env var
- **`store=False` on every call** — Gemini does not store or train on conversations (Cloud Assist privacy guarantee)
- Conversation history is **client-managed** and injected as context text, never as server-side session state

**What was built:**

| Component | Detail |
|---|---|
| `call_llm()` | Real async Gemini call with `store=False`; graceful placeholder if key missing |
| `stream_llm()` | Streaming variant — yields SSE text chunks for real-time UI |
| Safety router | Keyword classifier: `urgent` (crisis keywords) → forced Soft mode + crisis preamble; `elevated` → blocks Sarcastic-Light |
| 7 mode prompts | Fully written system prompts for `soft`, `straight`, `coach`, `fire`, `sarcastic_light`, `quiet`, `rehearsal` |
| Universal guardrail | Appended to every prompt — no diagnosis, no meds advice, prompt injection protection |
| `POST /chat/stream` | **New** SSE streaming endpoint for real-time typing-style UI |
| `POST /chat/rehearsal` | Now generates dynamic simulation using Gemini (person/goal/intensity prompt) |
| `config.py` | Added `GEMINI_MODEL` setting |

---

## API Endpoints (current)

| Method | Path | Auth | Status |
|---|---|---|---|
| `GET` | `/health` | — | ✅ |
| `POST` | `/api/v1/users/register` | — | ✅ |
| `POST` | `/api/v1/users/login` | — | ✅ |
| `GET` | `/api/v1/users/me` | JWT | ✅ |
| `POST` | `/api/v1/chat/` | JWT | ✅ Real Gemini |
| `POST` | `/api/v1/chat/stream` | JWT | ✅ SSE streaming |
| `POST` | `/api/v1/chat/checkin` | JWT | ⚠️ Not persisted to DB |
| `POST` | `/api/v1/chat/rehearsal` | JWT | ✅ Real Gemini |
| `POST` | `/api/v1/memory/` | JWT | ✅ |
| `GET` | `/api/v1/memory/` | JWT | ✅ |
| `GET` | `/api/v1/memory/{id}` | JWT | ✅ |
| `DELETE` | `/api/v1/memory/{id}` | JWT | ✅ |
| `GET` | `/api/v1/memory/receipt/latest` | JWT | ⚠️ Stub |

---

## Privacy Architecture (implemented so far)

| Guarantee | Status |
|---|---|
| Server stores only ciphertext in Memory Vault | ✅ Model has `encrypted_data`, no plaintext field |
| No conversation training by Gemini | ✅ `store=False` on every LLM call |
| Client-managed conversation history | ✅ History injected as context, no server session |
| JWT short-lived auth | ✅ 15-min default expiry |
| Password hashing | ✅ bcrypt |
| User public key field for future E2EE sync | ✅ `public_key` column in User model |
| Client-side encryption before upload | ❌ No client yet |
| Memory TTL enforcement | ❌ `purge_expired_memories()` exists but no scheduler |
| Privacy receipt with real data | ❌ Stub only |

---

## Environment Setup

```bash
# 1. Create PostgreSQL database
psql -U postgres -c "CREATE USER unsaid WITH PASSWORD 'unsaid';"
psql -U postgres -c "CREATE DATABASE unsaid OWNER unsaid;"

# 2. Configure environment
cp .env.example .env
# Edit .env — set GEMINI_API_KEY and SECRET_KEY at minimum

# 3. Install dependencies
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 4. Run migrations
alembic upgrade head

# 5. Start server
uvicorn app.main:app --reload
```

---

## .env Variables

| Variable | Required | Default | Notes |
|---|---|---|---|
| `SECRET_KEY` | ✅ | — | Long random string for JWT signing |
| `DATABASE_URL` | ✅ | `postgresql+asyncpg://unsaid:unsaid@localhost:5432/unsaid` | PostgreSQL only |
| `GEMINI_API_KEY` | ✅ | — | Get from [aistudio.google.com](https://aistudio.google.com) |
| `GEMINI_MODEL` | — | `gemini-3.8-flash` | Swap model without code changes |
| `OPENAI_API_KEY` | — | — | Reserved, not wired yet |
| `BACKEND_CORS_ORIGINS` | — | `["http://localhost:3000"]` | Frontend origin(s) |

---

## ✅ Done / ❌ Remaining

> This section is the live tracker. Updated every session.

### Backend

| Status | Item | Notes |
|---|---|---|
| ✅ | FastAPI app setup | CORS, lifespan, route registration |
| ✅ | PostgreSQL async engine | `asyncpg` driver, `create_async_engine` |
| ✅ | Alembic migrations | `initial_tables` migration — `users` + `memories` |
| ✅ | User model | `id`, `username`, `hashed_password`, `public_key`, `is_active` |
| ✅ | Memory model | `encrypted_data`, `encrypted_category`, `retention`, `owner_id` |
| ✅ | JWT auth | Register, login, `get_current_user` dependency |
| ✅ | Password hashing | bcrypt via passlib |
| ✅ | Memory Vault CRUD | Create, list, get, delete — server stores ciphertext only |
| ✅ | Memory 7-day TTL function | `purge_expired_memories()` written |
| ✅ | Gemini LLM integration | Real `call_llm()` with `store=False`, `gemini-3.8-flash` |
| ✅ | Streaming LLM | `stream_llm()` + `POST /chat/stream` SSE endpoint |
| ✅ | Safety router | Keyword classifier: `urgent` / `elevated` / `low` |
| ✅ | 7 companion mode prompts | `soft`, `straight`, `coach`, `fire`, `sarcastic_light`, `quiet`, `rehearsal` |
| ✅ | Rehearsal endpoint | Dynamic Gemini-generated simulation |
| ✅ | Universal LLM guardrail | No diagnosis, no meds, prompt injection protection |
| ✅ | Pydantic schemas | Chat, User, Memory, CheckIn, Rehearsal |
| ❌ | CheckIn DB persistence | `/checkin` accepts requests but saves nothing |
| ❌ | CheckIn model | No `CheckIn` SQLAlchemy model or migration yet |
| ❌ | Weekly pattern view | Needs persisted check-ins first |
| ❌ | Memory TTL scheduler | `purge_expired_memories()` exists but never called — needs APScheduler/Celery |
| ❌ | Privacy receipt (real data) | `build_privacy_receipt()` returns stub `stored=0, deleted=0` |
| ❌ | RAG pipeline | `rag_pipeline.py` is empty; LangChain + LlamaIndex in deps |
| ❌ | Multi-device sync | `public_key` column exists but no key exchange logic |
| ❌ | Logging setup | `core/logging.py` is an empty file |
| ❌ | Tests | `conftest.py` exists but zero test cases written |
| ❌ | ML safety classifier | Current safety router is keyword-only; needs a real classifier |
| ❌ | Blank Mode endpoint | Designed in `features.md`; not started |
| ❌ | "Do not remember" toggle | `remember_session` field exists in schema; not enforced server-side |
| ❌ | Anti-dependency guardrails | Designed; not implemented in prompts yet |

### Frontend

| Status | Item | Notes |
|---|---|---|
| ❌ | Any frontend | Zero code — full 8-week roadmap in `ui-ux-masterplan.md` |
| ❌ | Client-side AES-GCM encryption | Required before Memory Vault privacy guarantee is real |
| ❌ | "Cloud AI used" label in UI | Must be shown per privacy architecture |
| ❌ | Privacy Center screen | Designed; not built |
| ❌ | Companion mode selector UI | Designed; not built |
| ❌ | Check-in UI | Designed; not built |
| ❌ | Streaming chat UI (SSE) | Backend ready; frontend not started |

### Infrastructure

| Status | Item | Notes |
|---|---|---|
| ✅ | Dockerfile | Present in `/backend` |
| ✅ | `.env.example` | All variables documented |
| ❌ | Docker Compose | No `docker-compose.yml` (Postgres + API together) |
| ❌ | Background task scheduler | For memory TTL purge |
| ❌ | Production secret management | `SECRET_KEY` is a placeholder in config |
| ❌ | Vector DB / embeddings store | Needed for RAG |
| ❌ | CI/CD pipeline | Not set up |

---

## Key Design Decisions & Why

| Decision | Reason |
|---|---|
| `store=False` on all Gemini calls | Cloud Assist path — must not train on private mental health conversations |
| Client-managed conversation history | Server never accumulates session state; no leakage on breach |
| Server stores only ciphertext in Memory Vault | Server-side breach can't expose vault content without client key |
| `public_key` on User model | Groundwork for future cross-device E2EE sync (Signal-style) |
| Alembic instead of `create_tables()` | Production-grade: migrations are versioned, reversible, auditable |
| Async SQLAlchemy throughout | FastAPI is async — sync DB calls block the event loop |
| `gemini-3.8-flash` | 1M context window handles long conversation history; fast enough for real-time chat |
| No E2EE claim for cloud AI chat | Honest per the three-path architecture — Cloud Assist label required in UI |
