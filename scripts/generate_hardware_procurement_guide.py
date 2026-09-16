"""
KisanKavach - Hardware Infrastructure Specification & Official Procurement Guide
Author: Sarath Babu Rayaprolu
Generates:
1. 09_KisanKavach_Hardware_Specification_Procurement_Guide.pdf
2. 09_KisanKavach_Hardware_Specification_Procurement_Guide.md
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PROJECT_DOCS_DIR = r"d:\KisanKavach\Project Docs"
PUBLIC_DIR = r"d:\KisanKavach\public"
ARTIFACTS_DIR = r"C:\Users\ACER\.gemini\antigravity\brain\38925bf4-5e20-4f48-94c1-995f735978fb"
LOGO_PATH = r"d:\KisanKavach\public\logo.png"

PDF_FILENAME = "09_KisanKavach_Hardware_Specification_Procurement_Guide.pdf"
MD_FILENAME = "09_KisanKavach_Hardware_Specification_Procurement_Guide.md"


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress running header/footer on cover page

        self.saveState()
        # Running Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#044E29"))
        self.drawString(54, A4[1] - 36, "KISANKAVACH | HARDWARE SPECIFICATION & PROCUREMENT GUIDE")
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#EA580C"))
        self.drawRightString(A4[0] - 54, A4[1] - 36, "AUTHOR: SARATH BABU RAYAPROLU")

        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, A4[1] - 42, A4[0] - 54, A4[1] - 42)

        # Running Footer
        self.line(54, 42, A4[0] - 54, 42)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 30, "Confidential - Programme Stakeholders, SLBC Banks & Dept. of Agriculture")

        page_str = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#044E29"))
        self.drawRightString(A4[0] - 54, 30, page_str)
        self.restoreState()


def generate_pdf(pdf_path, logo_path):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=52,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    c_primary = colors.HexColor("#044E29")      # Forest Green
    c_secondary = colors.HexColor("#EA580C")    # Saffron Orange
    c_accent = colors.HexColor("#059669")       # Emerald
    c_dark = colors.HexColor("#0F172A")         # Slate Dark
    c_muted = colors.HexColor("#475569")        # Slate Muted
    c_border = colors.HexColor("#CBD5E1")       # Border Slate
    c_card_bg = colors.HexColor("#ECFDF5")      # Emerald 50
    c_orange_bg = colors.HexColor("#FFF7ED")    # Orange 50
    c_light_bg = colors.HexColor("#F8FAFC")     # Slate 50

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverDocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        alignment=1,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'CoverDocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        alignment=1,
        spaceAfter=6
    )

    tagline_style = ParagraphStyle(
        'CoverTagline',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_muted,
        alignment=1,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'H1Header',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2Header',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark
    )

    bold_style = ParagraphStyle(
        'BodyDarkBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=c_dark
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=c_dark
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=c_muted
    )

    table_header = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_body = ParagraphStyle(
        'TB',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_dark
    )

    table_body_bold = ParagraphStyle(
        'TBB',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=c_dark
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#9A3412")
    )

    story = []

    # =========================================================================
    # COVER PAGE (PAGE 1)
    # =========================================================================
    story.append(Spacer(1, 10))
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=72, height=84))
        story.append(Spacer(1, 10))

    story.append(Paragraph("KISANKAVACH", title_style))
    story.append(Paragraph("HARDWARE INFRASTRUCTURE SPECIFICATION & PROCUREMENT GUIDE", subtitle_style))
    story.append(Paragraph("Comprehensive Technical Sizing, UIDAI L1 Compliance & Official GeM Procurement Blueprint", tagline_style))
    story.append(Spacer(1, 8))

    # Metadata Table
    meta_data = [
        [Paragraph("Project Author & Architect:", meta_label), Paragraph("Sarath Babu Rayaprolu", meta_val)],
        [Paragraph("Document Reference:", meta_label), Paragraph("KK-HW-PROC-2026-001 (Version 1.0)", meta_val)],
        [Paragraph("Deployment Geography:", meta_label), Paragraph("Karnataka (10 Pilot Districts Expanding to All 31 Districts)", meta_val)],
        [Paragraph("Target Implementers:", meta_label), Paragraph("State Level Bankers' Committee (SLBC), Dept. of Agriculture, Grama One / CSCs", meta_val)],
        [Paragraph("Statutory Mandates:", meta_label), Paragraph("UIDAI L1 Biometric Mandate, STQC Certified, BIS Registered, DPDP Act 2023", meta_val)],
        [Paragraph("Procurement Portals:", meta_label), Paragraph("Government e-Marketplace (GeM) & Authorized OEM Direct Distribution", meta_val)],
        [Paragraph("Classification:", meta_label), Paragraph("Commercial-in-Confidence | Official Technical Specification Memorandum", meta_val)]
    ]
    meta_table = Table(meta_data, colWidths=[155, 332])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_light_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # Executive Hardware Callout Cards (Grid 3x2)
    card_data = [
        [
            Paragraph("<b>UIDAI L1 BIOMETRICS</b><br/><font size=11 color='#044E29'><b>100% Cryptographic</b></font><br/><font size=6.5 color='#475569'>Zero Replay / Spoof Proof</font>", styles['Normal']),
            Paragraph("<b>ASSISTED KIOSK FLEET</b><br/><font size=11 color='#059669'><b>6,000+ Centers</b></font><br/><font size=6.5 color='#475569'>Grama One & Mandi Kiosks</font>", styles['Normal']),
            Paragraph("<b>BANK BRANCH DESKS</b><br/><font size=11 color='#EA580C'><b>1,850+ Branches</b></font><br/><font size=6.5 color='#475569'>Maker-Checker Duplex Scanners</font>", styles['Normal']),
        ],
        [
            Paragraph("<b>COMMAND CENTER WALL</b><br/><font size=11 color='#044E29'><b>31 Districts</b></font><br/><font size=6.5 color='#475569'>Collectorate Real-Time LFDs</font>", styles['Normal']),
            Paragraph("<b>PRIMARY SOURCING</b><br/><font size=11 color='#059669'><b>GeM Portal</b></font><br/><font size=6.5 color='#475569'>Govt e-Marketplace Verified</font>", styles['Normal']),
            Paragraph("<b>WARRANTY STANDARD</b><br/><font size=11 color='#EA580C'><b>3 Yr On-Site + AMC</b></font><br/><font size=6.5 color='#475569'>Mission-Critical Field SLA</font>", styles['Normal']),
        ]
    ]
    card_table = Table(card_data, colWidths=[162, 163, 162])
    card_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_accent),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#A7F3D0")),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(card_table)
    story.append(Spacer(1, 10))

    # Executive Memorandum Box
    memo_text = (
        "<b>Executive Hardware Mandate:</b> KisanKavach bridges the last-mile physical-to-digital divide across "
        "Karnataka's 8.2 million farmers and 1,850+ rural bank branches. Delivering 6-day loan sanctions requires "
        "rugged, tamper-proof hardware in rural taluks combined with high-throughput document scanners at bank desks. "
        "In strict compliance with UIDAI regulations, all biometric capture hardware specified herein utilizes Level 1 (L1) "
        "cryptographic key storage, ensuring biometric data is encrypted directly on-chip before leaving the sensor. "
        "Every specified device is fully procurable via the <b>Government e-Marketplace (GeM)</b> or through empaneled national distributors."
    )
    memo_p = Paragraph(memo_text, body_style)
    memo_table = Table([[memo_p]], colWidths=[487])
    memo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_orange_bg),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#FED7AA")),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(memo_table)
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Document Prepared & Architected by: Sarath Babu Rayaprolu</b>", bold_style))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 1 & 2: SPECIFICATIONS BY TIER
    # =========================================================================
    story.append(Paragraph("1. Compliance Mandates & Engineering Standards", h1_style))
    story.append(Paragraph(
        "Deploying field biometric hardware across Karnataka's agricultural belt demands adherence to rigid national security standards:",
        body_style
    ))
    story.append(Spacer(1, 4))

    std_data = [
        [
            Paragraph("<b>STANDARD / REGULATION</b>", table_header),
            Paragraph("<b>STATUTORY AUTHORITY</b>", table_header),
            Paragraph("<b>MANDATORY SPECIFICATION FOR KISANKAVACH</b>", table_header)
        ],
        [
            Paragraph("<b>UIDAI L1 Biometric Mandate</b>", table_body_bold),
            Paragraph("UIDAI (Aadhaar)", table_body),
            Paragraph("Must use Level 1 (L1) certified sensors where biometric encryption occurs within the crypto-boundary of the device. Legacy L0 devices are strictly rejected.", table_body)
        ],
        [
            Paragraph("<b>STQC Certification</b>", table_body_bold),
            Paragraph("MeitY / STQC", table_body),
            Paragraph("Mandatory Standardisation Testing and Quality Certification ensuring optical quality, false acceptance rate (FAR < 0.001%), and false rejection rate (FRR < 0.1%).", table_body)
        ],
        [
            Paragraph("<b>BIS Registration</b>", table_body_bold),
            Paragraph("Bureau of Indian Standards", table_body),
            Paragraph("Compliance with IS 13252 (Part 1) for information technology electrical safety under compulsory registration scheme (CRS).", table_body)
        ],
        [
            Paragraph("<b>Environmental Ruggedness</b>", table_body_bold),
            Paragraph("Field Standard", table_body),
            Paragraph("IP54 / IP65 dust and water splash resistance, drop-tested from 1.2 meters, operational temperature tolerance up to 50 deg C for rural field camps.", table_body)
        ]
    ]
    std_table = Table(std_data, colWidths=[130, 100, 257])
    std_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(std_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Category A: Field & Assisted Kiosk Fleet (Grama One / CSCs)", h1_style))
    story.append(Paragraph(
        "Deployed at Grama One centers, APMC Mandis, Primary Agricultural Credit Societies (PACS), and field verification officers:",
        body_style
    ))
    story.append(Spacer(1, 4))

    cat_a_data = [
        [
            Paragraph("<b>DEVICE / COMPONENT</b>", table_header),
            Paragraph("<b>RECOMMENDED MODEL</b>", table_header),
            Paragraph("<b>KEY TECHNICAL SPECIFICATIONS</b>", table_header),
            Paragraph("<b>UNIT COST (INR)</b>", table_header)
        ],
        [
            Paragraph("<b>A1. UIDAI L1 Fingerprint Scanner</b>", table_body_bold),
            Paragraph("Mantra MFS110 L1<br/><i>(Alt: Morpho MSO 1300 E3 L1)</i>", table_body),
            Paragraph("Optical sensor (500 DPI), hardware cryptoprocessor, on-chip AES-256 encryption, Android/Windows USB-C & micro-USB OTG, STQC & UIDAI L1 certified.", table_body),
            Paragraph("Rs. 3,200 - Rs. 3,850", table_body_bold)
        ],
        [
            Paragraph("<b>A2. Dual-Eye Iris Scanner</b><br/><i>(For elderly/worn fingerprints)</i>", table_body_bold),
            Paragraph("Mantra MIS100V2 L1<br/><i>(Alt: IriShield MK 2120U)</i>", table_body),
            Paragraph("Spatial resolution > 60% @ 4.0 Lp/mm, pixel resolution 640x480, operating distance 10-15cm, STQC certified, dual LED infrared illumination.", table_body),
            Paragraph("Rs. 4,500 - Rs. 5,200", table_body_bold)
        ],
        [
            Paragraph("<b>A3. All-in-One Rugged Bio-POS Tablet</b>", table_body_bold),
            Paragraph("Evolute Falcon 4G<br/><i>(Alt: BioRugged 7-Inch)</i>", table_body),
            Paragraph("7.0\" touch display, integrated L1 fingerprint sensor, 2\" thermal printer, 4G Dual SIM, GPS/NavIC, 6000mAh battery, IP54 rugged casing.", table_body),
            Paragraph("Rs. 18,500 - Rs. 22,000", table_body_bold)
        ],
        [
            Paragraph("<b>A4. Bluetooth Thermal Receipt Printer</b>", table_body_bold),
            Paragraph("NGX N-POS 2\"<br/><i>(Alt: TVS RP 3200)</i>", table_body),
            Paragraph("2-inch thermal printer (58mm), 203 DPI, Bluetooth 4.0 + USB, prints bilingual Kannada/English transaction receipts & KCC acknowledgment slips.", table_body),
            Paragraph("Rs. 2,400 - Rs. 3,100", table_body_bold)
        ],
        [
            Paragraph("<b>A5. Solar Field Battery Pack</b>", table_body_bold),
            Paragraph("Ambrane / Mi 20,000mAh<br/><i>(Alt: EcoFlow 100W Kit)</i>", table_body),
            Paragraph("20,000mAh rugged battery bank with 65W Power Delivery, dual USB-C output, solar panel charging input for off-grid taluk camp operations.", table_body),
            Paragraph("Rs. 1,800 - Rs. 2,400", table_body_bold)
        ]
    ]
    cat_a_table = Table(cat_a_data, colWidths=[115, 110, 192, 70])
    cat_a_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(cat_a_table)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 3 & 4: BANK DESK, COMMAND CENTER & DATA CENTER
    # =========================================================================
    story.append(Paragraph("3. Category B: Bank Branch Underwriting Desks (Maker-Checker)", h1_style))
    story.append(Paragraph(
        "Installed at 1,850+ participating commercial, RRB, and cooperative bank branches across Karnataka:",
        body_style
    ))
    story.append(Spacer(1, 4))

    cat_b_data = [
        [
            Paragraph("<b>COMPONENT</b>", table_header),
            Paragraph("<b>RECOMMENDED MODEL</b>", table_header),
            Paragraph("<b>SPECIFICATIONS & OPERATIONAL PURPOSE</b>", table_header),
            Paragraph("<b>UNIT COST (INR)</b>", table_header)
        ],
        [
            Paragraph("<b>B1. High-Speed Duplex Document Scanner</b>", table_body_bold),
            Paragraph("Epson WorkForce DS-530 II<br/><i>(Alt: Fujitsu fi-8170)</i>", table_body),
            Paragraph("Sheet-fed duplex scanner, 35 ppm / 70 ipm, 50-sheet ADF, ultrasonic double-feed detection. Scans multi-page legacy land deeds, Pahani extracts, and mortgage charge memos.", table_body),
            Paragraph("Rs. 26,000 - Rs. 32,000", table_body_bold)
        ],
        [
            Paragraph("<b>B2. FIPS Cryptographic USB Tokens</b>", table_body_bold),
            Paragraph("ePass2003 / ProxKey<br/><i>(Watchdata / Hypersecu)</i>", table_body),
            Paragraph("FIPS 140-2 Level 3 certified USB cryptographic token. Stores Class 3 digital signature certificates (DSC) for Branch Managers to digitally sign sanction letters & lien memos.", table_body),
            Paragraph("Rs. 850 - Rs. 1,200", table_body_bold)
        ],
        [
            Paragraph("<b>B3. Dual-Screen Underwriter Workstation</b>", table_body_bold),
            Paragraph("Dell OptiPlex 7010 / HP ProDesk 400 + Dual 24\" FHD", table_body),
            Paragraph("Intel Core i5 (13th Gen), 16GB DDR5, 512GB NVMe SSD, dual 24-inch IPS monitors. Enables underwriters to view Bhoomi cadastral maps on Screen 1 and bank loan file on Screen 2.", table_body),
            Paragraph("Rs. 58,000 - Rs. 68,000", table_body_bold)
        ]
    ]
    cat_b_table = Table(cat_b_data, colWidths=[115, 110, 192, 70])
    cat_b_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(cat_b_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("4. Category C: State Command Center & SLBC Oversight Hub", h1_style))
    story.append(Paragraph(
        "Deployed at the State SLBC Secretariat (Canara Bank HO, Bengaluru) and District Collectorates:",
        body_style
    ))
    story.append(Spacer(1, 4))

    cat_c_data = [
        [
            Paragraph("<b>COMPONENT</b>", table_header),
            Paragraph("<b>RECOMMENDED MODEL</b>", table_header),
            Paragraph("<b>SPECIFICATIONS & OPERATIONAL PURPOSE</b>", table_header),
            Paragraph("<b>UNIT COST (INR)</b>", table_header)
        ],
        [
            Paragraph("<b>C1. Command Center Video Wall LFD</b>", table_body_bold),
            Paragraph("Samsung 55\" Video Wall (VH55R-R)<br/><i>(Alt: LG 55SVH7F)</i>", table_body),
            Paragraph("55-inch ultra-narrow bezel (0.88mm), 700 nits brightness, 24/7 non-glare panel, daisy-chain DP 1.2. Displays live taluk heatmaps and SLA breach alerts.", table_body),
            Paragraph("Rs. 1,45,000 / panel", table_body_bold)
        ],
        [
            Paragraph("<b>C2. Multi-Display GIS Controller</b>", table_body_bold),
            Paragraph("HP Z4 G5 Workstation<br/><i>(Alt: Dell Precision 3660)</i>", table_body),
            Paragraph("Intel Xeon W-2400, 64GB ECC RAM, NVIDIA RTX A4000 (16GB), drives 4x 4K video wall outputs simultaneously for geospatial district drilldowns.", table_body),
            Paragraph("Rs. 1,85,000 - Rs. 2,15,000", table_body_bold)
        ],
        [
            Paragraph("<b>C3. SLBC Virtual Meeting Endpoint</b>", table_body_bold),
            Paragraph("Logitech Rally Plus System<br/><i>(Alt: Poly Studio X50)</i>", table_body),
            Paragraph("Ultra-HD 4K PTZ camera, dual beamforming speakerphones, automatic speaker framing for quarterly SLBC and district LDM coordination reviews.", table_body),
            Paragraph("Rs. 1,65,000 - Rs. 1,95,000", table_body_bold)
        ]
    ]
    cat_c_table = Table(cat_c_data, colWidths=[115, 110, 192, 70])
    cat_c_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0284C7")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(cat_c_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("5. Category D: Data Center, Bank Gateway & Network Enclave", h1_style))
    story.append(Paragraph(
        "Required for State Data Centre (SDC) rack deployments and dedicated bank leased-line terminations:",
        body_style
    ))
    story.append(Spacer(1, 4))

    cat_d_data = [
        [
            Paragraph("<b>COMPONENT</b>", table_header),
            Paragraph("<b>RECOMMENDED MODEL</b>", table_header),
            Paragraph("<b>SPECIFICATIONS & OPERATIONAL PURPOSE</b>", table_header),
            Paragraph("<b>UNIT COST (INR)</b>", table_header)
        ],
        [
            Paragraph("<b>D1. Enterprise Next-Gen Firewall / VPN</b>", table_body_bold),
            Paragraph("Fortinet FortiGate 100F<br/><i>(Alt: Cisco Firepower 1150)</i>", table_body),
            Paragraph("10 Gbps firewall throughput, 1 Gbps IPsec VPN throughput, redundant power supply, terminates point-to-point IPsec tunnels to Finacle/BaNCS CBS centers.", table_body),
            Paragraph("Rs. 2,85,000 - Rs. 3,40,000", table_body_bold)
        ],
        [
            Paragraph("<b>D2. Hardware Security Module (HSM)</b>", table_body_bold),
            Paragraph("Thales Luna HSM A790<br/><i>(Alt: Entrust nShield Connect)</i>", table_body),
            Paragraph("FIPS 140-2 Level 3 certified network HSM. Cryptographic key isolation for Aadhaar Data Vault (ADV), database column encryption, and DPDP consent tokens.", table_body),
            Paragraph("Rs. 8,50,000 - Rs. 11,00,000", table_body_bold)
        ]
    ]
    cat_d_table = Table(cat_d_data, colWidths=[115, 110, 192, 70])
    cat_d_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_dark),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(cat_d_table)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 5: OFFICIAL PROCUREMENT SOURCES & GEM PORTAL GUIDE
    # =========================================================================
    story.append(Paragraph("6. Official Procurement Sources & GeM Portal Workflow", h1_style))
    story.append(Paragraph(
        "For government entities (Dept. of Agriculture, District Collectorates) and Public Sector Banks "
        "(Canara Bank, SBI, KVGB), public procurement must strictly flow through the <b>Government e-Marketplace (GeM)</b> "
        "or authorized OEM national distributors under General Financial Rules (GFR) 2017.",
        body_style
    ))
    story.append(Spacer(1, 6))

    proc_data = [
        [
            Paragraph("<b>ITEM CODE & CATEGORY</b>", table_header),
            Paragraph("<b>GeM PORTAL CATEGORY NAME</b>", table_header),
            Paragraph("<b>AUTHORIZED OEM / NATIONAL DISTRIBUTORS</b>", table_header),
            Paragraph("<b>PROCUREMENT METHOD</b>", table_header)
        ],
        [
            Paragraph("<b>A1 & A2</b><br/>Biometric Fingerprint & Iris Scanners", table_body_bold),
            Paragraph("Biometric Attendance / Access Control & Aadhaar Identification Devices (L1 Certified)", table_body),
            Paragraph(
                "• <b>Mantra Softech India Pvt. Ltd.</b> (Bengaluru / Ahmedabad)<br/>"
                "• <b>IDEMIA (Morpho) India</b><br/>"
                "• <b>Savex Technologies</b> (National Distributor)<br/>"
                "• GeM Direct: Search 'MFS110 L1' or 'MIS100V2'",
                table_body
            ),
            Paragraph("GeM Direct Purchase (< Rs. 5L) or L1 Custom Bid / PAC (Proprietary Article Certificate)", table_body)
        ],
        [
            Paragraph("<b>A3 & A4</b><br/>Bio-POS Tablets & Bluetooth Printers", table_body_bold),
            Paragraph("Point of Sale (POS) Terminals / Portable Micro-ATM Machines", table_body),
            Paragraph(
                "• <b>Evolute Devices Pvt. Ltd.</b> (Mumbai / Bengaluru)<br/>"
                "• <b>NGX Technologies Pvt. Ltd.</b> (Bengaluru)<br/>"
                "• <b>Ingram Micro India Pvt. Ltd.</b><br/>"
                "• GeM Product ID: Evolute Falcon POS",
                table_body
            ),
            Paragraph("GeM e-Bidding with Custom Specification BoQ (Bill of Quantities)", table_body)
        ],
        [
            Paragraph("<b>B1 & B2</b><br/>Duplex Document Scanners & DSC Tokens", table_body_bold),
            Paragraph("Document Scanners (ADF Sheetfed) & Cryptographic USB Hardware Tokens", table_body),
            Paragraph(
                "• <b>Epson India Pvt. Ltd.</b> (Bengaluru)<br/>"
                "• <b>Redington India Ltd.</b> (National Distributor)<br/>"
                "• <b>e-Mudhra / SafeScrypt / VSign</b> (DSC Tokens)<br/>"
                "• GeM Search: 'Epson DS-530 II' / 'ePass2003'",
                table_body
            ),
            Paragraph("GeM Direct Buy / Rate Contract across Bank Regional Offices", table_body)
        ],
        [
            Paragraph("<b>B3 & C2</b><br/>Dual-Screen Desks & GIS Workstations", table_body_bold),
            Paragraph("Desktop Computers / Computer Monitors / High Performance Workstations", table_body),
            Paragraph(
                "• <b>Dell Technologies India</b><br/>"
                "• <b>HP Enterprise India Pvt. Ltd.</b><br/>"
                "• <b>Redington / Savex Technologies</b><br/>"
                "• GeM Product ID: OptiPlex 7010 / HP Z4 G5",
                table_body
            ),
            Paragraph("GeM Forward Auction / OEM Bunch Bidding for volume discounts", table_body)
        ],
        [
            Paragraph("<b>C1 & C3</b><br/>Video Wall LFDs & Video Conferencing", table_body_bold),
            Paragraph("Large Format Displays (LFD) / Video Conferencing System", table_body),
            Paragraph(
                "• <b>Samsung India Electronics</b><br/>"
                "• <b>Logitech Electronics India</b><br/>"
                "• <b>Actis Technologies / Vega Global</b> (AV SI Partners)<br/>"
                "• GeM Search: 'Samsung VH55R' / 'Rally Plus'",
                table_body
            ),
            Paragraph("State e-Governance / CeG empaneled AV Turnkey tender", table_body)
        ],
        [
            Paragraph("<b>D1 & D2</b><br/>Firewalls & Hardware Security Modules", table_body_bold),
            Paragraph("Unified Threat Management (UTM) / Hardware Security Modules (HSM)", table_body),
            Paragraph(
                "• <b>Fortinet Technologies India</b><br/>"
                "• <b>Thales India Pvt. Ltd.</b> (Noida / Bengaluru)<br/>"
                "• <b>Wipro / TCS / ITI Limited</b> (System Integrators)",
                table_body
            ),
            Paragraph("Bank IT Procurement / MeitY Empaneled Data Centre SI Contract", table_body)
        ]
    ]
    proc_table = Table(proc_data, colWidths=[105, 110, 172, 100])
    proc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(proc_table)
    story.append(Spacer(1, 8))

    # Procurement Notice Box
    p_notice = (
        "<b>Important GeM Sourcing Tip:</b> When raising bids on the GeM portal for Category A (Biometrics), "
        "procuring nodal officers must explicitly mandate <b>'UIDAI Level 1 (L1) Certificate Copy from STQC'</b> "
        "as a mandatory technical qualification criterion. Bids lacking this requirement often receive non-compliant "
        "legacy L0 devices which will be rejected upon connection to the UIDAI Aadhaar verification server."
    )
    p_notice_p = Paragraph(p_notice, callout_style)
    p_notice_table = Table([[p_notice_p]], colWidths=[487])
    p_notice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_orange_bg),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#FED7AA")),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(p_notice_table)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 6: PHASE-WISE BUDGET & ROLLOUT SIZING
    # =========================================================================
    story.append(Paragraph("7. Phase-Wise Hardware Procurement Budget & Quantities", h1_style))
    story.append(Paragraph(
        "Estimated procurement quantities and capital outlay structured across the four strategic rollout horizons:",
        body_style
    ))
    story.append(Spacer(1, 4))

    budget_data = [
        [
            Paragraph("<b>ROLLOUT PHASE</b>", table_header),
            Paragraph("<b>GEOGRAPHIC & BRANCH SCOPE</b>", table_header),
            Paragraph("<b>KEY HARDWARE QUANTITIES</b>", table_header),
            Paragraph("<b>EST. BUDGET (INR)</b>", table_header)
        ],
        [
            Paragraph("<b>PHASE 1: PILOT LAUNCH</b><br/>Months 1 – 6 (2026)", table_body_bold),
            Paragraph("10 Pilot Districts<br/>• 350 Bank Branches<br/>• 1,200 Grama One / CSCs", table_body),
            Paragraph(
                "• 1,200 Mantra MFS110 L1 Fingerprint Scanners<br/>"
                "• 150 Mantra MIS100V2 Iris Scanners<br/>"
                "• 350 Epson DS-530 II Duplex Scanners<br/>"
                "• 350 Workstations & DSC Tokens<br/>"
                "• 1 Pilot Command Center Display Unit",
                table_body
            ),
            Paragraph("<b>Rs. 3.45 Crore</b><br/>($415K USD)", table_body_bold)
        ],
        [
            Paragraph("<b>PHASE 2: STATEWIDE KA</b><br/>Months 7 – 18 (2027)", table_body_bold),
            Paragraph("All 31 Karnataka Districts<br/>• 1,850 Bank Branches<br/>• 6,000 Grama One / CSCs<br/>• 31 Collectorate Desks", table_body),
            Paragraph(
                "• 4,800 Additional L1 Fingerprint Scanners<br/>"
                "• 600 Additional Iris Scanners<br/>"
                "• 1,500 Additional Duplex Scanners<br/>"
                "• 1,500 Additional Underwriter Workstations<br/>"
                "• 31 District Command Center LFD Displays<br/>"
                "• Redundant Fortinet Firewalls & HSM Enclave",
                table_body
            ),
            Paragraph("<b>Rs. 14.80 Crore</b><br/>($1.78M USD)", table_body_bold)
        ],
        [
            Paragraph("<b>PHASE 3: REGIONAL SCALE</b><br/>Months 19 – 36 (2028-29)", table_body_bold),
            Paragraph("Karnataka + AP, Telangana, TN<br/>• 4,200 Bank Branches<br/>• 15,000 Rural CSC Kiosks", table_body),
            Paragraph(
                "• 9,000 L1 Biometric Scanners (PACS & Kiosks)<br/>"
                "• 2,350 Duplex Scanners for Regional Branches<br/>"
                "• 1,500 Rugged Evolute Bio-POS Tablets<br/>"
                "• State Data Centre High-Throughput HSM Expansion",
                table_body
            ),
            Paragraph("<b>Rs. 28.50 Crore</b><br/>($3.43M USD)", table_body_bold)
        ],
        [
            Paragraph("<b>PHASE 4: PAN-INDIA SCALE</b><br/>Months 37 – 60 (2029-31)", table_body_bold),
            Paragraph("7 Sovereign States<br/>• 16,000 Bank Branches<br/>• 50,000 Rural Touchpoints", table_body),
            Paragraph(
                "• 35,000 L1 Biometric Scanners<br/>"
                "• 11,800 Bank Branch Underwriter Bundles<br/>"
                "• 8,000 Bio-POS Mobile Field Terminals<br/>"
                "• National AgriStack Sovereign Hardware Enclave",
                table_body
            ),
            Paragraph("<b>Rs. 92.00 Crore</b><br/>($11.08M USD)", table_body_bold)
        ]
    ]
    budget_table = Table(budget_data, colWidths=[110, 115, 172, 90])
    budget_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(budget_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("8. Warranty, Spares & Field Maintenance Protocol", h1_style))
    story.append(Paragraph(
        "To prevent disruptions in rural credit delivery during the peak agricultural sowing window (Kharif & Rabi), "
        "the procurement RFP must mandate the following Service Level Agreement (SLA):",
        body_style
    ))
    story.append(Spacer(1, 4))

    sla_data = [
        [Paragraph("<b>SLA PARAMETER</b>", table_header), Paragraph("<b>MANDATORY CONTRACTUAL REQUIREMENT</b>", table_header)],
        [
            Paragraph("<b>Warranty Period</b>", table_body_bold),
            Paragraph("Minimum 3-Year Comprehensive On-Site OEM Warranty covering all parts, sensor optical glass, and labor.", table_body)
        ],
        [
            Paragraph("<b>Buffer Spares in Taluks</b>", table_body_bold),
            Paragraph("5% operational spare inventory maintained at each District Lead Bank Office (LDM) for immediate swap within 24 hours.", table_body)
        ],
        [
            Paragraph("<b>Mean Time to Replace (MTTR)</b>", table_body_bold),
            Paragraph("< 24 hours in District Headquarters; < 48 hours in rural Taluk / Hobli centers.", table_body)
        ],
        [
            Paragraph("<b>Annual Maintenance Contract (AMC)</b>", table_body_bold),
            Paragraph("Years 4 and 5 covered under fixed-rate AMC capped at 8% of original equipment capital cost.", table_body)
        ]
    ]
    sla_table = Table(sla_data, colWidths=[140, 347])
    sla_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(sla_table)
    story.append(Spacer(1, 12))

    # Author Signoff Box
    signoff_data = [
        [
            Paragraph("<b>Document Author & Lead Architect:</b> Sarath Babu Rayaprolu<br/>"
                      "<b>Project:</b> KisanKavach (Next-Gen Agricultural Credit DPI)<br/>"
                      "<b>Portal:</b> https://kisan.digikavach.net  |  <b>Official Release Date:</b> September 2026", bold_style)
        ]
    ]
    signoff_table = Table(signoff_data, colWidths=[487])
    signoff_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_primary),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(signoff_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Hardware Specification PDF generated successfully at: {pdf_path}")


def generate_markdown(md_path):
    md_content = """# KisanKavach: Hardware Infrastructure Specification & Procurement Blueprint
