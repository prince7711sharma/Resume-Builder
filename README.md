# RS Education Solution — AI Resume Builder API

AI-powered Resume Builder backend built with FastAPI, LangChain, and Groq.

---

## Stack

| Layer      | Technology                      |
|------------|---------------------------------|
| Framework  | FastAPI + Uvicorn               |
| LLM        | Groq API (llama3-70b-8192)      |
| Orchestration | LangChain + PromptTemplate   |
| Validation | Pydantic v2                     |
| Config     | pydantic-settings + dotenv      |

---

## Project Structure

```
app/
├── main.py                    # FastAPI app factory + health routes
├── core/
│   ├── config.py              # Settings via pydantic-settings
│   └── llm.py                 # Groq LLM initializer
├── schemas/
│   └── resume_schema.py       # Pydantic input/output models
├── agents/
│   └── resume_agent.py        # LangChain agent + PromptTemplate
├── services/
│   └── resume_service.py      # Business logic orchestration
├── api/
│   └── routes/
│       └── resume_routes.py   # POST /api/v1/generate-resume
└── utils/
    └── formatter.py           # Input serializer + output cleaner
```

---

## Setup

### 1. Clone and enter the project

```bash
git clone <repo-url>
cd resume_builder
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env and set your GROQ_API_KEY
```

### 5. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## API Endpoints

| Method | Endpoint                    | Description              |
|--------|-----------------------------|--------------------------|
| GET    | `/`                         | Health check             |
| GET    | `/health`                   | Detailed health status   |
| GET    | `/docs`                     | Swagger UI               |
| GET    | `/redoc`                    | ReDoc documentation      |
| POST   | `/api/v1/generate-resume`   | Generate resume          |

---

## Test with sample payload

```bash
curl -X POST http://localhost:8000/api/v1/generate-resume \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

---

## Environment Variables

| Variable        | Required | Default              | Description              |
|-----------------|----------|----------------------|--------------------------|
| GROQ_API_KEY    | Yes      | —                    | Your Groq API key        |
| GROQ_MODEL      | No       | llama3-70b-8192      | Groq model name          |
| GROQ_TEMPERATURE| No       | 0.3                  | LLM temperature          |
| GROQ_MAX_TOKENS | No       | 4096                 | Max output tokens        |
| DEBUG           | No       | False                | Enable debug mode        |

---

## Resume Output Format

Every generated resume follows this exact structure:

1. **HEADER** — Name, contact, profile links
2. **PROFESSIONAL SUMMARY** — 3–4 line paragraph
3. **EXPERTISE** — Single line with | separators
4. **TECHNICAL SKILLS** — Categorized: Languages, Web Dev, ML & AI, Libraries, Tools & DBs
5. **FEATURED PROJECTS** — Role | Name with 3 action-driven bullets each
6. **EDUCATION** — Degree | Institution | Year
7. **CERTIFICATIONS & ACHIEVEMENTS** — Bullet list

---

Built for RS Education Solution Platform.
