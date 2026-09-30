from backend.services.document_service import sanitize_text, split_terms
from backend.services.exporters import format_docx, format_pdf


def sample():
    return """NON-DISCLOSURE AGREEMENT

1. CONFIDENTIALITY
The receiving party shall protect confidential information.

2. TERM
This agreement starts on the effective date.

SIGNATURES
Party 1: __________________
Party 2: __________________
"""


def test_sanitize_text():
    assert sanitize_text("“Hello”\u00a0world") == '"Hello" world'


def test_split_terms():
    assert split_terms("A; B; ; C") == ["A", "B", "C"]


def test_docx_export():
    data = format_docx(sample(), "NDA")
    assert data[:2] == b"PK"


def test_pdf_export():
    data = format_pdf(sample(), "NDA")
    assert data.startswith(b"%PDF")
