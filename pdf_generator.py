from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Paragraph


def generate_pdf(data, customer_name):
    from reportlab.lib.pagesizes import A4, landscape

    pdf = SimpleDocTemplate(
    "Claim_History.pdf",
    pagesize=landscape(A4)
 )

    # 👇 Paste Step 2 here
    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER

    normal_style = styles["Normal"]

    # Existing code
    # Wrap long text
    for i in range(1, len(data)):
        data[i][3] = Paragraph(str(data[i][3]), normal_style)   # Material Description
        data[i][6] = Paragraph(str(data[i][6]), normal_style)   # Defect Description
    table = Table(
    data,
    colWidths=[
        70,   # Docket Number
        58,   # Docket Date
        90,   # Customer Name
        155,  # Material Description
        100,  # Serial Number
        60,   # Status
        170,  # Defect Description
        55,   # Claim Loss
        45    # Wear %
      ]
     )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,1), (-1,-1), colors.beige),
        ("BOTTOMPADDING", (0,0), (-1,0), 10),
    ]))

    from datetime import datetime

    elements = []

# Title
    elements.append(Paragraph("CEAT TYRE CLAIM REPORT", title_style))
    elements.append(Spacer(1, 0.20 * inch))

# Report Details
    elements.append(Paragraph(f"<b>Customer Name:</b> {customer_name}", normal_style))
    elements.append(Paragraph(f"<b>Generated On:</b> {datetime.now().strftime('%d-%m-%Y %I:%M %p')}", normal_style))
    elements.append(Paragraph(f"<b>Total Claims:</b> {len(data)-1}", normal_style))

    elements.append(Spacer(1, 0.25 * inch))
# Table
    elements.append(table)

    pdf.build(elements)

    return "Claim_History.pdf"