from __future__ import annotations

from google import genai
from google.genai import types


class GeminiDocumentGenerator:
    """Generate legal-document drafts through Google's Gemini API."""

    def __init__(self, api_key: str, model: str) -> None:
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")
        self.model = model
        self.client = genai.Client(api_key=api_key)

    def generate_document(
        self,
        *,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
        jurisdiction: str,
        additional_instructions: str = "",
    ) -> str:
        prompt = f"""
You are LegalEase's legal-document drafting assistant.

Create a professional LEGAL DOCUMENT DRAFT, not legal advice. Use only the facts supplied by the user. Do not invent names, addresses, dates, money amounts, statutes, case citations, registration numbers, or other material facts.

Document type:
{document_type}

Parties:
{parties}

Effective date:
{effective_date}

Jurisdiction:
{jurisdiction}

User-supplied terms:
{terms}

Additional instructions:
{additional_instructions or "None"}

Drafting requirements:
1. Start with a clear document title.
2. Identify the parties and effective date.
3. Use numbered sections with concise headings.
4. Convert the supplied terms into appropriate clauses without changing their meaning.
5. Add only standard structural clauses that are appropriate to the selected document type; when a fact is missing, use a clearly marked placeholder such as [TO BE COMPLETED].
6. Include signature blocks at the end.
7. Do not claim that the document is legally valid, attorney-reviewed, or suitable for a particular jurisdiction unless the user supplied that fact.
8. Do not include markdown code fences.
9. Return plain text suitable for editing and DOCX/PDF conversion.
10. If jurisdiction is not specified, keep jurisdiction-specific legal claims generic and include [JURISDICTION TO BE CONFIRMED].

Return only the draft document.
""".strip()

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=8192,
            ),
        )

        text = (response.text or "").strip()
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text
