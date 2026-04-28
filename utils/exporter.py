"""Export meeting analysis results to PDF and DOCX."""
from __future__ import annotations

from io import BytesIO
from typing import Any, Dict


def export_to_pdf(result: Dict[str, Any]) -> bytes:
    """Return a meeting intelligence report as PDF bytes."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 12, "Meeting Intelligence Report", ln=True)
    pdf.ln(3)

    def section(title: str, content: Any) -> None:
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 9, title.encode("latin-1", "replace").decode("latin-1"), ln=True)
        pdf.set_font("Arial", "", 10)
        if isinstance(content, list):
            for item in content:
                pdf.multi_cell(0, 6, ("- " + str(item)).encode("latin-1", "replace").decode("latin-1"))
        elif isinstance(content, dict):
            for k, v in content.items():
                pdf.multi_cell(0, 6, f"{k}: {v}".encode("latin-1", "replace").decode("latin-1"))
        else:
            pdf.multi_cell(0, 6, str(content).encode("latin-1", "replace").decode("latin-1"))
        pdf.ln(2)

    section("Executive Summary", result.get("executive_summary", ""))
    section("Key Decisions", result.get("key_decisions", []))
    section("Action Items", result.get("action_items", []))
    section("Risks Flagged", result.get("risks_flagged", []))
    section("Open Questions", result.get("open_questions", []))
    section("Follow-up Email", result.get("follow_up_email", {}))
    data = pdf.output(dest="S")
    return data if isinstance(data, bytes) else data.encode("latin-1")


def export_to_docx(result: Dict[str, Any]) -> bytes:
    """Return a meeting intelligence report as DOCX bytes."""
    from docx import Document

    doc = Document()
    doc.add_heading("Meeting Intelligence Report", level=0)

    def section(title: str, content: Any) -> None:
        doc.add_heading(title, level=1)
        if isinstance(content, list):
            for item in content:
                doc.add_paragraph(str(item), style="List Bullet")
        elif isinstance(content, dict):
            for k, v in content.items():
                doc.add_paragraph(f"{k}: {v}")
        else:
            doc.add_paragraph(str(content))

    section("Executive Summary", result.get("executive_summary", ""))
    section("Key Decisions", result.get("key_decisions", []))
    section("Action Items", result.get("action_items", []))
    section("Risks Flagged", result.get("risks_flagged", []))
    section("Open Questions", result.get("open_questions", []))
    section("Follow-up Email", result.get("follow_up_email", {}))
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()
