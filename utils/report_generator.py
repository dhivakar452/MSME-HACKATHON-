import io
import pandas as pd
from typing import List, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_pdf_report(month: str, records: List[Any], username: str) -> bytes:
    """
    Generates a beautifully structured PDF monthly performance report for the MSME factory.
    Uses reportlab to draw tables, text, and summaries.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette definition
    primary_color = colors.HexColor("#1e3d59")    # Sleek Navy Blue
    secondary_color = colors.HexColor("#17b978")  # Forest Green accent
    neutral_light = colors.HexColor("#f5f5f5")    # Soft gray background
    text_color = colors.HexColor("#333333")
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'ReportSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#777777"),
        spaceAfter=20
    )
    
    h2_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        leading=20,
        textColor=primary_color,
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=text_color
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        textColor=colors.white,
        fontName='Helvetica-Bold'
    )
    
    table_body_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        textColor=text_color
    )

    story = []
    
    # --- Header Banner ---
    story.append(Paragraph("MSME Smart Decision Support System", title_style))
    story.append(Paragraph(f"Monthly Performance Report — Month of <b>{month}</b> | Prepared for: <b>{username}</b>", subtitle_style))
    story.append(Spacer(1, 10))
    
    # --- Aggregate Calculations ---
    data_list = []
    for r in records:
        if hasattr(r, "__dict__"):
            d = {col.name: getattr(r, col.name) for col in r.__table__.columns}
        else:
            d = dict(r)
        data_list.append(d)
        
    df = pd.DataFrame(data_list)
    
    total_sales = df['sales'].sum()
    total_production = df['production'].sum()
    total_electricity = df['electricity_bill'].sum()
    total_raw_material = df['raw_material_cost'].sum()
    total_salary = df['salary'].sum()
    total_profit = df['profit'].sum()
    avg_downtime = df['machine_downtime'].mean()
    avg_running = df['machine_running_hours'].mean()
    
    # --- Section: Executive Summary ---
    story.append(Paragraph("Executive Summary", h2_style))
    summary_text = (
        f"This report outlines the operational metrics and business performance recorded during the month of {month}. "
        f"A total sales volume of <b>${total_sales:,.2f}</b> was generated, producing a net profit of <b>${total_profit:,.2f}</b>. "
        f"Factory machines operated for an average of <b>{avg_running:.1f} hours/day</b>, experiencing an average daily downtime of <b>{avg_downtime:.1f} hours</b>. "
        f"Key resource costs included raw materials at <b>${total_raw_material:,.2f}</b>, labor salaries at <b>${total_salary:,.2f}</b>, and electricity charges totaling <b>${total_electricity:,.2f}</b>."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 15))
    
    # --- Section: Key Financial & Operational Aggregates ---
    story.append(Paragraph("Monthly Aggregates", h2_style))
    
    summary_table_data = [
        [Paragraph("<b>Metric Description</b>", table_header_style), Paragraph("<b>Monthly Aggregate Value</b>", table_header_style)],
        [Paragraph("Total Sales Revenue", table_body_style), Paragraph(f"${total_sales:,.2f}", table_body_style)],
        [Paragraph("Total Output Produced", table_body_style), Paragraph(f"{total_production:,.1f} Units", table_body_style)],
        [Paragraph("Raw Material Expenses", table_body_style), Paragraph(f"${total_raw_material:,.2f}", table_body_style)],
        [Paragraph("Labor & Salaries Expenses", table_body_style), Paragraph(f"${total_salary:,.2f}", table_body_style)],
        [Paragraph("Electricity & Utilities Bills", table_body_style), Paragraph(f"${total_electricity:,.2f}", table_body_style)],
        [Paragraph("Average Machine Operating Time", table_body_style), Paragraph(f"{avg_running:.1f} Hours/Day", table_body_style)],
        [Paragraph("Average Machine Downtime Logged", table_body_style), Paragraph(f"{avg_downtime:.1f} Hours/Day", table_body_style)],
        [Paragraph("<b>Net Monthly Operating Profit</b>", table_body_style), Paragraph(f"<b>${total_profit:,.2f}</b>", table_body_style)]
    ]
    
    summary_table = Table(summary_table_data, colWidths=[3.5*inch, 3.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, neutral_light]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 15))
    
    # --- Section: Daily Breakdown Table ---
    story.append(Paragraph("Daily Metrics Record Summary", h2_style))
    
    breakdown_headers = [
        Paragraph("<b>Date</b>", table_header_style),
        Paragraph("<b>Sales</b>", table_header_style),
        Paragraph("<b>Prod</b>", table_header_style),
        Paragraph("<b>Elec</b>", table_header_style),
        Paragraph("<b>Mat. Cost</b>", table_header_style),
        Paragraph("<b>Run Hrs</b>", table_header_style),
        Paragraph("<b>Down Hrs</b>", table_header_style),
        Paragraph("<b>Profit</b>", table_header_style),
    ]
    
    breakdown_table_data = [breakdown_headers]
    
    # Sorting by date to present chronological logs
    sorted_df = df.sort_values(by='date')
    for _, row in sorted_df.iterrows():
        breakdown_table_data.append([
            Paragraph(str(row['date']), table_body_style),
            Paragraph(f"${row['sales']:,.0f}", table_body_style),
            Paragraph(f"{row['production']:.0f}", table_body_style),
            Paragraph(f"${row['electricity_bill']:,.0f}", table_body_style),
            Paragraph(f"${row['raw_material_cost']:,.0f}", table_body_style),
            Paragraph(f"{row['machine_running_hours']:.1f}", table_body_style),
            Paragraph(f"{row['machine_downtime']:.1f}", table_body_style),
            Paragraph(f"${row['profit']:,.0f}", table_body_style),
        ])
        
    # Standardize column widths to fit on 1 page width (approx 7 inches total)
    col_widths = [1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 0.9*inch, 0.8*inch, 0.8*inch, 1.1*inch]
    
    breakdown_table = Table(breakdown_table_data, colWidths=col_widths)
    breakdown_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, neutral_light]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    
    story.append(breakdown_table)
    story.append(Spacer(1, 20))
    
    # --- Footer disclaimer ---
    footer_text = Paragraph(
        "<font size='8' color='#999999'>Report generated dynamically by the MSME Smart Decision Support System. "
        "Calculations are based on operational logs recorded in SQLite and processed via Pandas analytical pipelines.</font>", 
        body_style
    )
    story.append(footer_text)

    # Build the document
    doc.build(story)
    
    pdf_output = buffer.getvalue()
    buffer.close()
    return pdf_output
