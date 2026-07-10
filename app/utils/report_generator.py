import json
from io import BytesIO
from typing import Any

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def generate_analysis_json(result_data: dict[str, Any]) -> bytes:
    return json.dumps(
        result_data,
        indent=4,
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")


def generate_analysis_pdf(result_data: dict[str, Any]) -> bytes:
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45,
        title="AI Resume Analysis Report",
        author="AI Resume Analyzer",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=24,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=17,
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        name="ReportBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=6,
    )

    story = [
        Paragraph("AI Resume Analysis Report", title_style),
        Paragraph(
            f"<b>Resume:</b> {_safe_text(result_data.get('name', 'Unknown'))}",
            body_style,
        ),
        Paragraph(
            f"<b>Analysis ID:</b> {_safe_text(result_data.get('file_id', 'N/A'))}",
            body_style,
        ),
        Paragraph(
            f"<b>Status:</b> {_safe_text(result_data.get('status', 'N/A'))}",
            body_style,
        ),
        Paragraph(
            f"<b>ATS Score:</b> {_safe_text(result_data.get('ats_score', 'N/A'))}/100",
            body_style,
        ),
        Spacer(1, 0.15 * inch),
    ]

    _add_list_section(
        story,
        "Matched Skills",
        result_data.get("matched_skills"),
        heading_style,
        body_style,
    )

    _add_list_section(
        story,
        "Missing Skills",
        result_data.get("missing_skills"),
        heading_style,
        body_style,
    )

    _add_list_section(
        story,
        "Required Skills",
        result_data.get("required_skills"),
        heading_style,
        body_style,
    )

    story.append(Paragraph("Job Description", heading_style))
    story.append(
        Paragraph(
            _safe_text(result_data.get("job_description")),
            body_style,
        )
    )

    story.append(Paragraph("Detailed Analysis", heading_style))

    report_text = result_data.get("result") or "No analysis report available."

    for line in report_text.splitlines():
        clean_line = line.strip()

        if not clean_line:
            story.append(Spacer(1, 0.08 * inch))
            continue

        if clean_line.startswith("#"):
            heading = clean_line.lstrip("#").strip()
            story.append(Paragraph(_safe_text(heading), heading_style))
        else:
            story.append(Paragraph(_safe_text(clean_line), body_style))

    document.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes


def _add_list_section(
    story: list,
    title: str,
    values: list[str] | None,
    heading_style: ParagraphStyle,
    body_style: ParagraphStyle,
) -> None:
    story.append(Paragraph(title, heading_style))

    if not values:
        story.append(Paragraph("None", body_style))
        return

    for value in values:
        story.append(
            Paragraph(
                f"- {_safe_text(value)}",
                body_style,
            )
        )


def _safe_text(value: Any) -> str:
    if value is None:
        return "Not available"

    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )