# UNSAID Backend

Privacy-first mental health companion API built with Python, FastAPI, and LLM integrations. This backend serves as the core engine for the UNSAID application, prioritizing user privacy, strict safety rules, and encrypted memory storage.

## Tech Stack
- **Framework**: FastAPI (Python 3)
- **Database**: SQLite (local) / PostgreSQL (production) via SQLAlchemy
- **Validation & Config**: Pydantic
- **Security**: JWT Authentication (python-jose), Password Hashing (passlib + bcrypt)
- **AI/LLM Integration**: Designed for LangChain / LlamaIndex / OpenAI

## Core Architecture & Features

### 1. Privacy & Memory Vault (`app/services/memory_vault.py`)
- **Client-Side Symmetric Encryption**: The backend **never** sees or stores plaintext memories. It only stores AES-GCM-256 ciphertext.
- **Memory Dial**: Memories are tagged with user-controlled retention rules (`7_days`, `until_delete`, `vault`).
- **Privacy Receipt**: The API generates a receipt after sensitive sessions to transparently show users what was saved, deleted, and where inference occurred.

### 2. Safety Router (`app/services/llm_service.py`)
- Safety is non-negotiable and overrides personality modes.
- **Urgent Risk**: If keywords like "self-harm" or "suicide" are detected, the API bypasses the chosen personality and forces a "Safe Mode" response with grounding language and crisis bridges.
- **Elevated Risk**: Disables lighter/sarcastic modes to ensure the companion remains supportive during panic or distress.

### 3. API Endpoints
- **`/api/v1/users`**: Handles user registration, JWT login, and profile fetching.
- **`/api/v1/memory`**: CRUD operations for the encrypted Memory Vault.
- **`/api/v1/chat/`**: The main interaction pipeline: `Safety Router → Mode Selector → LLM Call → Response`.
- **`/api/v1/chat/checkin`**: Emotional check-ins to measure user state without diagnostic labeling.
- **`/api/v1/chat/rehearsal`**: "Conversation Gym" endpoint where the AI simulates difficult real-world conversations and breaks down what is in/out of the user's control.

## Directory Structure
```text
backend/
├── app/
│   ├── api/
│   │   ├── routes/          # API endpoints (chat.py, memory.py, user.py)
│   │   └── dependencies.py  # Auth (get_current_user) & DB dependencies
│   ├── core/                # Configuration, security tools, and custom exceptions
│   ├── db/                  # Database session config
│   │   └── models/          # SQLAlchemy models (User, Memory)
│   ├── schemas/             # Pydantic validation models (DTOs)
│   ├── services/            # Core business & AI logic (LLM service, Memory Vault)
│   └── main.py              # FastAPI application entry point
├── requirements.txt         
└── README.md
```

## Setup & Running Locally

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Copy `.env.example` to `.env` (if available) and configure your `SECRET_KEY` and LLM API keys (e.g., `OPENAI_API_KEY`).

4. **Run the server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   *Note: The SQLite database and tables will be automatically created upon startup.*

5. **API Documentation**:
   Once running, visit `http://localhost:8000/docs` to view the interactive Swagger UI and test the endpoints.
