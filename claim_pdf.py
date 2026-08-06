from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)
from reportlab.lib.units import inch


def generate_claim_pdf(claim):

    file_name = f"Claim_{claim[2]}.pdf"

    pdf = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    elements = []

    logo = Image("assets/ceat_logo.png", width=1.2*inch, height=0.45*inch)
    title = Paragraph(
    "<font size=20><b>TYRE CLAIM REPORT</b></font>",
    styles["Title"]
     )

    header = Table(
    [[logo, title]],
    colWidths=[1.2*inch, 4.8*inch]
     )

    header.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("ALIGN", (1, 0), (1, 0), "LEFT"),
    ("LEFTPADDING", (1, 0), (1, 0), 2),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
     ]))

    elements.append(header)
    elements.append(Spacer(1, 0.2*inch))

    claim_loss = float(claim[17])
    gst = claim_loss * 0.18
    total = claim_loss + gst

    data = [
        ["Field", "Value"],
        ["Docket Number", claim[2]],
        ["Docket Date", claim[3]],
        ["Customer Name", claim[8]],
        ["Material", claim[10]],
        ["Serial Number", claim[11]],
        ["Disposition", claim[12]],
        ["Defect", claim[14]],
        ["Claim Loss", f"₹{claim_loss:,.2f}"],
        ["GST (18%)", f"₹{gst:,.2f}"],
        ["Total Payable", f"₹{total:,.2f}"],
    ]

    table = Table(data, colWidths=[3 * inch, 3.5* inch])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0053AE")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 1), (0, -1), colors.lightgrey),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
    ]))

    elements.append(table)

    pdf.build(elements)

    return file_name