**Document Reference**: KK-HW-PROC-2026-001  
**Author & Lead Architect**: Sarath Babu Rayaprolu  
**Project**: KisanKavach (ಕಿಸಾನ್ ಕವಚ) — Agricultural Credit, Benefits & Fraud Defense DPI  
**Target Stakeholders**: State Level Bankers' Committee (SLBC), Dept. of Agriculture, Grama One / CSC Networks, District Collectors  
**Statutory Compliance**: UIDAI L1 Biometric Mandate, STQC Certified, BIS Registered, DPDP Act 2023  
**Procurement Channels**: Government e-Marketplace (GeM) & Authorized OEM National Distribution  

---

## 1. Executive Hardware Mandate & Compliance Standards

To deliver rapid 6-day loan disbursements across Karnataka's 8.2 million farmers and 1,850+ rural bank branches, KisanKavach requires a robust, tamper-proof hardware ecosystem spanning rural field kiosks, bank underwriting desks, district command centers, and data center enclaves.

### Mandatory Statutory Standards:
1. **UIDAI Level 1 (L1) Biometric Mandate**: All biometric devices must possess an on-chip cryptographic processor where fingerprint/iris encryption occurs inside the hardware boundary. *Legacy L0 devices are strictly prohibited.*
2. **STQC Certification**: Issued by the Ministry of Electronics and Information Technology (MeitY) ensuring optical scan fidelity, False Acceptance Rate (FAR < 0.001%), and False Rejection Rate (FRR < 0.1%).
3. **BIS Registration**: Registered under the Compulsory Registration Scheme (CRS) compliant with IS 13252 (Part 1).
4. **Environmental Ruggedness**: Minimum IP54 ingress protection rating for rural field touchpoints, drop-tested from 1.2 meters, operational up to 50°C.

---

## 2. Comprehensive Hardware Catalog by Tier

### Tier A: Field & Assisted Kiosk Fleet (Grama One / CSCs / Field Officers)

| Item Code | Device / Component | Recommended Model | Technical Specifications | Indicative Unit Cost |
| :--- | :--- | :--- | :--- | :--- |
| **A1** | **UIDAI L1 Fingerprint Scanner** | **Mantra MFS110 L1**<br/>*(Alt: Morpho MSO 1300 E3 L1)* | Optical sensor (500 DPI), hardware cryptoprocessor, on-chip AES-256 encryption, Android/Windows USB-C & OTG, STQC & UIDAI L1 certified. | **Rs. 3,200 – Rs. 3,850** |
| **A2** | **Dual-Eye Iris Scanner** | **Mantra MIS100V2 L1**<br/>*(Alt: IriShield MK 2120U)* | Spatial resolution > 60% @ 4.0 Lp/mm, pixel resolution 640x480, operating distance 10–15cm, STQC certified, dual IR illumination. | **Rs. 4,500 – Rs. 5,200** |
| **A3** | **All-in-One Rugged Bio-POS Tablet** | **Evolute Falcon 4G**<br/>*(Alt: BioRugged 7-Inch)* | 7.0" touch display, integrated L1 fingerprint sensor, 2" thermal printer, 4G Dual SIM, GPS/NavIC, 6000mAh battery, IP54 casing. | **Rs. 18,500 – Rs. 22,000** |
| **A4** | **Bluetooth Thermal Receipt Printer** | **NGX N-POS 2"**<br/>*(Alt: TVS RP 3200)* | 2-inch thermal printer (58mm), 203 DPI, Bluetooth 4.0 + USB, prints bilingual Kannada/English transaction receipts & KCC acknowledgment slips. | **Rs. 2,400 – Rs. 3,100** |
| **A5** | **Solar Field Battery Pack** | **Ambrane / Mi 20,000mAh**<br/>*(Alt: EcoFlow 100W Kit)* | 20,000mAh rugged battery bank with 65W Power Delivery, dual USB-C output, solar panel charging input for off-grid taluk camp operations. | **Rs. 1,800 – Rs. 2,400** |

---

### Tier B: Bank Branch Underwriting Desks (Maker-Checker)

| Item Code | Component | Recommended Model | Technical Specifications & Purpose | Indicative Unit Cost |
| :--- | :--- | :--- | :--- | :--- |
| **B1** | **High-Speed Duplex Document Scanner** | **Epson WorkForce DS-530 II**<br/>*(Alt: Fujitsu fi-8170)* | Sheet-fed duplex scanner, 35 ppm / 70 ipm, 50-sheet ADF, ultrasonic double-feed detection. Scans multi-page legacy land deeds, Pahani extracts, and charge creation forms. | **Rs. 26,000 – Rs. 32,000** |
| **B2** | **FIPS Cryptographic USB Tokens** | **ePass2003 / ProxKey**<br/>*(Watchdata / Hypersecu)* | FIPS 140-2 Level 3 certified USB cryptographic token. Stores Class 3 digital signature certificates (DSC) for Branch Managers to digitally sign sanction letters & lien memos. | **Rs. 850 – Rs. 1,200** |
| **B3** | **Dual-Screen Underwriter Workstation** | **Dell OptiPlex 7010 / HP ProDesk 400 + Dual 24" FHD** | Intel Core i5 (13th Gen), 16GB DDR5, 512GB NVMe SSD, dual 24-inch IPS monitors. Enables underwriters to view Bhoomi cadastral maps on Screen 1 and bank loan file on Screen 2. | **Rs. 58,000 – Rs. 68,000** |

