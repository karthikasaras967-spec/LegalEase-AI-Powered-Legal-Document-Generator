from fastapi import APIRouter, HTTPException
from backend.ai_core.gemini_generator import GeminiDocumentGenerator
from backend.config import get_settings
from backend.schemas import DocumentRequest, DocumentResponse
from backend.services.document_service import demo_document, sanitize_text

router = APIRouter(tags=["documents"])


@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest) -> DocumentResponse:
    settings = get_settings()

    if settings.demo_mode:
        content = demo_document(
            request.document_type,
            request.parties,
            request.terms,
            request.effective_date,
            request.jurisdiction,
        )
        return DocumentResponse(
            document_type=request.document_type,
            content=sanitize_text(content),
            model="demo",
            demo_mode=True,
        )

    try:
        generator = GeminiDocumentGenerator(
            api_key=settings.gemini_api_key,
            model=settings.gemini_model,
        )
        content = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            jurisdiction=request.jurisdiction,
            additional_instructions=request.additional_instructions,
        )
        return DocumentResponse(
            document_type=request.document_type,
            content=sanitize_text(content),
            model=settings.gemini_model,
            demo_mode=False,
        )
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AI generation failed: {exc}",
        ) from exc
