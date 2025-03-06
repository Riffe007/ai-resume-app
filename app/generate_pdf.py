import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# Define PDF Storage Directory
PDF_DIR = "generated_pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

# **Define Styles**
TITLE_STYLE = ParagraphStyle(
    "Title", fontSize=22, textColor=colors.HexColor("#003366"),
    spaceAfter=12, alignment=1, fontName="Helvetica-Bold"
)
SECTION_HEADER_STYLE = ParagraphStyle(
    "SectionHeader", fontSize=14, textColor=colors.HexColor("#004B87"),
    spaceBefore=15, spaceAfter=8, fontName="Helvetica-Bold"
)
JOB_TITLE_STYLE = ParagraphStyle(
    "JobTitle", fontSize=12, textColor=colors.HexColor("#2E3A46"),
    spaceBefore=8, spaceAfter=4, fontName="Helvetica-Bold"
)
DATE_STYLE = ParagraphStyle(
    "Date", fontSize=10, textColor=colors.HexColor("#666666"),
    spaceAfter=6, fontName="Helvetica-Oblique"
)
BODY_STYLE = ParagraphStyle("Body", fontSize=11, leading=14, spaceAfter=5)
BULLET_STYLE = ParagraphStyle("Bullet", fontSize=11, leading=14, bulletIndent=10, leftIndent=20)

def generate_pdf_resume(markdown_resume: str, resume_id: str):
    """Generates a **high-end** professionally formatted resume PDF."""

    pdf_path = os.path.join(PDF_DIR, f"resume_{resume_id}.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=50, bottomMargin=30)
    elements = []

    # **Contact Information**
    contact_info = [
        ["📧 **Email:**", "timothy.riffe@unified-software-ai.com"],
        ["📞 **Phone:**", "(661) 809-6450"],
        ["🔗 **LinkedIn:**", "linkedin.com/in/timothyriffe"]
    ]
    contact_table = Table(contact_info, colWidths=[100, 350])
    contact_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#003366")),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8F1FA")),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))

    # **Key Skills**
    key_skills = [
        ["✔ AI/ML Strategy", "✔ Cybersecurity & Risk Management"],
        ["✔ Financial Modeling", "✔ Government Contracting"],
        ["✔ Cloud Computing", "✔ Business Intelligence"],
        ["✔ Strategic Leadership", ""]
    ]
    skills_table = Table(key_skills, colWidths=[225, 225])
    skills_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F5F5")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#2E3A46")),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    # **Certifications & Tech Stack**
    certs_tech = [
        ["📜 **Certifications:**", "📌 **Technical Stack:**"],
        ["✔ AWS AI Practitioner", "✔ Python, TensorFlow, PyTorch"],
        ["✔ AWS Cloud Practitioner", "✔ AWS, Azure, Google Cloud"],
        ["✔ Series 65 & 63", "✔ SIEM, Zero Trust Security"],
        ["✔ Professional Selling Skills", "✔ Bloomberg Terminal, Capital IQ"]
    ]
    certs_table = Table(certs_tech, colWidths=[225, 225])
    certs_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F5F5")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#2E3A46")),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    # **Work Experience**
    experience = [
        ["**CEO & AI Consultant** — Unified Software Solutions", "2021 – Present"],
        ["- Founded and scaled AI-driven business solutions for finance and government sectors.", ""],
        ["- Led 150+ developers & AI engineers in enterprise solution delivery.", ""],
        ["- Secured DARPA & SOCOM government contracts integrating AI into national security.", ""],
        ["**Director of Strategic Initiatives** — ATTAC Group Inc.", "2020 – 2021"],
        ["- Led initiatives that helped ATTAC secure 7+ contracts.", ""],
        ["- Negotiated key deals with Magellan RX Management.", ""],
        ["**Quantitative Researcher** — WorldQuant", "2023 – Present"],
        ["- Developed ML models optimizing investment strategies.", ""],
        ["- Utilized big data analytics to identify market trends.", ""]
    ]
    experience_table = Table(experience, colWidths=[350, 100])
    experience_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#2E3A46")),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    # **Military Service & Awards**
    military_awards = [
        ["🏅 **Two Combat Action Ribbons**"],
        ["🎖 **Army Achievement Medal**"],
        ["🏅 **Two Good Conduct Medals**"],
        ["🎖 **Iraq & Afghanistan Campaign Medals**"],
        ["🏅 **Global War on Terrorism Medal**"],
        ["🎖 **Navy Unit Commendation**"],
        ["🏅 **Multiple Meritorious Masts**"],
        ["🎖 **Letters of Appreciation**"]
    ]
    military_table = Table(military_awards, colWidths=[450])

    # **Add Sections**
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Timothy Riffe - AI Engineer Resume", TITLE_STYLE))
    elements.append(Spacer(1, 8))
    elements.append(contact_table)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Key Skills", SECTION_HEADER_STYLE))
    elements.append(skills_table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Certifications & Technical Stack", SECTION_HEADER_STYLE))
    elements.append(certs_table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Work Experience", SECTION_HEADER_STYLE))
    elements.append(experience_table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Military Service & Awards", SECTION_HEADER_STYLE))
    elements.append(military_table)

    doc.build(elements)
    return pdf_path