---

### Tier C: State Command Center & SLBC Oversight Hub

| Item Code | Component | Recommended Model | Technical Specifications & Purpose | Indicative Unit Cost |
| :--- | :--- | :--- | :--- | :--- |
| **C1** | **Command Center Video Wall LFD** | **Samsung 55" Video Wall (VH55R-R)**<br/>*(Alt: LG 55SVH7F)* | 55-inch ultra-narrow bezel (0.88mm), 700 nits brightness, 24/7 non-glare panel, daisy-chain DP 1.2. Displays live taluk heatmaps and SLA breach alerts. | **Rs. 1,45,000 / panel** |
| **C2** | **Multi-Display GIS Controller** | **HP Z4 G5 Workstation**<br/>*(Alt: Dell Precision 3660)* | Intel Xeon W-2400, 64GB ECC RAM, NVIDIA RTX A4000 (16GB), drives 4x 4K video wall outputs simultaneously for geospatial district drilldowns. | **Rs. 1,85,000 – Rs. 2,15,000** |
| **C3** | **SLBC Virtual Meeting Endpoint** | **Logitech Rally Plus System**<br/>*(Alt: Poly Studio X50)* | Ultra-HD 4K PTZ camera, dual beamforming speakerphones, automatic speaker framing for quarterly SLBC and district LDM coordination reviews. | **Rs. 1,65,000 – Rs. 1,95,000** |

