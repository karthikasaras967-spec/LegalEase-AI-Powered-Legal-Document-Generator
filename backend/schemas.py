from datetime import date
from pydantic import BaseModel, Field, field_validator


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    parties: str = Field(..., min_length=2, max_length=3000)
    terms: str = Field(..., min_length=2, max_length=10000)
    effective_date: str = Field(..., min_length=2, max_length=100)
    jurisdiction: str = Field(default="Not specified", max_length=200)
    additional_instructions: str = Field(default="", max_length=5000)

    @field_validator("document_type", "parties", "terms", "effective_date", "jurisdiction", "additional_instructions")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class DocumentResponse(BaseModel):
    document_type: str
    content: str
    model: str
    demo_mode: bool
