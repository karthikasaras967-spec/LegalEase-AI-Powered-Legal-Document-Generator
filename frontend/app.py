from __future__ import annotations

import html
import os
from datetime import date

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom styling
# ─────────────────────────────────────────────

st.markdown(
    """
    <style>

    /* Main page */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Header */
    .brand {
        text-align: center;
        margin-bottom: 0.3rem;
    }

    .brand-icon {
        font-size: 3.2rem;
        margin-bottom: 0;
    }

    .brand-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
    }

    .brand-title span {
        color: #7c3aed;
    }

    .brand-subtitle {
        color: #8b93a7;
        font-size: 1.05rem;
        margin-top: 0.3rem;
        margin-bottom: 1.5rem;
    }

    /* Section cards */
    .section-card {
        background: rgba(127, 127, 127, 0.07);
        border: 1px solid rgba(127, 127, 127, 0.15);
        border-radius: 16px;
        padding: 1.2rem 1.3rem;
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .section-description {
        color: #8b93a7;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    /* Preview */
    .preview {
        background: #111827;
        color: #f3f4f6;
        padding: 1.6rem;
        border-radius: 14px;
        min-height: 520px;
        max-height: 680px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-family: Georgia, "Times New Roman", serif;
        line-height: 1.65;
        border: 1px solid #273449;
    }

    /* Model badge */
    .model-badge {
        display: inline-block;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        background: rgba(124, 58, 237, 0.12);
        border: 1px solid rgba(124, 58, 237, 0.3);
        color: #a78bfa;
        font-size: 0.8rem;
        margin-top: 0.6rem;
    }

    /* Download card */
    .download-card {
        background: rgba(127, 127, 127, 0.06);
        border: 1px solid rgba(127, 127, 127, 0.14);
        border-radius: 14px;
        padding: 1rem;
        margin-top: 1rem;
    }

    /* Disclaimer */
    .disclaimer {
        padding: 1rem 1.1rem;
        border-radius: 12px;
        background: rgba(245, 158, 11, 0.10);
        border: 1px solid rgba(245, 158, 11, 0.25);
        color: #fbbf24;
        font-size: 0.88rem;
        line-height: 1.5;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(127, 127, 127, 0.15);
    }

    .sidebar-title {
        font-size: 1.35rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }

    .sidebar-subtitle {
        color: #8b93a7;
        font-size: 0.85rem;
        margin-bottom: 1.2rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #7f8798;
        font-size: 0.82rem;
        padding: 1.2rem 0 0.5rem 0;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────

st.markdown(
    """
    <div class="brand">
        <div class="brand-icon">⚖️</div>
        <div class="brand-title">Legal<span>Ease</span></div>
        <div class="brand-subtitle">
            AI-powered legal document drafting, editing and export
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="disclaimer">
        ⚠️ <strong>Important:</strong>
        LegalEase creates AI-generated drafts for informational and
        document-preparation purposes. Review the final document with a
        qualified legal professional before signing or relying on it.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


# ─────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────

if "document" not in st.session_state:
    st.session_state.document = ""

if "model" not in st.session_state:
    st.session_state.model = ""

if "docx_bytes" not in st.session_state:
    st.session_state.docx_bytes = None

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">⚙️ Document Setup</div>
        <div class="sidebar-subtitle">
            Enter the information needed to create your document.
        </div>
        """,
        unsafe_allow_html=True,
    )

    document_type = st.text_input(
        "Document type",
        value="Freelance Work Contract",
        placeholder="e.g. NDA, Lease Agreement",
    )

    parties = st.text_area(
        "Parties involved",
        value="Jane Doe (Service Provider), TechNova Inc. (Client)",
        height=100,
        placeholder="Enter the names and roles of all parties...",
    )

    effective_date = st.date_input(
        "Effective date",
        value=date.today(),
    )

    jurisdiction = st.text_input(
        "Jurisdiction",
        value="Not specified",
        help="Optional. Example: Tamil Nadu, India",
    )

    terms = st.text_area(
        "Terms & conditions",
        value=(
            "Payment within 30 days of invoice; "
            "Provider will deliver work by the agreed deadline; "
            "Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),
        height=180,
        help="Separate clauses with semicolons.",
    )

    additional = st.text_area(
        "Additional instructions",
        placeholder=(
            "Tone, special clauses, placeholders, "
            "formatting preferences..."
        ),
        height=100,
    )

    logo = st.file_uploader(
        "Optional logo for DOCX/PDF",
        type=["png", "jpg", "jpeg"],
    )

    st.write("")

    generate = st.button(
        "✨ Generate Document",
        type="primary",
        use_container_width=True,
    )


# ─────────────────────────────────────────────
# Generate document
# ─────────────────────────────────────────────

if generate:

    if not all(
        [
            document_type.strip(),
            parties.strip(),
            terms.strip(),
        ]
    ):
        st.error(
            "Please complete document type, parties, and terms."
        )

    else:

        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date.isoformat(),
            "jurisdiction": jurisdiction,
            "additional_instructions": additional,
        }

        try:

            with st.spinner(
                "🤖 Gemini is drafting your document..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120,
                )

            if response.ok:

                data = response.json()

                st.session_state.document = data["content"]
                st.session_state.model = data.get(
                    "model",
                    "",
                )

                # Clear old exports because the document changed.
                st.session_state.docx_bytes = None
                st.session_state.pdf_bytes = None

                st.success(
                    "✅ Document generated successfully."
                )

            else:

                try:
                    detail = response.json().get(
                        "detail",
                        response.text,
                    )
                except Exception:
                    detail = response.text

                st.error(
                    f"Backend error ({response.status_code}): {detail}"
                )

        except requests.RequestException as exc:

            st.error(
                "Could not connect to the FastAPI backend. "
                "Start it with `uvicorn backend.main:app --reload`."
            )

            st.caption(str(exc))


# ─────────────────────────────────────────────
# Main workspace
# ─────────────────────────────────────────────

left, right = st.columns(
    [1, 1],
    gap="large",
)


# ─────────────────────────────────────────────
# Generated document
# ─────────────────────────────────────────────

with left:

    st.markdown(
        """
        <div class="section-title">
            📄 Generated Document
        </div>
        <div class="section-description">
            Preview the AI-generated legal document.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.document:

        st.markdown(
            f"""
            <div class="preview">
                {html.escape(st.session_state.document)}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.model:

            st.markdown(
                f"""
                <div class="model-badge">
                    🤖 Generated with {html.escape(st.session_state.model)}
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        st.info(
            "Your generated document will appear here."
        )


# ─────────────────────────────────────────────
# Editable version
# ─────────────────────────────────────────────

with right:

    st.markdown(
        """
        <div class="section-title">
            ✏️ Editable Version
        </div>
        <div class="section-description">
            Review and modify the document before exporting it.
        </div>
        """,
        unsafe_allow_html=True,
    )

    edited = st.text_area(
        "Edit the document before exporting",
        value=st.session_state.document,
        height=520,
        label_visibility="collapsed",
        placeholder="Your generated document will appear here...",
    )

    if edited != st.session_state.document:

        st.session_state.document = edited

        # Edited content should require fresh exports.
        st.session_state.docx_bytes = None
        st.session_state.pdf_bytes = None

    document = st.session_state.document


# ─────────────────────────────────────────────
# Download section
# ─────────────────────────────────────────────

if document:

    st.divider()

    st.markdown(
        """
        <div class="section-title">
            📥 Export Document
        </div>
        <div class="section-description">
            Download your edited document in your preferred format.
        </div>
        """,
        unsafe_allow_html=True,
    )

    download_col1, download_col2, download_col3 = st.columns(
        3,
        gap="medium",
    )

    # TXT
    with download_col1:

        txt_bytes = document.encode("utf-8")

        st.download_button(
            "⬇️ Download TXT",
            data=txt_bytes,
            file_name="legalease_document.txt",
            mime="text/plain",
            use_container_width=True,
        )

    # DOCX
    with download_col2:

        if st.button(
            "📝 Prepare DOCX",
            use_container_width=True,
        ):

            try:

                from backend.services.exporters import format_docx

                logo_bytes = (
                    logo.getvalue()
                    if logo
                    else None
                )

                st.session_state.docx_bytes = format_docx(
                    document,
                    document_type,
                    logo_bytes,
                )

                st.success("DOCX ready.")

            except Exception as exc:

                st.error(
                    f"DOCX generation failed: {exc}"
                )

        if st.session_state.docx_bytes:

            st.download_button(
                "⬇️ Download DOCX",
                data=st.session_state.docx_bytes,
                file_name="legalease_document.docx",
                mime=(
                    "application/"
                    "vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                use_container_width=True,
            )

    # PDF
    with download_col3:

        if st.button(
            "📕 Prepare PDF",
            use_container_width=True,
        ):

            try:

                from backend.services.exporters import format_pdf

                logo_bytes = (
                    logo.getvalue()
                    if logo
                    else None
                )

                st.session_state.pdf_bytes = format_pdf(
                    document,
                    document_type,
                    logo_bytes,
                )

                st.success("PDF ready.")

            except Exception as exc:

                st.error(
                    f"PDF generation failed: {exc}"
                )

        if st.session_state.pdf_bytes:

            st.download_button(
                "⬇️ Download PDF",
                data=st.session_state.pdf_bytes,
                file_name="legalease_document.pdf",
                mime="application/pdf",
                use_container_width=True,
            )


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────

st.divider()

st.markdown(
    """
    <div class="footer">
        ⚖️ <strong>LegalEase</strong>
        &nbsp;•&nbsp;
        AI-powered legal document drafting
        &nbsp;•&nbsp;
        AI-generated drafts only
        <br>
        No generated document is automatically saved by this local application.
    </div>
    """,
    unsafe_allow_html=True,
)