---

### Tier D: Data Center, Bank Gateway & Network Enclave

| Item Code | Component | Recommended Model | Technical Specifications & Purpose | Indicative Unit Cost |
| :--- | :--- | :--- | :--- | :--- |
| **D1** | **Enterprise Next-Gen Firewall / VPN** | **Fortinet FortiGate 100F**<br/>*(Alt: Cisco Firepower 1150)* | 10 Gbps firewall throughput, 1 Gbps IPsec VPN throughput, redundant power supply, terminates point-to-point IPsec tunnels to Finacle/BaNCS CBS centers. | **Rs. 2,85,000 – Rs. 3,40,000** |
| **D2** | **Hardware Security Module (HSM)** | **Thales Luna HSM A790**<br/>*(Alt: Entrust nShield Connect)* | FIPS 140-2 Level 3 certified network HSM. Cryptographic key isolation for Aadhaar Data Vault (ADV), database column encryption, and DPDP consent tokens. | **Rs. 8,50,000 – Rs. 11,00,000** |

---

## 3. Official Procurement Sources & Government e-Marketplace (GeM) Workflow

Public sector banks (Canara Bank, SBI, KVGB) and government bodies (Dept. of Agriculture, CeG) must procure these devices strictly in compliance with General Financial Rules (GFR) 2017.

