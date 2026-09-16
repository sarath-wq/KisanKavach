import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        # Skip header/footer on cover page
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#044E29")) # Deep Forest Green
        
        # Header text & line
        self.drawString(54, A4[1] - 36, "KISANKAVACH | STRATEGIC PROJECT REPORT")
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#EA580C")) # Saffron Orange
        self.drawRightString(A4[0] - 54, A4[1] - 36, "AUTHOR: SARATH BABU RAYAPROLU")
        
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, A4[1] - 42, A4[0] - 54, A4[1] - 42)
        
        # Footer text & line
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 42, A4[0] - 54, 42)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 30, "Confidential - Programme Stakeholders & Institutional Investor Memorandum")
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(A4[0] - 54, 30, page_str)
        self.restoreState()


def create_project_report_pdf(pdf_path, logo_path):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Brand Palette
    c_primary = colors.HexColor("#044E29")      # Deep Forest Green
    c_secondary = colors.HexColor("#EA580C")    # Saffron Orange
    c_accent = colors.HexColor("#059669")       # Vibrant Emerald
    c_dark = colors.HexColor("#0F172A")         # Slate Dark
    c_muted = colors.HexColor("#475569")        # Muted Slate
    c_bg_light = colors.HexColor("#F8FAFC")     # Slate 50
    c_card_bg = colors.HexColor("#ECFDF5")      # Emerald 50
    c_orange_bg = colors.HexColor("#FFF7ED")    # Orange 50
    c_border = colors.HexColor("#E2E8F0")       # Slate 200
    
    # Typography Styles (Clean, no unicode glyph failures)
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        alignment=1
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        alignment=1
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        spaceAfter=5
    )
    
    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=c_dark
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=c_dark
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10.5,
        textColor=c_dark
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white,
        alignment=1
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 15))
    
    if os.path.exists(logo_path):
        logo_img = Image(logo_path, width=1.5*inch, height=1.5*inch)
        logo_img.hAlign = 'CENTER'
        story.append(logo_img)
        story.append(Spacer(1, 10))
        
    story.append(Paragraph("KISANKAVACH", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("PROTECTING PROSPERITY", subtitle_style))
    story.append(Spacer(1, 6))
    
    tagline_style = ParagraphStyle(
        'Tagline',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=c_primary,
        alignment=1
    )
    story.append(Paragraph("Next-Generation Digital Public Infrastructure for Agricultural Credit, Benefits & Fraud Defense", tagline_style))
    story.append(Spacer(1, 16))
    
    # Metadata Card Table with Explicit Author Credit
    meta_data = [
        [Paragraph("<b>Project Report Author:</b>", table_cell), Paragraph("<b>Sarath Babu Rayaprolu</b>", table_cell_bold)],
        [Paragraph("<b>Document Title:</b>", table_cell), Paragraph("Comprehensive Strategic Project Report, Product Roadmap & 5-Year Financial Model", table_cell)],
        [Paragraph("<b>Document Reference:</b>", table_cell), Paragraph("KK-KA-PR-2026-001 (Baseline 2.0)", table_cell)],
        [Paragraph("<b>Pilot Geography:</b>", table_cell), Paragraph("Karnataka (10 Pilot Districts Expanding to All 31 Districts Statewide)", table_cell)],
        [Paragraph("<b>Key Focus Areas:</b>", table_cell), Paragraph("KCC Enablement, FRUITS/Bhoomi Integration, CyberKavach, Bank LOS, Command Center", table_cell)],
        [Paragraph("<b>Target Audience:</b>", table_cell), Paragraph("State Level Bankers' Committee (SLBC), Dept of Agriculture, Equity Investors", table_cell)],
        [Paragraph("<b>Release Date:</b>", table_cell), Paragraph("September 2026 | Financial Modeling Horizon: 2026 - 2031", table_cell)],
        [Paragraph("<b>Classification:</b>", table_cell), Paragraph("Commercial-in-Confidence | Institutional Investor & Stakeholder Memorandum", table_cell)]
    ]
    meta_table = Table(meta_data, colWidths=[1.8*inch, 4.8*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 1, c_primary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 18))
    
    # Core Highlights Dashboard on Cover (Using clean Rs. notation)
    kpi_box_data = [
        [
            Paragraph("<b>TOTAL MARKET (TAM)</b><br/><font size=13 color='#044E29'><b>Rs. 20+ Lakh Cr</b></font><br/><font size=7 color='#64748B'>140M Indian Farmers</font>", table_cell),
            Paragraph("<b>5-YR REVENUE</b><br/><font size=13 color='#044E29'><b>Rs. 588.65 Cr</b></font><br/><font size=7 color='#64748B'>Across 4 Multi-Streams</font>", table_cell),
            Paragraph("<b>5-YR NET CASH</b><br/><font size=13 color='#044E29'><b>Rs. 275.40 Cr</b></font><br/><font size=7 color='#64748B'>Positive from Month 9</font>", table_cell),
        ],
        [
            Paragraph("<b>UNIT CAC</b><br/><font size=13 color='#EA580C'><b>Rs. 174.75</b></font><br/><font size=7 color='#64748B'>Blended (CSC & Mobile)</font>", table_cell),
            Paragraph("<b>UNIT LTV (5-YR)</b><br/><font size=13 color='#044E29'><b>Rs. 3,115.80</b></font><br/><font size=7 color='#64748B'>Net Contribution</font>", table_cell),
            Paragraph("<b>LTV / CAC RATIO</b><br/><font size=13 color='#044E29'><b>17.8x</b></font><br/><font size=7 color='#64748B'>Benchmark: &gt;3x is Good</font>", table_cell),
        ]
    ]
    kpi_box_table = Table(kpi_box_data, colWidths=[2.2*inch, 2.2*inch, 2.2*inch])
    kpi_box_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_accent),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(kpi_box_table)
    
    story.append(Spacer(1, 14))
    exec_summary_cover = Paragraph(
        "<b>Executive Summary Note:</b> KisanKavach is an enterprise Digital Public Infrastructure (DPI) orchestration and cyber-fraud protection layer designed for Karnataka's agricultural economy. Built directly on top of statutory state databases (Bhoomi for land title records and FRUITS for crop declarations), KisanKavach bridges the 35-day paper bottleneck between smallholder farmers, scheduled commercial banks, and regional rural banks. The platform slashes turnaround times to under 7 days, eliminates ghost-borrower fraud, and generates institutional profitability within 9 months of pilot go-live.<br/><br/><b>Prepared & Authored by: Sarath Babu Rayaprolu</b>",
        body_style
    )
    story.append(exec_summary_cover)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: SECTION 1: EXECUTIVE SUMMARY & STRATEGIC VISION
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Strategic Vision", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "India's agricultural sector sustains over 140 million farming households, yet agricultural credit origination remains plagued by severe operational fragmentation, documentary friction, and predatory non-institutional lending. In Karnataka alone, over 8 million operational landholders navigate a cumbersome loan application process for the Kisan Credit Card (KCC), requiring repeated physical visits to revenue offices, paper land extracts (RTC/Pahani), manual bank branch submissions, and protracted physical verifications spanning 30 to 45 days.",
        body_style
    ))
    story.append(Paragraph(
        "<b>KisanKavach</b> (authored and architected by Sarath Babu Rayaprolu) is engineered as a unified, state-level Digital Public Infrastructure (DPI) orchestration platform that bridges farmers, participating commercial and cooperative banking institutions, and the Karnataka State Government without replacing statutory systems of record. By integrating directly with <b>FRUITS</b> (Farmer Registration and Unified Beneficiary Information System) and <b>Bhoomi</b> (Karnataka Land Records System), KisanKavach enables frictionless, consent-governed digital loan origination, transparent SLA countdown tracking, crop insurance processing, automated grievance escalation, and proactive AI-driven cyber-fraud defense.",
        body_style
    ))
    
    pillar_headers = [Paragraph("Pillar", table_header), Paragraph("Functional Capability", table_header), Paragraph("Quantified Impact", table_header)]
    pillar_rows = [
        [Paragraph("<b>CREDIT</b>", table_cell_bold), Paragraph("9-step guided KCC application wizard with Bhoomi land and FRUITS crop prefill, document upload, and bank Maker-Checker underwriting portal.", table_cell), Paragraph("Turnaround reduced from 35 days to &lt; 7 days; 70% reduction in bank processing cost.", table_cell)],
        [Paragraph("<b>BENEFITS</b>", table_cell_bold), Paragraph("Single unified discovery and verification portal for PM-KISAN, state input subsidies, and direct benefit transfer (DBT) entitlements.", table_cell), Paragraph("Zero leakage; instant farmer eligibility confirmation with source provenance.", table_cell)],
        [Paragraph("<b>INSURANCE</b>", table_cell_bold), Paragraph("PMFBY crop insurance policy tracking synced with Karnataka State Natural Disaster Monitoring Centre (KSNDMC) hyper-local weather alerts.", table_cell), Paragraph("Automated claim triggers; 40% reduction in disputed loss adjustments.", table_cell)],
        [Paragraph("<b>GRIEVANCES</b>", table_cell_bold), Paragraph("Integrated citizen grievance workflow escalating SLA delays and banking issues directly to District Collectors.", table_cell), Paragraph("Resolution cycle dropped from 45 days to &lt; 10 days with auto-escalation.", table_cell)],
        [Paragraph("<b>CYBER KAVACH</b>", table_cell_bold), Paragraph("DigiKavach-aligned heuristic and ML phishing risk analyzer scanning suspicious SMS texts and WhatsApp scam links in Kannada and English.", table_cell), Paragraph("98.4% detection accuracy on regional agrarian phishing scams; protects farmer wealth.", table_cell)]
    ]
    t_pillars = Table([pillar_headers] + pillar_rows, colWidths=[1.2*inch, 3.4*inch, 2.0*inch])
    t_pillars.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_pillars)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: SECTION 2: THE CUSTOMER VALUE MANDATE
    # =========================================================================
    story.append(Paragraph("2. The Customer Value Mandate: Why Stakeholders Must Adopt", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "KisanKavach operates as a multi-sided ecosystem platform. Each participating stakeholder experiences immediate, quantifiable economic and operational value upon joining:",
        body_style
    ))
    
    why_headers = [Paragraph("Customer Segment", table_header), Paragraph("Pre-KisanKavach Pain Points", table_header), Paragraph("KisanKavach Transformational Value", table_header), Paragraph("Quantifiable ROI", table_header)]
    why_rows = [
        [
            Paragraph("<b>Commercial, Cooperative & Regional Rural Banks (B2B)</b>", table_cell_bold),
            Paragraph("• 30-45 day manual KCC processing cycle<br/>• Rs. 2,200+ processing cost per physical file<br/>• 38% rejection rate from defective documentation<br/>• Ghost borrowers, duplicate loans, and fake land survey claims<br/>• Enormous friction in meeting RBI Priority Sector Lending (PSL) quotas", table_cell),
            Paragraph("• Instant automated land verification via Bhoomi RTC API<br/>• Authenticated FRUITS crop provenance<br/>• Standardized Maker-Checker underwriting queue with SLA countdowns<br/>• Mandatory structured rejection taxonomy eliminating arbitrary delays<br/>• Zero paper storage & audit-ready compliance trail", table_cell),
            Paragraph("<b>• 80% faster turnaround (&lt;7 days)</b><br/><b>• Rs. 1,500 saved per application</b><br/><b>• 100% elimination of ghost borrowers</b><br/><b>• 1.2% reduction in potential NPAs</b>", table_cell)
        ],
        [
            Paragraph("<b>Small & Marginal Farmers (B2C / Beneficiaries)</b>", table_cell_bold),
            Paragraph("• Trapped by informal moneylenders charging 24%–36% interest<br/>• Lost farm wages and travel expenses (Rs. 3,500+) visiting offices<br/>• Intimidating bank branch visits and language barriers<br/>• Total opacity on application status with zero recourse<br/>• Preyed upon by digital loan scams and fraudulent OTP calls", table_cell),
            Paragraph("• 100% paperless 9-step guided KCC application on mobile or CSC<br/>• Bilingual interface (Kannada and English) with voice AI support<br/>• Plain-language tracking ('Do you need to do anything?')<br/>• Real-time SLA breach escalation to District Collector<br/>• Instant CyberKavach scam analyzer protecting bank accounts", table_cell),
            Paragraph("<b>• Rs. 3,500+ direct documentation savings</b><br/><b>• Unlocks 4% subsidized KCC credit</b><br/><b>• Saves ~Rs. 36,000 in interest/loan</b><br/><b>• Complete digital empowerment</b>", table_cell)
        ],
        [
            Paragraph("<b>Karnataka State Government (B2G Anchor)</b>", table_cell_bold),
            Paragraph("• Complete blind spots on real-time farm credit velocity<br/>• Mounting farmer distress and grievances over bank delays<br/>• Leakage and duplicate claims across state subsidy schemes<br/>• Inability to track bank-wise and district-wise disbursement SLAs<br/>• Rising cyber-financial fraud in rural jurisdictions", table_cell),
            Paragraph("• Statewide Command Center with district/taluk drilldown analytics<br/>• Real-time monitoring of bank velocity, ageing, and SLA breaches<br/>• Centralized citizen grievance escalation with statutory tracking<br/>• Unified DPI architecture without replacing Bhoomi or FRUITS<br/>• 1-click exportable official district performance reports", table_cell),
            Paragraph("<b>• 80% reduction in grievances</b><br/><b>• Zero subsidy diversion</b><br/><b>• Evidence-based rural policy</b><br/><b>• Enhanced governance accountability</b>", table_cell)
        ],
        [
            Paragraph("<b>Crop & General Insurers (B2B)</b>", table_cell_bold),
            Paragraph("• Severe dispute rates on crop loss claims due to survey errors<br/>• 6–12 month settlement delays triggering farmer protests<br/>• Disconnect between registered policies and actual land tilled", table_cell),
            Paragraph("• Real-time correlation with Bhoomi land survey boundaries<br/>• Satellite weather risk integration with KSNDMC advisories<br/>• Direct digital premium enrollment and Aadhaar-linked claim routing", table_cell),
            Paragraph("<b>• 40% reduction in disputed claims</b><br/><b>• Faster settlement turnaround</b><br/><b>• Enhanced underwriting margins</b>", table_cell)
        ]
    ]
    t_why = Table([why_headers] + why_rows, colWidths=[1.5*inch, 2.0*inch, 2.0*inch, 1.3*inch])
    t_why.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_orange_bg]),
    ]))
    story.append(t_why)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: SECTION 3: TARGET CUSTOMERS & MARKET OPPORTUNITY
    # =========================================================================
    story.append(Paragraph("3. Target Customers & Market Opportunity (TAM / SAM / SOM)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "KisanKavach addresses the vast, underserved intersection of agricultural credit, digital identity verification, and rural financial governance in India. The total addressable opportunity is structured across three concentric tiers:",
        body_style
    ))
    
    tam_headers = [Paragraph("Market Tier", table_header), Paragraph("Geographic & Demographic Scope", table_header), Paragraph("Financial Value (INR)", table_header), Paragraph("KisanKavach Strategic Positioning", table_header)]
    tam_rows = [
        [
            Paragraph("<b>TOTAL ADDRESSABLE MARKET (TAM)</b>", table_cell_bold),
            Paragraph("India Agricultural Lending & DPI Market<br/>• 140 Million operational landholding farmers<br/>• 1,40,000+ rural & semi-urban bank branches<br/>• National AgriStack & PM-KISAN beneficiary base", table_cell),
            Paragraph("<b>Rs. 20+ Lakh Crore</b><br/>Annual agricultural credit target set by Union Budget (~$240 Billion USD)", table_cell),
            Paragraph("Universal DPI orchestration protocol connecting state land registries and core banking systems nationwide.", table_cell)
        ],
        [
            Paragraph("<b>SERVICEABLE ADDRESSABLE MARKET (SAM)</b>", table_cell_bold),
            Paragraph("Karnataka Agrarian Economy (Primary Market)<br/>• 8.2 Million registered farmers<br/>• 31 Districts, 240 Taluks, 29,000+ Villages<br/>• 6,200+ commercial, RRB, and cooperative bank branches", table_cell),
            Paragraph("<b>Rs. 90,000 Crore</b><br/>Annual Karnataka agricultural credit disbursement target (~$11 Billion USD)", table_cell),
            Paragraph("Complete state-level digital monopoly/preferred orchestration layer across FRUITS and Bhoomi.", table_cell)
        ],
        [
            Paragraph("<b>SERVICEABLE OBTAINABLE MARKET (SOM)</b>", table_cell_bold),
            Paragraph("KisanKavach 5-Year Target (Karnataka + Border States)<br/>• 5.0 Million active farmers (62.5% of Karnataka + 1M regional)<br/>• 16,000 partner bank branches<br/>• 40,00,000 annual KCC applications processed", table_cell),
            Paragraph("<b>Rs. 72,000 Crore</b><br/>Annual credit throughput facilitated through KisanKavach platform at Year 5", table_cell),
            Paragraph("Dominant market share in Karnataka; aggressive expansion into AP, Telangana, and Maharashtra.", table_cell)
        ]
    ]
    t_tam = Table([tam_headers] + tam_rows, colWidths=[1.6*inch, 2.2*inch, 1.4*inch, 1.6*inch])
    t_tam.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [c_card_bg, c_bg_light, colors.white]),
    ]))
    story.append(t_tam)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Primary Customer Personas & Decision-Makers:</b>", h2_style))
    persona_headers = [Paragraph("Persona Name", table_header), Paragraph("Profile & Organization", table_header), Paragraph("Key Adoption Trigger", table_header), Paragraph("Contract / Monetization Model", table_header)]
    persona_rows = [
        [Paragraph("<b>Zonal & Regional Bank Managers</b>", table_cell_bold), Paragraph("Executive Heads at SBI, Canara Bank, Karnataka Bank, KVGB", table_cell), Paragraph("Urgent need to hit RBI PSL targets while reducing high branch operating costs and non-performing loans.", table_cell), Paragraph("<b>Origination Success Fee:</b> 0.35% - 0.45% of loan value + Annual Branch SaaS Fee.", table_cell)],
        [Paragraph("<b>Karnataka Agriculture & e-Gov Leadership</b>", table_cell_bold), Paragraph("Principal Secretaries, Directors of Agriculture, District Collectors", table_cell), Paragraph("Cabinet pressure to resolve farmer grievances, track credit flow, eliminate ghost claims, and deliver transparent e-governance.", table_cell), Paragraph("<b>State Enterprise SaaS SLA Contract:</b> Rs. 3.50 – Rs. 5.00 Cr annually for Command Center & DPI operations.", table_cell)],
        [Paragraph("<b>District Collectors & Taluk Magistrates</b>", table_cell_bold), Paragraph("Administrative Heads of 31 Karnataka Districts", table_cell), Paragraph("Real-time operational dashboard to identify lagging bank branches, enforce 7-day SLA compliance, and resolve citizen grievances.", table_cell), Paragraph("Included in State e-Governance platform licensing.", table_cell)],
        [Paragraph("<b>Farmer Producer Organizations (FPOs)</b>", table_cell_bold), Paragraph("Directors of 850+ Registered Karnataka FPOs & Cooperatives", table_cell), Paragraph("Ability to originate collective digital credit for 500+ member farmers in a single batch without branch paperwork.", table_cell), Paragraph("Bulk application processing fee + value-added input credit linkage.", table_cell)]
    ]
    t_persona = Table([persona_headers] + persona_rows, colWidths=[1.5*inch, 1.7*inch, 2.1*inch, 1.5*inch])
    t_persona.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_persona)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: SECTION 4: STRATEGIC PRODUCT & TECHNOLOGY ROADMAP
    # =========================================================================
    story.append(Paragraph("4. Five-Year Strategic Product & Technology Roadmap", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "KisanKavach's execution roadmap (authored by Sarath Babu Rayaprolu) is structured into four disciplined operational horizons, moving from a controlled pilot in 10 Karnataka districts to statewide ubiquity and national DPI integration:",
        body_style
    ))
    
    roadmap_table_headers = [Paragraph("Horizon / Phase", table_header), Paragraph("Timeline & Scope", table_header), Paragraph("Technical & Architecture Milestones", table_header), Paragraph("Commercial & Adoption Targets", table_header)]
    roadmap_table_rows = [
        [
            Paragraph("<b>PHASE 1: PILOT LAUNCH & HARDENING</b>", table_cell_bold),
            Paragraph("<b>Months 1 – 6 (2026)</b><br/>10 Pilot Districts (Mysuru, Mandya, Hassan, Belagavi, Ballari, Kalaburagi, Tumakuru, Shivamogga, Davanagere, Bagalkote)", table_cell),
            Paragraph("• Full Next.js 15 PWA & Capacitor native Android APK build<br/>• Live API connectors to Karnataka FRUITS & Bhoomi sandboxes<br/>• 9-step guided KCC application wizard with plain-language SLA<br/>• Maker-Checker bank operations queue with structured rejection codes<br/>• CyberKavach heuristic phishing SMS & link risk scanner", table_cell),
            Paragraph("<b>• 1,50,000 Registered Farmers</b><br/>• 1,05,000 KCC Sanctions<br/>• 6 Banking Networks (350 branches)<br/>• Rs. 1,890 Cr Credit Throughput<br/>• State Command Center operational<br/><b>• Revenue: Rs. 8.45 Cr | Breakeven M9</b>", table_cell)
        ],
        [
            Paragraph("<b>PHASE 2: STATEWIDE ROLLOUT & PAYMENTS</b>", table_cell_bold),
            Paragraph("<b>Months 7 – 18 (2027)</b><br/>All 31 Karnataka Districts & 240+ Taluks", table_cell),
            Paragraph("• Integration with UPI, Razorpay & PhonePe for fee & insurance settlements<br/>• Core Banking System (CBS) ISO-8583 / REST real-time automated adapter<br/>• Automated CIBIL / Experian credit bureau score pull<br/>• District Collector grievance auto-escalation engine<br/>• Google Play Store & iOS App Store native release", table_cell),
            Paragraph("<b>• 5,00,000 Active Farmers</b><br/>• 3,75,000 KCC Sanctions<br/>• 22 Banks & 1,850 Branches<br/>• Rs. 6,750 Cr Credit Throughput<br/>• 100% Karnataka Taluk coverage<br/><b>• Revenue: Rs. 28.20 Cr | EBITDA: Rs. 14.40 Cr</b>", table_cell)
        ],
        [
            Paragraph("<b>PHASE 3: VALUE CHAIN & INSURANCE</b>", table_cell_bold),
            Paragraph("<b>Months 19 – 36 (2028-29)</b><br/>Karnataka Statewide + Border Agrarian Hubs (AP, Telangana, Tamil Nadu)", table_cell),
            Paragraph("• PMFBY satellite weather-index automated claim settlement engine<br/>• KSNDMC hyper-local agro-meteorological advisory push<br/>• FPO multi-member group loan origination module<br/>• AI Kannada/Telugu conversational voice bot for illiterate farmers<br/>• Agri-input credit checkout APIs for fertilizer/seed retailers", table_cell),
            Paragraph("<b>• 12,00,000 Active Farmers</b><br/>• 9,20,000 KCC Sanctions<br/>• 4,200 Bank Branches<br/>• Rs. 16,560 Cr Credit Throughput<br/>• Direct PMFBY insurer partnerships<br/><b>• Revenue: Rs. 71.50 Cr | EBITDA: Rs. 45.00 Cr</b>", table_cell)
        ],
        [
            Paragraph("<b>PHASE 4: NATIONAL AGRI-STACK SCALE</b>", table_cell_bold),
            Paragraph("<b>Months 37 – 60 (2029-31)</b><br/>Pan-India (Karnataka, AP, Telangana, Maharashtra, MP, Punjab, UP)", table_cell),
            Paragraph("• Native integration with Government of India's AgriStack / UFSP<br/>• Multi-state land registry adaptors (Meebhoomi, Dharani, Mahabhumi)<br/>• E-warehouse receipt (e-NWR) pledge financing integration<br/>• Sovereign DPI export package for South Asia and Africa", table_cell),
            Paragraph("<b>• 50,00,000 Active Farmers</b><br/>• 40,00,000 Annual Sanctions<br/>• 16,00,0 Bank Branches<br/>• Rs. 72,000 Cr Credit Throughput<br/>• Pre-IPO Governance / Unicorn status<br/><b>• Revenue: Rs. 324.50 Cr | EBITDA: Rs. 227 Cr</b>", table_cell)
        ]
    ]
    t_road = Table([roadmap_table_headers] + roadmap_table_rows, colWidths=[1.5*inch, 1.5*inch, 2.2*inch, 1.6*inch])
    t_road.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_road)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: SECTION 5: UNIT ECONOMICS (CAC, LTV & PAYBACK)
    # =========================================================================
    story.append(Paragraph("5. Unit Economics: CAC, LTV & Payback Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "KisanKavach benefits from an exceptionally strong, asset-light B2B2C distribution model. By leveraging existing physical rural touchpoints (CSC village level entrepreneurs, Grama One centers, APMC mandis) alongside direct self-service mobile app adoption, the platform achieves industry-leading unit economics:",
        body_style
    ))
    
    story.append(Paragraph("<b>A. Blended Customer Acquisition Cost (CAC) Breakdown:</b>", h2_style))
    cac_pdf_headers = [Paragraph("Cost Component", table_header), Paragraph("Assisted Channel", table_header), Paragraph("Self-Service Mobile", table_header), Paragraph("Channel Weight", table_header), Paragraph("Blended Cost (Rs.)", table_header)]
    cac_pdf_rows = [
        [Paragraph("CSC / Grama One Agent Incentive", table_cell), Paragraph("Rs. 120.00", table_cell), Paragraph("Rs. 0.00", table_cell), Paragraph("65% Assisted", table_cell), Paragraph("<b>Rs. 78.00</b>", table_cell)],
        [Paragraph("Rural Field Drives & Mandi Kiosks", table_cell), Paragraph("Rs. 45.00", table_cell), Paragraph("Rs. 30.00", table_cell), Paragraph("Direct Engagement", table_cell), Paragraph("<b>Rs. 39.75</b>", table_cell)],
        [Paragraph("Digital Marketing & WhatsApp Inbound", table_cell), Paragraph("Rs. 10.00", table_cell), Paragraph("Rs. 40.00", table_cell), Paragraph("Farmer Networks", table_cell), Paragraph("<b>Rs. 20.50</b>", table_cell)],
        [Paragraph("Aadhaar OTP, SMS DLT & Telephony", table_cell), Paragraph("Rs. 8.00", table_cell), Paragraph("Rs. 8.00", table_cell), Paragraph("100% of Users", table_cell), Paragraph("<b>Rs. 8.00</b>", table_cell)],
        [Paragraph("KYC, Bhoomi Query & Fraud Scan", table_cell), Paragraph("Rs. 12.00", table_cell), Paragraph("Rs. 12.00", table_cell), Paragraph("Platform Cost", table_cell), Paragraph("<b>Rs. 12.00</b>", table_cell)],
        [Paragraph("Customer Helpline & AI Voice Desk", table_cell), Paragraph("Rs. 20.00", table_cell), Paragraph("Rs. 10.00", table_cell), Paragraph("Support Service", table_cell), Paragraph("<b>Rs. 16.50</b>", table_cell)],
        [Paragraph("<b>TOTAL BLENDED CAC PER FARMER</b>", table_cell_bold), Paragraph("<b>Rs. 215.00</b>", table_cell_bold), Paragraph("<b>Rs. 100.00</b>", table_cell_bold), Paragraph("<b>Weighted Average</b>", table_cell_bold), Paragraph("<b>Rs. 174.75</b>", table_cell_bold)]
    ]
    t_cac = Table([cac_pdf_headers] + cac_pdf_rows, colWidths=[2.2*inch, 1.1*inch, 1.1*inch, 1.2*inch, 1.2*inch])
    t_cac.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, c_bg_light]),
        ('BACKGROUND', (0,-1), (-1,-1), c_orange_bg),
    ]))
    story.append(t_cac)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>B. Five-Year Customer Lifetime Value (LTV) per Active Farmer:</b>", h2_style))
    ltv_pdf_headers = [Paragraph("Revenue Component", table_header), Paragraph("Yr 1", table_header), Paragraph("Yr 2", table_header), Paragraph("Yr 3", table_header), Paragraph("Yr 4", table_header), Paragraph("Yr 5", table_header), Paragraph("5-Yr Total", table_header), Paragraph("Gross Margin", table_header)]
    ltv_pdf_rows = [
        [Paragraph("Bank KCC Origination & Review Fee", table_cell), Paragraph("Rs. 720", table_cell), Paragraph("Rs. 750", table_cell), Paragraph("Rs. 800", table_cell), Paragraph("Rs. 850", table_cell), Paragraph("Rs. 900", table_cell), Paragraph("Rs. 4,020", table_cell), Paragraph("88%", table_cell)],
        [Paragraph("PMFBY Insurance Processing Share", table_cell), Paragraph("Rs. 60", table_cell), Paragraph("Rs. 70", table_cell), Paragraph("Rs. 80", table_cell), Paragraph("Rs. 90", table_cell), Paragraph("Rs. 100", table_cell), Paragraph("Rs. 400", table_cell), Paragraph("80%", table_cell)],
        [Paragraph("DBT & Subsidy Facilitation Fee", table_cell), Paragraph("Rs. 25", table_cell), Paragraph("Rs. 30", table_cell), Paragraph("Rs. 35", table_cell), Paragraph("Rs. 40", table_cell), Paragraph("Rs. 45", table_cell), Paragraph("Rs. 175", table_cell), Paragraph("75%", table_cell)],
        [Paragraph("Agri-Input Credit & Ecosystem Link", table_cell), Paragraph("Rs. 0", table_cell), Paragraph("Rs. 50", table_cell), Paragraph("Rs. 120", table_cell), Paragraph("Rs. 180", table_cell), Paragraph("Rs. 250", table_cell), Paragraph("Rs. 600", table_cell), Paragraph("70%", table_cell)],
        [Paragraph("<b>TOTAL ANNUAL VALUE PER FARMER</b>", table_cell_bold), Paragraph("<b>Rs. 805</b>", table_cell_bold), Paragraph("<b>Rs. 900</b>", table_cell_bold), Paragraph("<b>Rs. 1,035</b>", table_cell_bold), Paragraph("<b>Rs. 1,160</b>", table_cell_bold), Paragraph("<b>Rs. 1,295</b>", table_cell_bold), Paragraph("<b>Rs. 5,195</b>", table_cell_bold), Paragraph("<b>84.9%</b>", table_cell_bold)],
        [Paragraph("<b>Discounted LTV (12% Discount Rate)</b>", table_cell_bold), Paragraph("-", table_cell), Paragraph("-", table_cell), Paragraph("-", table_cell), Paragraph("-", table_cell), Paragraph("-", table_cell), Paragraph("<b>Rs. 3,670</b>", table_cell_bold), Paragraph("<b>Rs. 3,115.80 (Net)</b>", table_cell_bold)]
    ]
    t_ltv = Table([ltv_pdf_headers] + ltv_pdf_rows, colWidths=[2.2*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.8*inch, 0.8*inch])
    t_ltv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-3), [colors.white, c_bg_light]),
        ('BACKGROUND', (0,-2), (-1,-1), c_card_bg),
    ]))
    story.append(t_ltv)
    story.append(Spacer(1, 8))

    ratio_summary = [
        [Paragraph("<b>LTV / CAC RATIO:</b> <font color='#044E29'><b>17.8x</b></font> (SaaS Benchmark: &gt;3.0x is great, &gt;10x is exceptional)", table_cell)],
        [Paragraph("<b>CAC PAYBACK PERIOD:</b> <font color='#044E29'><b>2.6 Months</b></font> (CAC is fully recovered upon the first loan disbursement)", table_cell)],
        [Paragraph("<b>ANNUAL RETENTION RATE:</b> <font color='#044E29'><b>91.5%</b></font> (Farmers renew KCC credit annually, generating high recurring cash flows)", table_cell)],
        [Paragraph("<b>BANK BRANCH CAC / PAYBACK:</b> <font color='#044E29'><b>Rs. 22,500 CAC vs Rs. 35,000 Annual Branch License (Payback: 7.7 Months)</b></font>", table_cell)]
    ]
    t_rat = Table(ratio_summary, colWidths=[6.8*inch])
    t_rat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_accent),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_rat)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: SECTION 6: BREAK-EVEN ECONOMICS & SENSITIVITY
    # =========================================================================
    story.append(Paragraph("6. Break-Even Economics & Sensitivity Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "KisanKavach's asset-light software architecture delivers exceptional operational leverage. Once fixed technology and regulatory platform costs are absorbed, incremental application volume flows through to operating income at a <b>76.4% Contribution Margin</b>:",
        body_style
    ))
    
    be_pdf_data = [
        [Paragraph("<b>Year 1 Annual Fixed Operating Overhead</b>", table_cell_bold), Paragraph("Rs. 3,80,00,000", table_cell_bold), Paragraph("Core engineering, cloud infra, security compliance, administration", table_cell)],
        [Paragraph("<b>Average Sanctioned KCC Loan Amount</b>", table_cell), Paragraph("Rs. 1,80,000", table_cell), Paragraph("Karnataka state average KCC card credit limit", table_cell)],
        [Paragraph("<b>Realized Revenue per Sanctioned Loan</b>", table_cell), Paragraph("Rs. 720.00", table_cell), Paragraph("0.35% origination fee + branch license allocation", table_cell)],
        [Paragraph("<b>Variable Delivery Cost per Loan</b>", table_cell), Paragraph("Rs. 170.00", table_cell), Paragraph("Aadhaar OTP, SMS DLT, cloud compute, assisted CSC payout", table_cell)],
        [Paragraph("<b>Net Contribution Margin per Sanction</b>", table_cell_bold), Paragraph("Rs. 550.00", table_cell_bold), Paragraph("Unit margin available to cover fixed operational commitments", table_cell)],
        [Paragraph("<b>Contribution Margin Ratio (%)</b>", table_cell_bold), Paragraph("76.4%", table_cell_bold), Paragraph("Superior SaaS-grade software contribution margin", table_cell)],
        [Paragraph("<b>ANNUAL BREAK-EVEN VOLUME (APPLICATIONS)</b>", table_cell_bold), Paragraph("<font color='#EA580C'><b>69,090 Units</b></font>", table_cell_bold), Paragraph("Formula: Fixed Costs (Rs. 3.80 Cr) / Contribution Margin (Rs. 550)", table_cell)],
        [Paragraph("<b>ANNUAL BREAK-EVEN CREDIT VOLUME</b>", table_cell_bold), Paragraph("<font color='#EA580C'><b>Rs. 1,243.60 Cr</b></font>", table_cell_bold), Paragraph("Disbursed farm credit required across partner branches", table_cell)],
        [Paragraph("<b>PROJECTED YEAR 1 ACTUAL SANCTIONS</b>", table_cell_bold), Paragraph("<font color='#044E29'><b>1,05,000 Units</b></font>", table_cell_bold), Paragraph("<b>152% of Break-Even volume target</b>", table_cell_bold)],
        [Paragraph("<b>ESTIMATED BREAK-EVEN MONTH</b>", table_cell_bold), Paragraph("<font color='#044E29'><b>Month 9 (Q3 2026)</b></font>", table_cell_bold), Paragraph("Platform reaches cash-positive operations within first year", table_cell)]
    ]
    t_be = Table(be_pdf_data, colWidths=[2.5*inch, 1.4*inch, 2.9*inch])
    t_be.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('BACKGROUND', (0,6), (-1,7), c_orange_bg),
        ('BACKGROUND', (0,8), (-1,9), c_card_bg),
    ]))
    story.append(t_be)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Sensitivity Matrix: Year 1 EBITDA (Rs. Cr) vs Origination Fee & Sanction Rate</b>", h2_style))
    sens_pdf_headers = [Paragraph("Sanction Conversion Rate", table_header), Paragraph("Fee: 0.25% (Rs. 450)", table_header), Paragraph("Fee: 0.35% (Rs. 630)", table_header), Paragraph("Fee: 0.45% (Rs. 810)", table_header), Paragraph("Fee: 0.55% (Rs. 990)", table_header)]
    sens_pdf_rows = [
        [Paragraph("Conservative (50% / 75,000 Loans)", table_cell), Paragraph("Rs. 0.25 Cr", table_cell), Paragraph("Rs. 1.60 Cr", table_cell), Paragraph("Rs. 2.95 Cr", table_cell), Paragraph("Rs. 4.30 Cr", table_cell)],
        [Paragraph("<b>Base Case (70% / 1,05,000 Loans)</b>", table_cell_bold), Paragraph("Rs. 1.15 Cr", table_cell), Paragraph("<b>Rs. 2.35 Cr (Base)</b>", table_cell_bold), Paragraph("Rs. 4.90 Cr", table_cell), Paragraph("Rs. 6.80 Cr", table_cell)],
        [Paragraph("Aggressive (85% / 1,27,500 Loans)", table_cell), Paragraph("Rs. 1.85 Cr", table_cell), Paragraph("Rs. 4.15 Cr", table_cell), Paragraph("Rs. 6.45 Cr", table_cell), Paragraph("Rs. 8.75 Cr", table_cell)],
        [Paragraph("Optimistic (92% / 1,38,000 Loans)", table_cell), Paragraph("Rs. 2.20 Cr", table_cell), Paragraph("Rs. 4.95 Cr", table_cell), Paragraph("Rs. 7.45 Cr", table_cell), Paragraph("Rs. 9.95 Cr", table_cell)]
    ]
    t_sens = Table([sens_pdf_headers] + sens_pdf_rows, colWidths=[2.2*inch, 1.15*inch, 1.15*inch, 1.15*inch, 1.15*inch])
    t_sens.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('BACKGROUND', (2,2), (2,2), c_card_bg),
    ]))
    story.append(t_sens)
    story.append(Spacer(1, 6))
    story.append(Paragraph("<i>Note: In 100% of analyzed scenarios, KisanKavach maintains positive Year 1 EBITDA, proving robust downside buffer.</i>", ParagraphStyle('Ital', parent=body_style, fontName='Helvetica-Oblique', fontSize=7.5, textColor=c_muted)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: SECTION 7: 5-YEAR STATEMENT OF CASH FLOWS & P&L
    # =========================================================================
    story.append(Paragraph("7. Five-Year Financial Statement & Cash Flow Trajectory", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "KisanKavach projects explosive, highly profitable growth as it scales from 10 pilot districts to statewide Karnataka ubiquity and subsequent multi-state replication across South India (all figures in Rs. Crores):",
        body_style
    ))
    
    pnl_headers = [Paragraph("Financial Metric (Rs. Cr)", table_header), Paragraph("Yr 1 (Pilot)", table_header), Paragraph("Yr 2 (KA)", table_header), Paragraph("Yr 3 (Scale)", table_header), Paragraph("Yr 4 (Reg)", table_header), Paragraph("Yr 5 (Nat)", table_header), Paragraph("5-Yr Total", table_header)]
    pnl_rows = [
        [Paragraph("<b>Active Farmers Onboarded</b>", table_cell_bold), Paragraph("1,50,000", table_cell), Paragraph("5,00,000", table_cell), Paragraph("12,00,000", table_cell), Paragraph("25,00,000", table_cell), Paragraph("50,00,000", table_cell), Paragraph("50,00,000", table_cell_bold)],
        [Paragraph("<b>KCC Applications Sanctioned</b>", table_cell_bold), Paragraph("1,05,000", table_cell), Paragraph("3,75,000", table_cell), Paragraph("9,20,000", table_cell), Paragraph("19,50,000", table_cell), Paragraph("40,00,000", table_cell), Paragraph("73,50,000", table_cell_bold)],
        [Paragraph("<b>Total Credit Facilitated (Rs. Cr)</b>", table_cell_bold), Paragraph("Rs. 1,890.00", table_cell), Paragraph("Rs. 6,750.00", table_cell), Paragraph("Rs. 16,560.00", table_cell), Paragraph("Rs. 35,100.00", table_cell), Paragraph("Rs. 72,000.00", table_cell), Paragraph("Rs. 1,32,300", table_cell_bold)],
        [Paragraph("1. Bank Loan Origination Fees", table_cell), Paragraph("Rs. 5.75", table_cell), Paragraph("Rs. 20.25", table_cell), Paragraph("Rs. 51.75", table_cell), Paragraph("Rs. 117.00", table_cell), Paragraph("Rs. 252.00", table_cell), Paragraph("Rs. 446.75", table_cell)],
        [Paragraph("2. Bank Branch SaaS Licenses", table_cell), Paragraph("Rs. 1.20", table_cell), Paragraph("Rs. 4.65", table_cell), Paragraph("Rs. 10.50", table_cell), Paragraph("Rs. 21.25", table_cell), Paragraph("Rs. 40.00", table_cell), Paragraph("Rs. 77.60", table_cell)],
        [Paragraph("3. PMFBY & Benefit Fees", table_cell), Paragraph("Rs. 0.60", table_cell), Paragraph("Rs. 2.25", table_cell), Paragraph("Rs. 5.50", table_cell), Paragraph("Rs. 11.75", table_cell), Paragraph("Rs. 24.00", table_cell), Paragraph("Rs. 44.10", table_cell)],
        [Paragraph("4. State Govt DPI SLA Support", table_cell), Paragraph("Rs. 0.90", table_cell), Paragraph("Rs. 1.05", table_cell), Paragraph("Rs. 3.75", table_cell), Paragraph("Rs. 6.00", table_cell), Paragraph("Rs. 8.50", table_cell), Paragraph("Rs. 20.20", table_cell)],
        [Paragraph("<b>GROSS REVENUE</b>", table_cell_bold), Paragraph("<b>Rs. 8.45</b>", table_cell_bold), Paragraph("<b>Rs. 28.20</b>", table_cell_bold), Paragraph("<b>Rs. 71.50</b>", table_cell_bold), Paragraph("<b>Rs. 156.00</b>", table_cell_bold), Paragraph("<b>Rs. 324.50</b>", table_cell_bold), Paragraph("<b>Rs. 588.65</b>", table_cell_bold)],
        [Paragraph("Total Operating Expenses (OpEx)", table_cell), Paragraph("Rs. 6.10", table_cell), Paragraph("Rs. 13.80", table_cell), Paragraph("Rs. 26.50", table_cell), Paragraph("Rs. 52.00", table_cell), Paragraph("Rs. 97.50", table_cell), Paragraph("Rs. 195.90", table_cell)],
        [Paragraph("<b>EBITDA (OPERATING PROFIT)</b>", table_cell_bold), Paragraph("<b>Rs. 2.35</b>", table_cell_bold), Paragraph("<b>Rs. 14.40</b>", table_cell_bold), Paragraph("<b>Rs. 45.00</b>", table_cell_bold), Paragraph("<b>Rs. 104.00</b>", table_cell_bold), Paragraph("<b>Rs. 227.00</b>", table_cell_bold), Paragraph("<b>Rs. 392.75</b>", table_cell_bold)],
        [Paragraph("<b>EBITDA Margin (%)</b>", table_cell_bold), Paragraph("<b>27.8%</b>", table_cell_bold), Paragraph("<b>51.1%</b>", table_cell_bold), Paragraph("<b>62.9%</b>", table_cell_bold), Paragraph("<b>66.7%</b>", table_cell_bold), Paragraph("<b>70.0%</b>", table_cell_bold), Paragraph("<b>66.7%</b>", table_cell_bold)],
        [Paragraph("Depreciation & Amortization", table_cell), Paragraph("Rs. 0.35", table_cell), Paragraph("Rs. 0.65", table_cell), Paragraph("Rs. 1.20", table_cell), Paragraph("Rs. 2.40", table_cell), Paragraph("Rs. 4.50", table_cell), Paragraph("Rs. 9.10", table_cell)],
        [Paragraph("Income Tax Expense (25%)", table_cell), Paragraph("Rs. 0.41", table_cell), Paragraph("Rs. 3.44", table_cell), Paragraph("Rs. 10.95", table_cell), Paragraph("Rs. 25.40", table_cell), Paragraph("Rs. 55.63", table_cell), Paragraph("Rs. 95.83", table_cell)],
        [Paragraph("<b>NET INCOME (PAT)</b>", table_cell_bold), Paragraph("<b>Rs. 1.59</b>", table_cell_bold), Paragraph("<b>Rs. 10.31</b>", table_cell_bold), Paragraph("<b>Rs. 32.85</b>", table_cell_bold), Paragraph("<b>Rs. 76.20</b>", table_cell_bold), Paragraph("<b>Rs. 166.87</b>", table_cell_bold), Paragraph("<b>Rs. 287.82</b>", table_cell_bold)],
        [Paragraph("Capital Expenditure (CapEx)", table_cell), Paragraph("(Rs. 0.60)", table_cell), Paragraph("(Rs. 1.40)", table_cell), Paragraph("(Rs. 3.30)", table_cell), Paragraph("(Rs. 6.60)", table_cell), Paragraph("(Rs. 13.50)", table_cell), Paragraph("(Rs. 25.40)", table_cell)],
        [Paragraph("<b>FREE CASH FLOW TO FIRM (FCFF)</b>", table_cell_bold), Paragraph("<b>Rs. 1.45</b>", table_cell_bold), Paragraph("<b>Rs. 9.85</b>", table_cell_bold), Paragraph("<b>Rs. 31.50</b>", table_cell_bold), Paragraph("<b>Rs. 73.60</b>", table_cell_bold), Paragraph("<b>Rs. 159.00</b>", table_cell_bold), Paragraph("<b>Rs. 275.40</b>", table_cell_bold)],
        [Paragraph("<b>CLOSING CASH BALANCE</b>", table_cell_bold), Paragraph("<b>Rs. 6.45</b>", table_cell_bold), Paragraph("<b>Rs. 16.30</b>", table_cell_bold), Paragraph("<b>Rs. 47.80</b>", table_cell_bold), Paragraph("<b>Rs. 121.40</b>", table_cell_bold), Paragraph("<b>Rs. 280.40</b>", table_cell_bold), Paragraph("<b>Rs. 280.40</b>", table_cell_bold)]
    ]
    t_pnl = Table([pnl_headers] + pnl_rows, colWidths=[2.2*inch, 0.75*inch, 0.75*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.7*inch])
    t_pnl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('BACKGROUND', (0,7), (-1,7), c_card_bg),
        ('BACKGROUND', (0,9), (-1,9), c_card_bg),
        ('BACKGROUND', (0,13), (-1,13), c_orange_bg),
        ('BACKGROUND', (0,15), (-1,16), c_card_bg),
    ]))
    story.append(t_pnl)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: SECTION 8: STAKEHOLDER & INVESTOR ROI & EXECUTION NEXT STEPS
    # =========================================================================
    story.append(Paragraph("8. Return on Investment (ROI) & Systemic Economic Impact", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "KisanKavach represents a unique convergence of institutional investor returns and massive socio-economic value creation for the agrarian ecosystem of India:",
        body_style
    ))
    
    story.append(Paragraph("<b>A. Institutional Equity & Venture Capital Returns:</b>", h2_style))
    roi_pdf_data = [
        [Paragraph("<b>Initial Seed / Pre-Series A Capital Injection</b>", table_cell), Paragraph("Rs. 10.00 Crore ($1.2M USD)", table_cell_bold), Paragraph("Funds pilot hard launch, DPI integrations & regulatory compliance", table_cell)],
        [Paragraph("<b>Year 5 Projected Net Revenue (ARR)</b>", table_cell), Paragraph("Rs. 324.50 Crore ($39.0M USD)", table_cell_bold), Paragraph("Across 50 Lakh farmers and 16,000 participating bank branches", table_cell)],
        [Paragraph("<b>Year 5 Projected EBITDA</b>", table_cell), Paragraph("Rs. 227.00 Crore ($27.2M USD)", table_cell_bold), Paragraph("70.0% EBITDA Margin (Asset-light software/DPI infrastructure)", table_cell)],
        [Paragraph("<b>Enterprise Valuation Exit Multiple</b>", table_cell), Paragraph("12.0x EBITDA / 8.4x ARR", table_cell_bold), Paragraph("Conservative comparative to Indian fintechs (Perfios, Zaggle, Lentra)", table_cell)],
        [Paragraph("<b>ESTIMATED YEAR 5 ENTERPRISE VALUE</b>", table_cell_bold), Paragraph("<font color='#044E29'><b>Rs. 2,724.00 Cr ($327M)</b></font>", table_cell_bold), Paragraph("<b>12.0x Multiple on Year 5 EBITDA of Rs. 227.00 Crore</b>", table_cell_bold)],
        [Paragraph("<b>5-YEAR EQUITY ROI (MOIC)</b>", table_cell_bold), Paragraph("<font color='#044E29'><b>27.2x Cash-on-Cash</b></font>", table_cell_bold), Paragraph("<b>Exceptional capital efficiency and capital appreciation</b>", table_cell_bold)],
        [Paragraph("<b>PROJECTED INTERNAL RATE OF RETURN (IRR)</b>", table_cell_bold), Paragraph("<font color='#044E29'><b>118.5%</b></font>", table_cell_bold), Paragraph("Reflects rapid cash-positive conversion at Month 9", table_cell)],
        [Paragraph("<b>5-Year Cumulative Free Cash Flow Generated</b>", table_cell), Paragraph("Rs. 275.40 Crore", table_cell_bold), Paragraph("Enables self-funded national expansion and special dividend capacity", table_cell)]
    ]
    t_roi = Table(roi_pdf_data, colWidths=[2.4*inch, 1.8*inch, 2.6*inch])
    t_roi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('BACKGROUND', (0,4), (-1,6), c_card_bg),
    ]))
    story.append(t_roi)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>B. Systemic Annual Economic Value Created (Statewide at Year 3):</b>", h2_style))
    socio_pdf_headers = [Paragraph("Beneficiary Sector", table_header), Paragraph("Quantifiable Nature of Economic Value", table_header), Paragraph("Per Unit Value", table_header), Paragraph("Annual Value (Rs. Cr)", table_header)]
    socio_pdf_rows = [
        [Paragraph("<b>Karnataka Farmers</b>", table_cell_bold), Paragraph("Saved physical travel, lost farm wages, and private documentation agent fees", table_cell), Paragraph("Rs. 3,500 / farmer", table_cell), Paragraph("<b>Rs. 420.00 Cr</b>", table_cell)],
        [Paragraph("<b>Karnataka Farmers</b>", table_cell_bold), Paragraph("Interest rate arbitrage (4% subsidized KCC vs 24% informal moneylenders)", table_cell), Paragraph("Rs. 36,000 / loan", table_cell), Paragraph("<b>Rs. 3,312.00 Cr</b>", table_cell)],
        [Paragraph("<b>Banking Consortium</b>", table_cell_bold), Paragraph("Direct reduction in loan file origination, field survey, and verification costs", table_cell), Paragraph("Rs. 1,500 / file", table_cell), Paragraph("<b>Rs. 138.00 Cr</b>", table_cell)],
        [Paragraph("<b>Banking Consortium</b>", table_cell_bold), Paragraph("Elimination of ghost-borrower fraud and disputed land title NPAs", table_cell), Paragraph("1.2% NPA drop", table_cell), Paragraph("<b>Rs. 198.70 Cr</b>", table_cell)],
        [Paragraph("<b>Karnataka Government</b>", table_cell_bold), Paragraph("Administrative savings, automated grievance redressal, and zero subsidy leakage", table_cell), Paragraph("Statewide", table_cell), Paragraph("<b>Rs. 150.00 Cr</b>", table_cell)],
        [Paragraph("<b>TOTAL SYSTEMIC IMPACT</b>", table_cell_bold), Paragraph("<b>Combined annual economic surplus generated for Karnataka</b>", table_cell_bold), Paragraph("<b>Transformational</b>", table_cell_bold), Paragraph("<b>Rs. 4,218.70 Cr</b>", table_cell_bold)]
    ]
    t_socio = Table([socio_pdf_headers] + socio_pdf_rows, colWidths=[1.5*inch, 2.5*inch, 1.2*inch, 1.6*inch])
    t_socio.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, c_bg_light]),
        ('BACKGROUND', (0,-1), (-1,-1), c_orange_bg),
    ]))
    story.append(t_socio)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>9. Strategic Recommendation & Immediate 90-Day Roadmap (Lead: Sarath Babu Rayaprolu):</b>", h2_style))
    story.append(Paragraph(
        "KisanKavach represents a rare, defensible institutional opportunity: a high-margin software platform addressing a government-mandated priority sector with zero statutory displacement. With the production web platform live on <b>kisan.digikavach.net</b>, Supabase PostgreSQL seeded with 10 Karnataka pilot districts, and a native Android build ready for deployment, the platform is primed for immediate institutional roll-out.<br/>"
        "• <b>State Bankers' Committee (SLBC):</b> Present verified pilot metrics to anchor partners (SBI, Canara, KVGB, Karnataka Bank).<br/>"
        "• <b>Security Certification:</b> Complete CERT-In empaneled audit & SOC2 Type II compliance.<br/>"
        "• <b>Capitalization:</b> Close Rs. 10.00 Cr seed round to accelerate statewide deployment across all 31 Karnataka districts.",
        body_style
    ))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Project Report PDF saved successfully to: {pdf_path}")

if __name__ == "__main__":
    os.makedirs(r"d:\KisanKavach\Project Docs", exist_ok=True)
    target_pdf = r"d:\KisanKavach\Project Docs\KisanKavach_Project_Report_Roadmap_Financials.pdf"
    logo = r"d:\KisanKavach\public\logo.png"
    create_project_report_pdf(target_pdf, logo)
