# LegalEase — AI-Powered Legal Document Generator

LegalEase is a complete FastAPI + Streamlit application for generating editable legal-document drafts with Google Gemini, then exporting them as TXT, DOCX, or PDF.

> **Important:** LegalEase generates drafts for informational/document-preparation purposes. It is not a substitute for advice from a qualified lawyer. Users should review generated documents for the applicable jurisdiction before signing or relying on them.

## Architecture

```text
Streamlit UI
    |
    | HTTP POST /generate
    v
FastAPI backend
    |
    v
GeminiDocumentGenerator
    |
    v
Google Gemini API

Generated text
    |
    +--> editable preview
    +--> TXT
    +--> DOCX
    +--> PDF
```

The project follows the supplied documentation's intended architecture: Streamlit frontend, FastAPI backend, Gemini AI core, and DOCX/PDF/TXT formatting/export modules.

## Project structure

```text
LegalEase/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   ├── config.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_service.py
│   │   └── exporters.py
│   └── ai_core/
│       ├── __init__.py
│       └── gemini_generator.py
├── frontend/
│   └── app.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_exporters.py
├── assets/
│   └── .gitkeep
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Requirements

- Python 3.10+
- A Google Gemini API key
- VS Code recommended

The original project document specifies `gemini-1.5-pro`. That model is no longer a safe dependency to hard-code for a new application, so the implementation reads the model name from `GEMINI_MODEL`. Set it to a model available to your API account. A common current choice is `gemini-2.5-flash`.

## 1. Open the project in VS Code

Open the `LegalEase` folder in VS Code.

## 2. Create a virtual environment

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Gemini

Copy `.env.example` to `.env` and set your API key:

```env
GEMINI_API_KEY=your_real_api_key
GEMINI_MODEL=gemini-2.5-flash
BACKEND_URL=http://127.0.0.1:8000
```

Never commit `.env`.

## 5. Start the FastAPI backend

From the project root:

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Check:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## 6. Start the Streamlit frontend

Open a second VS Code terminal, activate the same `.venv`, then:

```bash
streamlit run frontend/app.py
```

Open the URL Streamlit prints, normally:

```text
http://localhost:8501
```

## 7. Test the application

Enter:

- Document type: `Freelance Work Contract`
- Parties: `Jane Doe (Service Provider), TechNova Inc. (Client)`
- Terms:
  - `Payment within 30 days of invoice`
  - `Provider will deliver work by the agreed deadline`
  - `Confidentiality must be maintained`
  - `Either party may terminate with 15 days notice`
- Effective date: today's or another intended date

Click **Generate Document**.

Then edit the text if needed and download TXT, DOCX, or PDF.

## Automated tests

The tests do not call Gemini. They validate schemas, health endpoints, sanitization, and document exporters.

```bash
pytest -q
```

## Running without Gemini

For UI/export development without an API key, the backend has a deterministic demo mode:

```env
DEMO_MODE=true
```

In demo mode, `/generate` returns a clearly marked sample draft instead of calling Gemini.

## Docker

```bash
docker compose up --build
```

The API is exposed at `http://localhost:8000`. Streamlit is exposed at `http://localhost:8501`.

Set `GEMINI_API_KEY` in your shell or `.env` before starting if you want real AI generation.

## Security notes

- API keys are loaded from environment variables.
- The frontend does not receive the Gemini API key.
- CORS is restricted by `CORS_ORIGINS`.
- Request size and field lengths are validated.
- Generated documents are drafts and are not automatically stored by the server.
- Uploaded logos are processed in memory by the frontend and are not sent to the backend.

## Troubleshooting

### `ModuleNotFoundError`

Make sure the virtual environment is activated:

```bash
python -c "import fastapi, streamlit, google.genai; print('OK')"
```

### Gemini authentication error

Check `.env`:

```env
GEMINI_API_KEY=...
```

Restart Uvicorn after changing environment variables.

### Model not found

Change:

```env
GEMINI_MODEL=...
```

to a Gemini model enabled for your API account.

### DOCX/PDF download error

Run:

```bash
pip install -r requirements.txt
```

and rerun the tests:

```bash
pytest -q
```