### Procurement Directory & GeM Categories:

```
┌───────────────┬──────────────────────────────────────────┬───────────────────────────────────────────┬─────────────────────────────────┐
│ Item Code     │ GeM Portal Category Name                 │ Authorized OEM / National Distributors    │ Recommended Procurement Method  │
├───────────────┼──────────────────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────┤
│ A1 & A2       │ Biometric Attendance / Access Control &  │ • Mantra Softech India Pvt. Ltd.          │ GeM Direct Purchase (< Rs. 5L)  │
│ (Fingerprint  │ Aadhaar Identification Devices           │ • IDEMIA (Morpho) India                   │ or L1 Custom Bid with UIDAI L1  │
│ & Iris)       │ (UIDAI L1 Certified)                     │ • Savex Technologies (National Dist.)     │ mandatory clause                │
├───────────────┼──────────────────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────┤
│ A3 & A4       │ Point of Sale (POS) Terminals /          │ • Evolute Devices Pvt. Ltd. (Mumbai/BLR)  │ GeM e-Bidding with Custom       │
│ (Bio-POS &    │ Portable Micro-ATM Machines              │ • NGX Technologies Pvt. Ltd. (Bengaluru)  │ Specification BoQ               │
│ Printers)     │                                          │ • Ingram Micro India Pvt. Ltd.            │                                 │
├───────────────┼──────────────────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────┤
│ B1 & B2       │ Document Scanners (ADF Sheetfed) &       │ • Epson India Pvt. Ltd. (Bengaluru)       │ GeM Direct Buy / Bank Rate      │
│ (Scanners &   │ Cryptographic USB Hardware Tokens        │ • Redington India Ltd. (National Dist.)   │ Contract across Regional Offices│
│ DSC Tokens)   │                                          │ • e-Mudhra / SafeScrypt / VSign           │                                 │
├───────────────┼──────────────────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────┤
│ B3 & C2       │ Desktop Computers / Workstations /       │ • Dell Technologies India                 │ GeM Forward Auction / OEM Bunch │
│ (Workstations)│ Computer Monitors                        │ • HP Enterprise India Pvt. Ltd.           │ Bidding for volume discounts    │
│               │                                          │ • Savex / Redington Technologies          │                                 │
├───────────────┼──────────────────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────┤
│ C1 & C3       │ Large Format Displays (LFD) &            │ • Samsung India Electronics               │ State e-Gov / CeG Empaneled     │
│ (AV Displays) │ Video Conferencing Systems               │ • Logitech Electronics India              │ Turnkey System Integrator tender│
│               │                                          │ • Actis Technologies / Vega Global        │                                 │
├───────────────┼──────────────────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────┤
│ D1 & D2       │ Unified Threat Management (UTM) &        │ • Fortinet Technologies India             │ Bank Core IT Procurement /      │
│ (Firewall/HSM)│ Hardware Security Modules (HSM)          │ • Thales India Pvt. Ltd. (Noida/BLR)      │ MeitY Empaneled Data Centre SI  │
└───────────────┴──────────────────────────────────────────┴───────────────────────────────────────────┴─────────────────────────────────┘
```

> **Critical Procurement Advisory for GeM Bidding:**  
> When creating bids on GeM for biometric scanners, the procuring authority must upload an additional buyer-added clause:  
> *"Bidder must furnish an authentic, active STQC Certificate confirming UIDAI Level 1 (L1) compliance. Non-L1 or L0 devices will be summarily rejected at technical evaluation without recourse."*

---

## 4. Phase-Wise Sizing & Capital Expenditure Budget

| Rollout Phase | Target Coverage | Key Hardware Quantities | Estimated Budget (INR) |
| :--- | :--- | :--- | :--- |
| **Phase 1: Pilot Launch**<br/>*(Months 1 – 6, 2026)* | 10 Pilot Districts<br/>• 350 Bank Branches<br/>• 1,200 Grama One / CSCs | • 1,200 Mantra MFS110 L1 Scanners<br/>• 150 Mantra MIS100V2 Iris Scanners<br/>• 350 Epson DS-530 II Duplex Scanners<br/>• 350 Workstations & DSC Tokens<br/>• 1 Pilot Command Center LFD Display | **Rs. 3.45 Crore**<br/>*($415,000 USD)* |
| **Phase 2: Statewide Rollout**<br/>*(Months 7 – 18, 2027)* | All 31 Karnataka Districts<br/>• 1,850 Bank Branches<br/>• 6,000 Grama One / CSCs<br/>• 31 Collectorate Desks | • 4,800 Additional L1 Fingerprint Scanners<br/>• 600 Additional Iris Scanners<br/>• 1,500 Additional Duplex Scanners<br/>• 1,500 Additional Underwriter Workstations<br/>• 31 District Command Center LFD Displays<br/>• Redundant Fortinet Firewalls & HSM Enclave | **Rs. 14.80 Crore**<br/>*($1.78 Million USD)* |
| **Phase 3: Regional Value Chain**<br/>*(Months 19 – 36, 2028-29)* | Karnataka + AP, Telangana, TN<br/>• 4,200 Bank Branches<br/>• 15,000 Rural CSC Kiosks | • 9,000 L1 Biometric Scanners (PACS & Kiosks)<br/>• 2,350 Duplex Scanners for Regional Branches<br/>• 1,500 Rugged Evolute Bio-POS Tablets<br/>• State Data Centre High-Throughput HSM Expansion | **Rs. 28.50 Crore**<br/>*($3.43 Million USD)* |
| **Phase 4: National Scale**<br/>*(Months 37 – 60, 2029-31)* | 7 Sovereign States<br/>• 16,000 Bank Branches<br/>• 50,000 Rural Touchpoints | • 35,000 L1 Biometric Scanners<br/>• 11,800 Bank Branch Underwriter Bundles<br/>• 8,000 Bio-POS Mobile Field Terminals<br/>• National AgriStack Sovereign Hardware Enclave | **Rs. 92.00 Crore**<br/>*($11.08 Million USD)* |

---

## 5. Warranty, Field Spares & Maintenance SLA

To ensure unhindered credit disbursements during the peak Kharif and Rabi agricultural sowing seasons:
1. **Warranty Standard**: Minimum 3-Year Comprehensive On-Site OEM Warranty including parts, optical glass, and labor.
2. **Buffer Inventory**: 5% buffer spare inventory maintained at each District Lead Bank (LDM) office for instant 24-hour equipment swaps.
3. **Mean Time to Replace (MTTR)**: Under 24 hours in District Headquarters; under 48 hours in rural Taluk / Hobli centers.
4. **Annual Maintenance Contract (AMC)**: Years 4 and 5 capped at 8% of original equipment capital cost.

---

**Prepared & Architected by:**  
**Sarath Babu Rayaprolu**  
*Founder & Lead System Architect, KisanKavach*  
*Platform: https://kisan.digikavach.net*
"""
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Markdown Guide written successfully to: {md_path}")


if __name__ == "__main__":
    os.makedirs(PROJECT_DOCS_DIR, exist_ok=True)
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    pdf_out = os.path.join(PROJECT_DOCS_DIR, PDF_FILENAME)
    md_out = os.path.join(PROJECT_DOCS_DIR, MD_FILENAME)

    print("Generating Hardware Specification PDF...")
    generate_pdf(pdf_out, LOGO_PATH)

    print("Generating Hardware Specification Markdown...")
    generate_markdown(md_out)

    print("Distributing to artifacts and public web directories...")
    for filename in [PDF_FILENAME, MD_FILENAME]:
        src = os.path.join(PROJECT_DOCS_DIR, filename)
        # Copy to public
        dst_pub = os.path.join(PUBLIC_DIR, filename)
        with open(src, "rb") as s, open(dst_pub, "wb") as d:
            d.write(s.read())
        # Copy to artifacts
        dst_art = os.path.join(ARTIFACTS_DIR, filename)
        with open(src, "rb") as s, open(dst_art, "wb") as d:
            d.write(s.read())
        print(f"Copied {filename} to public and artifacts directory.")

    print("\nALL HARDWARE SPECIFICATION & PROCUREMENT DELIVERABLES COMPLETED SUCCESSFULLY!")
