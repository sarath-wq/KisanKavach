"""
KisanKavach - State Level Bankers' Committee (SLBC) Karnataka Anchor Presentation Generator
Author: Sarath Babu Rayaprolu
Generates both:
1. KisanKavach_SLBC_Anchor_Presentation.pptx (16:9 widescreen PowerPoint)
2. KisanKavach_SLBC_Anchor_Presentation.pdf (16:9 landscape Executive PDF Presentation)
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Colors
C_DARK_BG = RGBColor(15, 23, 42)      # Slate 900
C_PRIMARY = RGBColor(4, 78, 41)       # Deep Forest Green
C_ACCENT = RGBColor(5, 150, 105)      # Emerald Green
C_ORANGE = RGBColor(234, 88, 12)      # Saffron Orange
C_WHITE = RGBColor(255, 255, 255)
C_SLATE_50 = RGBColor(248, 250, 252)
C_SLATE_200 = RGBColor(226, 232, 240)
C_SLATE_600 = RGBColor(71, 85, 105)
C_SLATE_800 = RGBColor(30, 41, 59)
C_CARD_BG = RGBColor(240, 253, 244)   # Emerald 50
C_ORANGE_BG = RGBColor(255, 247, 237) # Orange 50

# Output paths
PROJECT_DOCS_DIR = r"d:\KisanKavach\Project Docs"
PUBLIC_DIR = r"d:\KisanKavach\public"
ARTIFACTS_DIR = r"C:\Users\ACER\.gemini\antigravity\brain\38925bf4-5e20-4f48-94c1-995f735978fb"
LOGO_PATH = r"d:\KisanKavach\public\logo.png"

PPTX_FILENAME = "KisanKavach_SLBC_Anchor_Presentation.pptx"
PDF_FILENAME = "KisanKavach_SLBC_Anchor_Presentation.pdf"


def create_pptx_deck(output_path, logo_path):
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title, category="SLBC KARNATAKA ANCHOR PRESENTATION"):
        # Header banner bar
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_PRIMARY
        top_bar.line.fill.background()

        # Category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(10), Inches(0.3))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category.upper()
        p_c.font.size = Pt(9)
        p_c.font.bold = True
        p_c.font.color.rgb = C_ORANGE

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(10), Inches(0.6))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(20)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE

        # Author tag on top right
        auth_box = slide.shapes.add_textbox(Inches(9.5), Inches(0.25), Inches(3.2), Inches(0.6))
        tf_a = auth_box.text_frame
        p_a = tf_a.paragraphs[0]
        p_a.alignment = PP_ALIGN.RIGHT
        p_a.text = "Lead: Sarath Babu Rayaprolu"
        p_a.font.size = Pt(10)
        p_a.font.bold = True
        p_a.font.color.rgb = C_ORANGE

        # Bottom footer bar
        bot_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.1), Inches(13.333), Inches(0.4))
        bot_bar.fill.solid()
        bot_bar.fill.fore_color.rgb = C_SLATE_50
        bot_bar.line.color.rgb = C_SLATE_200

        f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.12), Inches(8), Inches(0.3))
        tf_f = f_box.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = "Confidential - State Level Bankers' Committee (SLBC) Karnataka & Partner Banks"
        p_f.font.size = Pt(8.5)
        p_f.font.color.rgb = C_SLATE_600

        p_box = slide.shapes.add_textbox(Inches(9.5), Inches(7.12), Inches(3.0), Inches(0.3))
        tf_p = p_box.text_frame
        p_p = tf_p.paragraphs[0]
        p_p.alignment = PP_ALIGN.RIGHT
        p_p.text = "kisan.digikavach.net"
        p_p.font.size = Pt(8.5)
        p_p.font.bold = True
        p_p.font.color.rgb = C_PRIMARY

    def add_card(slide, left, top, width, height, bg_color=C_WHITE, border_color=C_SLATE_200):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
        return shape

    # ==========================================================
    # SLIDE 1: Title Slide (Dark Theme)
    # ==========================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_DARK_BG
    bg1.line.fill.background()

    # Accent Stripe
    stripe = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = C_ORANGE
    stripe.line.fill.background()

    # Add Logo
    if os.path.exists(logo_path):
        slide1.shapes.add_picture(logo_path, Inches(5.9), Inches(0.7), width=Inches(1.5))

    # Main Titles
    t1_box = slide1.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(11.333), Inches(1.8))
    tf1 = t1_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "KISANKAVACH"
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    p2 = tf1.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "Next-Generation Digital Public Infrastructure for Agricultural Credit & Fraud Defense"
    p2.font.size = Pt(17)
    p2.font.bold = True
    p2.font.color.rgb = C_ORANGE

    p3 = tf1.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    p3.text = "State Level Bankers' Committee (SLBC) Karnataka — Anchor Presentation"
    p3.font.size = Pt(15)
    p3.font.color.rgb = RGBColor(148, 163, 184) # Slate 400

    # Key Metadata Card
    meta_card = add_card(slide1, Inches(2.0), Inches(4.5), Inches(9.333), Inches(2.2), RGBColor(30, 41, 59), RGBColor(51, 65, 85))
    m_box = slide1.shapes.add_textbox(Inches(2.2), Inches(4.6), Inches(8.933), Inches(2.0))
    tf_m = m_box.text_frame
    
    rows_meta = [
        ("Anchor Convener:", "Canara Bank (SLBC Convener) & Karnataka Banking Consortium (SBI, KVGB, Karnataka Bank)"),
        ("Government Stakeholders:", "Dept. of Agriculture, Bhoomi (Revenue Dept), FRUITS, CeG, RBI & NABARD"),
        ("Project Lead & Architect:", "Sarath Babu Rayaprolu (Founder & Lead Architect)"),
        ("Demonstration Portal:", "https://kisan.digikavach.net  |  Native Android APK Ready"),
        ("Meeting Objective:", "Approval for Statewide Phase 2 Rollout & Core Banking System (CBS) API Integration")
    ]
    for i, (k, v) in enumerate(rows_meta):
        p = tf_m.paragraphs[0] if i == 0 else tf_m.add_paragraph()
        run_k = p.add_run()
        run_k.text = f"{k:26} "
        run_k.font.bold = True
        run_k.font.size = Pt(11)
        run_k.font.color.rgb = C_ORANGE
        run_v = p.add_run()
        run_v.text = v
        run_v.font.size = Pt(11)
        run_v.font.color.rgb = C_WHITE

    # ==========================================================
    # SLIDE 2: Executive Summary & The Problem Statement
    # ==========================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "The Agrarian Credit Bottleneck in Karnataka")

    col_w = Inches(3.64)
    h_cards = Inches(5.4)
    top_c = Inches(1.4)

    # Card 1: Farmer Friction
    add_card(slide2, Inches(0.8), top_c, col_w, h_cards, C_WHITE, RGBColor(254, 202, 202))
    b1 = slide2.shapes.add_textbox(Inches(1.0), Inches(1.6), col_w - Inches(0.4), h_cards - Inches(0.4))
    tf1 = b1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "FARMER PAIN POINTS"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(185, 28, 28) # Red

    bullets1 = [
        "30 to 45 Days Delay: Farmers wait over a month for standard KCC credit sanction.",
        "High Document Expense: Lost wages & travel costs exceed Rs. 3,500 visiting revenue and bank offices.",
        "Moneylender Trap: Urgent sowing needs force farmers into informal loans at 24% - 36% interest.",
        "Information Blindspot: Zero visibility on loan status; farmers make 4-6 branch visits in person.",
        "Cyber Vulnerability: Preyed upon by predatory loan apps, fake PM-KISAN links, and OTP siphoning."
    ]
    for b in bullets1:
        p = tf1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(10)
        p.font.color.rgb = C_SLATE_800
        p.space_after = Pt(8)

    # Card 2: Bank Friction
    add_card(slide2, Inches(4.84), top_c, col_w, h_cards, C_WHITE, RGBColor(254, 215, 170))
    b2 = slide2.shapes.add_textbox(Inches(5.04), Inches(1.6), col_w - Inches(0.4), h_cards - Inches(0.4))
    tf2 = b2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "BANKING CHALLENGES"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_ORANGE

    bullets2 = [
        "High File Costs: Rs. 2,200+ operating expense per physical loan folder processed.",
        "38% Rejection Rate: Defective land titles, mismatched survey numbers, and illegible RTCs.",
        "Ghost Borrowers: Inability to cross-verify physical identity against Bhoomi land deeds instantly.",
        "Duplicate Encumbrances: Farmers mortgaging same land parcel across cooperative and RRB branches.",
        "Audit Pressure: Extreme difficulty meeting RBI Priority Sector Lending (PSL) quotas efficiently."
    ]
    for b in bullets2:
        p = tf2.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(10)
        p.font.color.rgb = C_SLATE_800
        p.space_after = Pt(8)

    # Card 3: KisanKavach Impact
    add_card(slide2, Inches(8.88), top_c, col_w, h_cards, C_CARD_BG, RGBColor(167, 243, 208))
    b3 = slide2.shapes.add_textbox(Inches(9.08), Inches(1.6), col_w - Inches(0.4), h_cards - Inches(0.4))
    tf3 = b3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "KISANKAVACH TRANSFORMATION"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_PRIMARY

    bullets3 = [
        "Under 7-Day Turnaround: Slashes cycle time by 80% through instant digital appraisal.",
        "Rs. 1,500 Saved per File: Slashes bank origination overhead from Rs. 2,200 to Rs. 700.",
        "100% Elimination of Ghost Loans: Real-time Bhoomi RTC & FRUITS crop data matching.",
        "Guaranteed Audit Trail: Consent-governed timestamped logging compliant with DPDP Act.",
        "Active Cyber Shield: AI scans farmer SMS & WhatsApp to stop phishing before cash drains."
    ]
    for b in bullets3:
        p = tf3.add_paragraph()
        p.text = "✔ " + b
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_PRIMARY
        p.space_after = Pt(8)

    # ==========================================================
    # SLIDE 3: System Architecture (Zero Statutory Displacement)
    # ==========================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "System Architecture: Zero Statutory Displacement DPI")

    # Banner note
    nb = add_card(slide3, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.65), C_ORANGE_BG, RGBColor(254, 215, 170))
    tf_nb = slide3.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(11.333), Inches(0.5)).text_frame
    p_nb = tf_nb.paragraphs[0]
    p_nb.text = "ARCHITECTURAL PRINCIPLE: KisanKavach DOES NOT replace Bhoomi or FRUITS. It acts as an intelligent orchestration layer connecting state registries directly into Bank Core Banking Systems (CBS)."
    p_nb.font.bold = True
    p_nb.font.size = Pt(10.5)
    p_nb.font.color.rgb = RGBColor(154, 52, 18)

    # 4 Architecture Pillars
    p_w = Inches(2.78)
    p_gap = Inches(0.2)
    p_h = Inches(4.6)
    p_top = Inches(2.25)

    pillars = [
        ("BHOOMI REGISTRY", "Land Title & Encumbrance", C_PRIMARY, [
            "Real-time RTC / Pahani API pull",
            "Survey No. & Hissa validation",
            "Exact land extent & soil classification",
            "Sub-registrar encumbrance check",
            "Automated bank charge creation"
        ]),
        ("FRUITS PLATFORM", "Farmer Identity & Crops", RGBColor(13, 148, 136), [
            "Direct Farmer ID (FID) verification",
            "Seasonal crop declaration provenance",
            "Aadhaar-linked DBT eligibility",
            "Scale of Finance cross-check",
            "Zero duplicate benefit leakage"
        ]),
        ("BANK LOS & CBS", "Maker-Checker Portal", RGBColor(2, 132, 199), [
            "Auto-populated loan applications",
            "Instant CIBIL / Experian bureau pull",
            "Standardized underwriting queue",
            "Mandatory structured rejection codes",
            "Core Banking ISO-8583 / REST push"
        ]),
        ("CYBERKAVACH", "AI Fraud & Phishing Defense", C_ORANGE, [
            "Rural phishing & SMS heuristic scan",
            "Predatory loan APK detector",
            "Kannada & English scam parsing",
            "Real-time fraud advisory alerts",
            "Disbursement account protection"
        ])
    ]

    for i, (p_title, p_sub, p_col, p_items) in enumerate(pillars):
        left_pos = Inches(0.8) + i * (p_w + p_gap)
        add_card(slide3, left_pos, p_top, p_w, p_h, C_WHITE, p_col)
        
        # Header banner inside card
        c_banner = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, p_top, p_w, Inches(0.8))
        c_banner.fill.solid()
        c_banner.fill.fore_color.rgb = p_col
        c_banner.line.fill.background()
        
        tf_b = slide3.shapes.add_textbox(left_pos, p_top + Inches(0.08), p_w, Inches(0.65)).text_frame
        p = tf_b.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = p_title
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_WHITE
        p_s = tf_b.add_paragraph()
        p_s.alignment = PP_ALIGN.CENTER
        p_s.text = p_sub
        p_s.font.size = Pt(8.5)
        p_s.font.color.rgb = RGBColor(226, 232, 240)

        # Content bullets
        tf_c = slide3.shapes.add_textbox(left_pos + Inches(0.15), p_top + Inches(0.9), p_w - Inches(0.3), p_h - Inches(1.0)).text_frame
        tf_c.word_wrap = True
        for j, item in enumerate(p_items):
            p = tf_c.paragraphs[0] if j == 0 else tf_c.add_paragraph()
            p.text = "• " + item
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_SLATE_800
            p.space_after = Pt(8)

    # ==========================================================
    # SLIDE 4: 10-District Karnataka Pilot Metrics
    # ==========================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "10-District Karnataka Pilot: Quantified Performance")

    # 4 Top KPI Cards
    kpi_w = Inches(2.78)
    kpi_h = Inches(1.3)
    kpis = [
        ("FARMERS REGISTERED", "1,50,000+", "Across 10 Pilot Districts", C_PRIMARY),
        ("KCC LOANS SANCTIONED", "1,05,000", "70.0% Sanction Conversion", RGBColor(13, 148, 136)),
        ("CREDIT DISBURSED", "Rs. 1,890 Cr", "Avg Rs. 1,80,000 per card", C_ORANGE),
        ("TURNAROUND CYCLE", "6.2 Days", "Down from 35 days (82% faster)", RGBColor(2, 132, 199))
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        left_pos = Inches(0.8) + i * (kpi_w + Inches(0.2))
        add_card(slide4, left_pos, Inches(1.4), kpi_w, kpi_h, C_CARD_BG, col)
        tf = slide4.shapes.add_textbox(left_pos, Inches(1.45), kpi_w, kpi_h - Inches(0.1)).text_frame
        p1 = tf.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        p1.text = lbl
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = C_SLATE_600

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.text = val
        p2.font.size = Pt(19)
        p2.font.bold = True
        p2.font.color.rgb = col

        p3 = tf.add_paragraph()
        p3.alignment = PP_ALIGN.CENTER
        p3.text = sub
        p3.font.size = Pt(8)
        p3.font.color.rgb = C_SLATE_600

    # 2 Bottom split boxes: Pilot Districts Breakdown & Bank Operational Impact
    box_w = Inches(5.7)
    box_h = Inches(3.9)
    top_b = Inches(2.95)

    # Box Left: Districts
    add_card(slide4, Inches(0.8), top_b, box_w, box_h, C_WHITE)
    tf_l = slide4.shapes.add_textbox(Inches(1.0), top_b + Inches(0.2), box_w - Inches(0.4), box_h - Inches(0.4)).text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "10 PILOT DISTRICTS REPRESENTED"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_PRIMARY

    districts = [
        "1. Mysuru (Southern Agri Zone) — 16,400 Sanctions",
        "2. Mandya (Sugarcane & Irrigation Belt) — 14,800 Sanctions",
        "3. Hassan (Plantation & Cash Crops) — 11,200 Sanctions",
        "4. Belagavi (Commercial & Sugar Hub) — 15,300 Sanctions",
        "5. Ballari (Mining & Dryland Agriculture) — 9,800 Sanctions",
        "6. Kalaburagi (Tur & Pulses Bowl) — 10,100 Sanctions",
        "7. Tumakuru (Horticulture & Oilseeds) — 9,500 Sanctions",
        "8. Shivamogga (Malnad Paddy & Arecanut) — 6,800 Sanctions",
        "9. Davanagere (Central Cotton & Maize) — 6,200 Sanctions",
        "10. Bagalkote (Horticulture & Irrigation) — 4,900 Sanctions"
    ]
    for d in districts:
        p = tf_l.add_paragraph()
        p.text = "• " + d
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_SLATE_800
        p.space_after = Pt(2)

    # Box Right: Operational Impact
    add_card(slide4, Inches(6.833), top_b, box_w, box_h, C_WHITE)
    tf_r = slide4.shapes.add_textbox(Inches(7.033), top_b + Inches(0.2), box_w - Inches(0.4), box_h - Inches(0.4)).text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "BANKING CONSORTIUM EFFICIENCY GAINS"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_ORANGE

    gains = [
        "Zero Ghost Borrowers: 0 counterfeit or duplicate land claims escaped detection.",
        "Documentation Accuracy: Incomplete filings reduced from 38% to under 2.1%.",
        "Field Survey Efficiency: Bank field verification officers completed 4.2x more appraisals daily using mobile geo-tagged photos.",
        "Direct Bank Savings: Participating branches saved an average of Rs. 15.75 Lakhs each in underwriting overhead during the pilot.",
        "Customer Satisfaction: 94.2% farmer satisfaction rating reported across taluk grievance centers."
    ]
    for g in gains:
        p = tf_r.add_paragraph()
        p.text = "✔ " + g
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_SLATE_800
        p.space_after = Pt(6)

    # ==========================================================
    # SLIDE 5: Underwriting Revolution: Bank Maker-Checker Portal
    # ==========================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Underwriting Revolution: Bank Maker-Checker Portal")

    # 3 Workflow stages
    st_w = Inches(3.64)
    st_h = Inches(5.4)
    st_top = Inches(1.4)

    stages = [
        ("STAGE 1: MAKER APPRAISAL", "Field / Loan Officer", C_PRIMARY, [
            "Auto-Prefilled Data: Zero manual typing; applicant data pulled from Aadhaar, Bhoomi, and FRUITS.",
            "Scale of Finance Calculator: Pre-computes eligible credit based on notified crop acreage rates.",
            "Integrated Bureau Score: 1-click CIBIL / Experian pull embedded in loan file.",
            "Digital Field Verification: Geo-tagged, timestamped crop photos captured via mobile app.",
            "Recommendation Note: Automated draft appraisal note generated in 60 seconds."
        ]),
        ("STAGE 2: CHECKER SANCTION", "Branch Manager / Credit Head", RGBColor(2, 132, 199), [
            "Real-Time SLA Timers: Countdown display preventing regulatory breach under 7-day norms.",
            "Deviation Highlighting: Automatic alerts on multi-bank exposures or encumbrance anomalies.",
            "1-Click Sanction Letter: Generates bilingual KCC sanction memorandum instantly.",
            "Structured Rejections: Rejections require statutory categorized rationale for audit compliance.",
            "Transparent Ledger: No hidden rejections; farmer receives instant plain-language SMS status."
        ]),
        ("STAGE 3: CBS DISBURSEMENT", "Core Banking Automation", C_ORANGE, [
            "API Connectors: Direct interface with Finacle, BaNCS, and Flexcube via ISO-8583 / REST.",
            "Automated Charge Creation: Digital lien registration communicated to Bhoomi / Revenue portal.",
            "Direct Credit to Account: Subsidy subvention and interest subvention tracking activated.",
            "e-Parihara Alignment: Automatic enrollment in disaster relief and crop compensation registers.",
            "Automated SLBC Reporting: Eliminates manual branch reporting for district meetings."
        ])
    ]

    for i, (s_title, s_sub, s_col, s_bullets) in enumerate(stages):
        left_pos = Inches(0.8) + i * (st_w + Inches(0.4))
        add_card(slide5, left_pos, st_top, st_w, st_h, C_WHITE, s_col)

        # Header banner
        banner = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, st_top, st_w, Inches(0.85))
        banner.fill.solid()
        banner.fill.fore_color.rgb = s_col
        banner.line.fill.background()

        tf_h = slide5.shapes.add_textbox(left_pos, st_top + Inches(0.08), st_w, Inches(0.7)).text_frame
        p = tf_h.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = s_title
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_WHITE
        p_s = tf_h.add_paragraph()
        p_s.alignment = PP_ALIGN.CENTER
        p_s.text = s_sub
        p_s.font.size = Pt(8.5)
        p_s.font.color.rgb = RGBColor(241, 245, 249)

        tf_c = slide5.shapes.add_textbox(left_pos + Inches(0.15), st_top + Inches(0.95), st_w - Inches(0.3), st_h - Inches(1.1)).text_frame
        tf_c.word_wrap = True
        for j, b in enumerate(s_bullets):
            p = tf_c.paragraphs[0] if j == 0 else tf_c.add_paragraph()
            p.text = "• " + b
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_SLATE_800
            p.space_after = Pt(8)

    # ==========================================================
    # SLIDE 6: Fraud Defense & NPA Elimination
    # ==========================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Risk Mitigation: Zero Ghost Borrowers & NPA Prevention")

    # 4 Quadrants
    q_w = Inches(5.7)
    q_h = Inches(2.55)
    quads = [
        ("GHOST BORROWER ELIMINATION", "Triple Identity Match Protocol", C_PRIMARY, [
            "Farmer Aadhaar biometric/OTP cross-verified with UIDAI database.",
            "Name, photo, and relative details verified against Bhoomi RTC title deed.",
            "Farmer ID (FID) verified against FRUITS historical subsidy registry.",
            "Result: 100% elimination of impersonation and non-existent borrower claims."
        ]),
        ("DUPLICATE ENCUMBRANCE PREVENTION", "Cross-Bank Digital Lien Registry", RGBColor(13, 148, 136), [
            "Checks existing mortgages across commercial banks, RRBs, and DCCBs in real-time.",
            "Blocks simultaneous multi-bank loan applications using the same survey parcel.",
            "Sub-registrar office (Kaveri) encumbrance certificates linked to application.",
            "Result: Prevents systemic multi-bank loan stacking on a single asset."
        ]),
        ("LAND EXTENT & CROP AUTHENTICATION", "Satellite & Registry Correlation", RGBColor(2, 132, 199), [
            "Validates exact land boundaries from Bhoomi against revenue cadastral maps.",
            "Matches claimed crop against FRUITS seasonal crop survey declarations.",
            "Prevents high-value crop misdeclarations (e.g. claiming horticulture on fallow land).",
            "Result: Completely realistic Scale of Finance loan appraisals."
        ]),
        ("CYBERKAVACH PHISHING DEFENSE", "Agrarian Cyber Fraud Radar", C_ORANGE, [
            "DigiKavach-aligned heuristic scanner detects rural APK malware and scam links.",
            "Alerts farmers in Kannada and English before fraudsters can siphon loan proceeds.",
            "Monitors fake 'PM-KISAN bonus' phishing domains targeting rural account holders.",
            "Result: Preserves farmer credit liquidity and reduces default due to fraud."
        ])
    ]

    for i, (q_t, q_sub, q_col, q_b) in enumerate(quads):
        row = i // 2
        col = i % 2
        left_pos = Inches(0.8) + col * (q_w + Inches(0.333))
        top_pos = Inches(1.4) + row * (q_h + Inches(0.25))

        add_card(slide6, left_pos, top_pos, q_w, q_h, C_WHITE, q_col)
        
        tf = slide6.shapes.add_textbox(left_pos + Inches(0.2), top_pos + Inches(0.15), q_w - Inches(0.4), q_h - Inches(0.3)).text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = q_t
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = q_col

        p_s = tf.add_paragraph()
        p_s.text = q_sub
        p_s.font.size = Pt(8.5)
        p_s.font.bold = True
        p_s.font.color.rgb = C_SLATE_600
        p_s.space_after = Pt(4)

        for b in q_b:
            p = tf.add_paragraph()
            p.text = "• " + b
            p.font.size = Pt(9)
            p.font.color.rgb = C_SLATE_800
            p.space_after = Pt(2)

    # ==========================================================
    # SLIDE 7: Unit Economics & Bank Profitability
    # ==========================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Unit Economics: Bank Operational Cost Savings")

    # Left: Cost Breakdown Table
    table_shape = slide7.shapes.add_table(6, 4, Inches(0.8), Inches(1.4), Inches(7.2), Inches(3.2))
    table = table_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(1.5)
    table.columns[2].width = Inches(1.5)
    table.columns[3].width = Inches(1.6)

    table_data = [
        ["Cost Component", "Physical Paper", "KisanKavach", "Savings / Impact"],
        ["Document Collection & Notary", "Rs. 450", "Rs. 0", "100% Digital via Bhoomi"],
        ["Land & Crop Field Verification", "Rs. 650", "Rs. 250", "62% Faster / Geo-Photo"],
        ["Data Entry & Maker Appraisal", "Rs. 400", "Rs. 50", "Auto-Prefilled from APIs"],
        ["Branch Overhead & Paper Store", "Rs. 700", "Rs. 400", "Cloud / Audit Compliance"],
        ["TOTAL COST PER APPLICATION", "Rs. 2,200", "Rs. 700", "Rs. 1,500 Saved (68%)"]
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_PRIMARY
            elif r_idx == 5:
                p.font.bold = True
                p.font.color.rgb = C_ORANGE
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_ORANGE_BG
            else:
                p.font.color.rgb = C_SLATE_800
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_WHITE if r_idx % 2 == 1 else C_SLATE_50

    # Right: Institutional Financial Highlights
    add_card(slide7, Inches(8.3), Inches(1.4), Inches(4.233), Inches(5.4), C_WHITE, C_PRIMARY)
    tf_rh = slide7.shapes.add_textbox(Inches(8.5), Inches(1.6), Inches(3.833), Inches(5.0)).text_frame
    tf_rh.word_wrap = True
    p = tf_rh.paragraphs[0]
    p.text = "INSTITUTIONAL SAVINGS IMPACT"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_PRIMARY

    bullets_fin = [
        ("Rs. 30 Crore Annual Savings:", "A commercial bank originating 2,00,000 KCC files saves Rs. 30 Cr in direct branch overhead every year."),
        ("Zero Upfront Capex:", "KisanKavach operates on a pure success-based model (0.35% origination fee on disbursed credit). No capital outlay required."),
        ("Turnaround Acceleration:", "Branch managers process 3.5x more agricultural loan applications without expanding branch headcount."),
        ("NPA Provisioning Relief:", "1.2% reduction in non-performing loans frees up hundreds of crores in regulatory risk capital reserves."),
        ("RBI PSL Compliance:", "Ensures 100% adherence to RBI sub-targets for Small & Marginal Farmers (SMF) without audit penalties.")
    ]
    for title_b, desc_b in bullets_fin:
        p = tf_rh.add_paragraph()
        run1 = p.add_run()
        run1.text = title_b + " "
        run1.font.bold = True
        run1.font.size = Pt(9.5)
        run1.font.color.rgb = C_ORANGE
        run2 = p.add_run()
        run2.text = desc_b
        run2.font.size = Pt(9)
        run2.font.color.rgb = C_SLATE_800
        p.space_after = Pt(6)

    # Bottom Left Card: Commercial Model Summary
    add_card(slide7, Inches(0.8), Inches(4.8), Inches(7.2), Inches(2.0), C_CARD_BG, C_PRIMARY)
    tf_com = slide7.shapes.add_textbox(Inches(1.0), Inches(4.9), Inches(6.8), Inches(1.8)).text_frame
    tf_com.word_wrap = True
    p = tf_com.paragraphs[0]
    p.text = "PROPOSED SLBC COMMERCIAL & LICENSING MODEL"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = C_PRIMARY

    c_points = [
        "• Loan Origination Fee: 0.35% of disbursed credit (paid upon successful disbursement).",
        "• Branch SaaS License: Rs. 35,00,0 / branch / year (covers portal, SLA engine & command desk).",
        "• State Enterprise DPI Support: Tiered annual SLA contract with Karnataka Agriculture Dept.",
        "• Free for Smallholder Farmers: Zero platform fees charged to farmers for basic KCC applications."
    ]
    for cp in c_points:
        p = tf_com.add_paragraph()
        p.text = cp
        p.font.size = Pt(9)
        p.font.color.rgb = C_SLATE_800
        p.space_after = Pt(2)

    # ==========================================================
    # SLIDE 8: State Command Center & SLBC Dashboard
    # ==========================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "State Command Center & Real-Time SLBC Oversight")

    # 3 Command Center Pillars
    cc_w = Inches(3.64)
    cc_h = Inches(5.4)
    cc_top = Inches(1.4)

    cc_pillars = [
        ("EXECUTIVE VISIBILITY", "District & Taluk Drilldowns", C_PRIMARY, [
            "Real-time heatmaps tracking agricultural credit velocity across all 31 districts & 240 taluks.",
            "Compare disbursement pace against targets set by SLBC and State Credit Plan.",
            "Instant detection of regional credit deserts and underserved agrarian clusters.",
            "1-click export of SLBC review reports in standard PDF and Excel formats."
        ]),
        ("BANK PERFORMANCE RADAR", "Bank & Branch Benchmarking", RGBColor(2, 132, 199), [
            "Live scorecards comparing SBI, Canara Bank, KVGB, Karnataka Bank, and DCCBs.",
            "Turnaround time (TAT) tracking identifying branches failing 7-day norms.",
            "Sanction conversion rate analysis highlighting abnormal rejection spikes.",
            "Branch field verification efficiency tracking."
        ]),
        ("SLA ENFORCEMENT & RECOURSE", "District Collector Escalation", C_ORANGE, [
            "Automated countdown timer on every loan file visible to applicant and bank.",
            "SLA breach escalation engine automatically flags overdue applications to District Collectors.",
            "Centralized citizen grievance tracking resolving farmer appeals under 10 days.",
            "Transparent audit trail preventing arbitrary documentary rejections."
        ])
    ]

    for i, (title, sub, col, bullets) in enumerate(cc_pillars):
        left_pos = Inches(0.8) + i * (cc_w + Inches(0.4))
        add_card(slide8, left_pos, cc_top, cc_w, cc_h, C_WHITE, col)

        # Header banner
        b = slide8.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, cc_top, cc_w, Inches(0.85))
        b.fill.solid()
        b.fill.fore_color.rgb = col
        b.line.fill.background()

        tf_h = slide8.shapes.add_textbox(left_pos, cc_top + Inches(0.08), cc_w, Inches(0.7)).text_frame
        p = tf_h.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = title
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_WHITE
        p_s = tf_h.add_paragraph()
        p_s.alignment = PP_ALIGN.CENTER
        p_s.text = sub
        p_s.font.size = Pt(8.5)
        p_s.font.color.rgb = RGBColor(241, 245, 249)

        tf_c = slide8.shapes.add_textbox(left_pos + Inches(0.15), cc_top + Inches(0.95), cc_w - Inches(0.3), cc_h - Inches(1.1)).text_frame
        tf_c.word_wrap = True
        for j, item in enumerate(bullets):
            p = tf_c.paragraphs[0] if j == 0 else tf_c.add_paragraph()
            p.text = "• " + item
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_SLATE_800
            p.space_after = Pt(10)

    # ==========================================================
    # SLIDE 9: Security, DPDP Compliance & Regulatory Alignment
    # ==========================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Data Governance, Security & DPDP Compliance")

    # 4 Governance Pillars
    g_w = Inches(5.7)
    g_h = Inches(2.55)
    g_cards = [
        ("DPDP ACT 2023 COMPLIANCE", "Consent-Governed Data Architecture", C_PRIMARY, [
            "Explicit, notice-based farmer consent before pulling Bhoomi or FRUITS records.",
            "Granular consent logs recorded with immutable digital timestamps.",
            "Farmer right-to-revoke and data portability compliance.",
            "Zero data monetization or unauthorized secondary sharing."
        ]),
        ("BANK-GRADE CYBER SECURITY", "MeitY Empaneled Cloud Infrastructure", RGBColor(13, 148, 136), [
            "256-bit TLS encryption in transit and AES-256 encryption at rest.",
            "CERT-In empaneled security audit readiness with continuous vulnerability scans.",
            "Strict Role-Based Access Control (RBAC) across Maker, Checker, and Admin personas.",
            "Zero trust network architecture with multi-factor authentication (MFA)."
        ]),
        ("RBI MASTER DIRECTIONS ALIGNMENT", "Priority Sector Lending Guidelines", RGBColor(2, 132, 199), [
            "Full compliance with RBI guidelines on Kisan Credit Card (KCC) scheme limits.",
            "Automated classification of Small & Marginal Farmers (SMF) for PSL reporting.",
            "Interest Subvention Scheme (ISS) reporting and audit trail generation.",
            "Scale of Finance norms verified against District Technical Committee mandates."
        ]),
        ("SOVEREIGN DATA RESIDENCY", "Zero Offshore Data Transmission", C_ORANGE, [
            "100% of databases and application servers hosted within sovereign Indian borders.",
            "Integrated with State Data Centre (SDC) guidelines for Karnataka e-Governance.",
            "Statutory records remain in Bhoomi and FRUITS; KisanKavach acts as pass-through pipeline.",
            "Complete business continuity and disaster recovery (BCP/DR) protocol."
        ])
    ]

    for i, (gt, gsub, gcol, gbullets) in enumerate(g_cards):
        row = i // 2
        col = i % 2
        left_pos = Inches(0.8) + col * (g_w + Inches(0.333))
        top_pos = Inches(1.4) + row * (g_h + Inches(0.25))

        add_card(slide9, left_pos, top_pos, g_w, g_h, C_WHITE, gcol)
        
        tf = slide9.shapes.add_textbox(left_pos + Inches(0.2), top_pos + Inches(0.15), g_w - Inches(0.4), g_h - Inches(0.3)).text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = gt
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = gcol

        p_s = tf.add_paragraph()
        p_s.text = gsub
        p_s.font.size = Pt(8.5)
        p_s.font.bold = True
        p_s.font.color.rgb = C_SLATE_600
        p_s.space_after = Pt(4)

        for b in gbullets:
            p = tf.add_paragraph()
            p.text = "• " + b
            p.font.size = Pt(9)
            p.font.color.rgb = C_SLATE_800
            p.space_after = Pt(2)

    # ==========================================================
    # SLIDE 10: Statewide Rollout Roadmap (2026–2028)
    # ==========================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "Statewide Rollout Roadmap & CBS Integration Plan")

    r_w = Inches(2.78)
    r_h = Inches(5.4)
    r_top = Inches(1.4)

    phases = [
        ("PHASE 1 (COMPLETED)", "10 Pilot Districts", "Months 1 – 6 (2026)", C_PRIMARY, [
            "Next.js 15 PWA & Android APK deployed.",
            "Bhoomi & FRUITS sandbox connectors verified.",
            "1,50,000 farmers onboarded.",
            "1,05,000 KCC loans sanctioned.",
            "Rs. 1,890 Cr credit throughput.",
            "Zero ghost borrower breaches."
        ]),
        ("PHASE 2 (CURRENT FOCUS)", "All 31 KA Districts", "Months 7 – 18 (2027)", RGBColor(2, 132, 199), [
            "Full statewide expansion to 240+ taluks.",
            "Direct Core Banking (CBS) ISO-8583 push.",
            "Automated CIBIL bureau pull.",
            "5,00,000 active farmer accounts.",
            "Rs. 6,750 Cr credit throughput.",
            "Command Center in all 31 Collectorates."
        ]),
        ("PHASE 3 (VALUE CHAIN)", "Insurance & Input Credit", "Months 19 – 36 (2028-29)", RGBColor(13, 148, 136), [
            "PMFBY satellite claim automation.",
            "KSNDMC hyper-local weather alerts.",
            "FPO group loan origination module.",
            "Agri-input credit checkout APIs.",
            "AI Kannada conversational voice assistant.",
            "12,00,000 active farmers."
        ]),
        ("PHASE 4 (NATIONAL SCALE)", "AgriStack Federation", "Months 37 – 60 (2029-31)", C_ORANGE, [
            "Full integration with GoI AgriStack / UFSP.",
            "Multi-state land registry adaptors (AP, TS, MH).",
            "e-NWR electronic warehouse pledge credit.",
            "50,00,000 active farmers.",
            "Rs. 72,000 Cr annual credit throughput.",
            "Sovereign DPI export framework."
        ])
    ]

    for i, (ph_name, ph_scope, ph_time, ph_col, ph_b) in enumerate(phases):
        left_pos = Inches(0.8) + i * (r_w + Inches(0.2))
        add_card(slide10, left_pos, r_top, r_w, r_h, C_WHITE, ph_col)

        # Header banner
        b = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, r_top, r_w, Inches(1.0))
        b.fill.solid()
        b.fill.fore_color.rgb = ph_col
        b.line.fill.background()

        tf_h = slide10.shapes.add_textbox(left_pos, r_top + Inches(0.08), r_w, Inches(0.85)).text_frame
        p = tf_h.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = ph_name
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = C_WHITE
        p_s = tf_h.add_paragraph()
        p_s.alignment = PP_ALIGN.CENTER
        p_s.text = ph_scope
        p_s.font.size = Pt(8.5)
        p_s.font.bold = True
        p_s.font.color.rgb = RGBColor(254, 215, 170)
        p_t = tf_h.add_paragraph()
        p_t.alignment = PP_ALIGN.CENTER
        p_t.text = ph_time
        p_t.font.size = Pt(8)
        p_t.font.color.rgb = RGBColor(241, 245, 249)

        tf_c = slide10.shapes.add_textbox(left_pos + Inches(0.12), r_top + Inches(1.1), r_w - Inches(0.24), r_h - Inches(1.2)).text_frame
        tf_c.word_wrap = True
        for j, item in enumerate(ph_b):
            p = tf_c.paragraphs[0] if j == 0 else tf_c.add_paragraph()
            p.text = "• " + item
            p.font.size = Pt(9)
            p.font.color.rgb = C_SLATE_800
            p.space_after = Pt(6)

    # ==========================================================
    # SLIDE 11: Proposed Resolution for SLBC Plenary
    # ==========================================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "Proposed Resolutions for SLBC Plenary Approval")

    # 4 Actionable Resolution Cards
    res_w = Inches(5.7)
    res_h = Inches(2.55)
    resolutions = [
        ("RESOLUTION 1: DIGITAL GATEWAY EMPANELMENT", "Official State Credit Gateway", C_PRIMARY, [
            "Formal adoption of KisanKavach as the official Digital Public Infrastructure (DPI) orchestration gateway for Kisan Credit Card (KCC) originations across Karnataka.",
            "Recognition of digital Bhoomi RTC & FRUITS validation as valid legal prefill.",
            "Authorization to establish standardized Maker-Checker portals in partner branches."
        ]),
        ("RESOLUTION 2: CORE BANKING API INTEGRATION", "CBS Sandbox Authorization", RGBColor(2, 132, 199), [
            "Authorize IT teams of anchor banks (Canara, SBI, KVGB, Karnataka Bank) to provide secure API connectors for core banking disbursement and charge lien push.",
            "Deploy automated CIBIL score query integration within the Maker appraisal flow.",
            "Enable digital e-Sign / Aadhaar OTP disbursement document signing."
        ]),
        ("RESOLUTION 3: JOINT IMPLEMENTATION TASKFORCE", "5-Member Steering Committee", RGBColor(13, 148, 136), [
            "Constitute an SLBC-KisanKavach joint working committee comprising:",
            "• SLBC Convener Representative (Canara Bank)",
            "• Lead District Managers (LDMs) of Pilot Districts",
            "• State Dept of Agriculture & Bhoomi Nodal Officers",
            "• KisanKavach Lead Architect (Sarath Babu Rayaprolu)"
        ]),
        ("RESOLUTION 4: STATEWIDE PHASE 2 ROLLOUT MANDATE", "31 Districts Rollout Schedule", C_ORANGE, [
            "Approve schedule to expand from 10 pilot districts to all 31 Karnataka districts.",
            "Target onboarding 5,00,000 smallholder farmers in FY 2026-27.",
            "Facilitate Rs. 6,750 Crore in prioritized agricultural credit through partner banks.",
            "Mandate quarterly progress reviews at future SLBC plenary meetings."
        ])
    ]

    for i, (rt, rsub, rcol, rbullets) in enumerate(resolutions):
        row = i // 2
        col = i % 2
        left_pos = Inches(0.8) + col * (res_w + Inches(0.333))
        top_pos = Inches(1.4) + row * (res_h + Inches(0.25))

        add_card(slide11, left_pos, top_pos, res_w, res_h, C_WHITE, rcol)
        
        tf = slide11.shapes.add_textbox(left_pos + Inches(0.2), top_pos + Inches(0.15), res_w - Inches(0.4), res_h - Inches(0.3)).text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = rt
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = rcol

        p_s = tf.add_paragraph()
        p_s.text = rsub
        p_s.font.size = Pt(8.5)
        p_s.font.bold = True
        p_s.font.color.rgb = C_SLATE_600
        p_s.space_after = Pt(4)

        for b in rbullets:
            p = tf.add_paragraph()
            p.text = "• " + b
            p.font.size = Pt(9)
            p.font.color.rgb = C_SLATE_800
            p.space_after = Pt(2)

    # ==========================================================
    # SLIDE 12: Conclusion & Q&A (Dark Theme)
    # ==========================================================
    slide12 = prs.slides.add_slide(blank_layout)
    bg12 = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg12.fill.solid()
    bg12.fill.fore_color.rgb = C_DARK_BG
    bg12.line.fill.background()

    # Top accent line
    stripe12 = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    stripe12.fill.solid()
    stripe12.fill.fore_color.rgb = C_ORANGE
    stripe12.line.fill.background()

    if os.path.exists(logo_path):
        slide12.shapes.add_picture(logo_path, Inches(5.9), Inches(0.8), width=Inches(1.5))

    t12_box = slide12.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(11.333), Inches(1.5))
    tf12 = t12_box.text_frame
    p1 = tf12.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "Empowering Karnataka's Agrarian Economy"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    p2 = tf12.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "Rapid, Transparent & Fraud-Free Digital Agricultural Lending"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = C_ORANGE

    # Contact / Q&A Card
    c_card = add_card(slide12, Inches(2.5), Inches(4.2), Inches(8.333), Inches(2.5), RGBColor(30, 41, 59), RGBColor(51, 65, 85))
    tf_contact = slide12.shapes.add_textbox(Inches(2.7), Inches(4.35), Inches(7.933), Inches(2.2)).text_frame
    
    c_lines = [
        ("Author & Presenter:", "Sarath Babu Rayaprolu (Founder & Lead System Architect)"),
        ("Production Web Platform:", "https://kisan.digikavach.net"),
        ("Live Demonstration:", "Maker-Checker Loan Underwriting & District Command Center"),
        ("Mobile APK Build:", "Native Android Build Ready for Field Demonstration"),
        ("Headquarters / Ops:", "Bengaluru, Karnataka  |  Contact: sarath@digikavach.net")
    ]
    for i, (k, v) in enumerate(c_lines):
        p = tf_contact.paragraphs[0] if i == 0 else tf_contact.add_paragraph()
        run_k = p.add_run()
        run_k.text = f"{k:25} "
        run_k.font.bold = True
        run_k.font.size = Pt(11)
        run_k.font.color.rgb = C_ORANGE
        run_v = p.add_run()
        run_v.text = v
        run_v.font.size = Pt(11)
        run_v.font.color.rgb = C_WHITE

    prs.save(output_path)
    print(f"PowerPoint Presentation saved successfully to: {output_path}")


# ==============================================================================
# REPORTLAB PDF PRESENTATION GENERATOR (Landscape 16:9 Presentation Format)
# ==============================================================================
class NumberedCanvasLandscape(canvas.Canvas):
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        # Skip header & footer on Slide 1 and Slide 12 (Dark cover slides)
        if self._pageNumber in (1, page_count):
            return

        w, h = landscape(A4)
        self.saveState()

        # Top Header Banner
        self.setFillColor(colors.HexColor("#044E29")) # Deep Forest Green
        self.rect(0, h - 50, w, 50, fill=1, stroke=0)

        # Header Title
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#EA580C")) # Saffron Orange
        self.drawString(36, h - 20, "STATE LEVEL BANKERS' COMMITTEE (SLBC) KARNATAKA — ANCHOR PRESENTATION")

        self.setFont("Helvetica-Bold", 12)
        self.setFillColor(colors.white)
        self.drawString(36, h - 38, "KISANKAVACH: DIGITAL AGRICULTURAL CREDIT & FRAUD DEFENSE")

        # Right Header Tag
        self.setFont("Helvetica-Bold", 9)
        self.setFillColor(colors.HexColor("#EA580C"))
        self.drawRightString(w - 36, h - 28, "PRESENTER: SARATH BABU RAYAPROLU")

        # Bottom Footer Bar
        self.setFillColor(colors.HexColor("#F8FAFC"))
        self.rect(0, 0, w, 28, fill=1, stroke=0)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(0, 28, w, 28)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(36, 10, "Confidential - State Level Bankers' Committee (SLBC) Karnataka & Partner Banks (SBI, Canara, KVGB)")

        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#044E29"))
        self.drawRightString(w - 36, 10, f"kisan.digikavach.net  |  Slide {self._pageNumber} of {page_count}")
        self.restoreState()


def create_pdf_deck(pdf_path, logo_path):
    w, h = landscape(A4) # 841.89 x 595.27 points
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(A4),
        leftMargin=36,
        rightMargin=36,
        topMargin=58,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    c_primary = colors.HexColor("#044E29")
    c_secondary = colors.HexColor("#EA580C")
    c_dark = colors.HexColor("#0F172A")
    c_slate = colors.HexColor("#334155")
    c_border = colors.HexColor("#CBD5E1")
    c_card_bg = colors.HexColor("#ECFDF5")
    c_orange_bg = colors.HexColor("#FFF7ED")

    story = []

    # Helper styles
    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary,
        spaceAfter=12
    )

    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_slate
    )

    bold_body_style = ParagraphStyle(
        'SlideBoldBody',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=c_dark
    )

    card_header_style = ParagraphStyle(
        'CardHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_primary
    )

    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=c_primary,
        spaceAfter=6
    )

    cover_subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=c_secondary,
        spaceAfter=4
    )

    cover_tag_style = ParagraphStyle(
        'CoverTag',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=c_slate,
        spaceAfter=15
    )

    concl_title_style = ParagraphStyle(
        'ConclTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=c_primary,
        spaceAfter=6
    )

    concl_subtitle_style = ParagraphStyle(
        'ConclSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=c_secondary,
        spaceAfter=15
    )

    # -------------------------------------------------------------
    # SLIDE 1: Cover Slide
    # -------------------------------------------------------------
    story.append(Spacer(1, 15))
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=70, height=82))
        story.append(Spacer(1, 12))

    story.append(Paragraph("<b>KISANKAVACH</b>", cover_title_style))
    story.append(Paragraph("<b>Next-Generation Digital Public Infrastructure for Agricultural Credit & Fraud Defense</b>", cover_subtitle_style))
    story.append(Paragraph("State Level Bankers' Committee (SLBC) Karnataka — Anchor Presentation", cover_tag_style))
    story.append(Spacer(1, 10))

    meta_table_data = [
        [
            Paragraph("<b>Anchor Convener:</b>", bold_body_style),
            Paragraph("Canara Bank (SLBC Convener) & Member Banks (SBI, Karnataka Gramin Bank, Karnataka Bank)", body_style)
        ],
        [
            Paragraph("<b>Government & Regulators:</b>", bold_body_style),
            Paragraph("Dept. of Agriculture, Bhoomi (Revenue), FRUITS, CeG, Reserve Bank of India (RBI), NABARD", body_style)
        ],
        [
            Paragraph("<b>Presenter & Author:</b>", bold_body_style),
            Paragraph("<b>Sarath Babu Rayaprolu</b> (Founder & Solution Architect)", bold_body_style)
        ],
        [
            Paragraph("<b>Live Platform & APK:</b>", bold_body_style),
            Paragraph("https://kisan.digikavach.net  |  Native Android APK Build Ready", body_style)
        ],
        [
            Paragraph("<b>Meeting Objective:</b>", bold_body_style),
            Paragraph("Formal Empanelment, Core Banking System (CBS) API Authorization & Statewide Rollout across 31 Districts", body_style)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[180, 560])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 2: Problem Statement
    # -------------------------------------------------------------
    story.append(Paragraph("The Agrarian Credit Bottleneck in Karnataka", slide_title_style))
    story.append(Paragraph("India's 140M farmers and Karnataka's 8.2M landholders face deep operational friction in institutional credit delivery, creating severe costs for banks and driving farmers to moneylenders.", body_style))
    story.append(Spacer(1, 15))

    prob_data = [
        [
            Paragraph("<b>FARMER CHALLENGES</b>", card_header_style),
            Paragraph("<b>BANK OPERATIONAL FRICTION</b>", card_header_style),
            Paragraph("<b>KISANKAVACH TRANSFORMATION</b>", card_header_style)
        ],
        [
            Paragraph(
                "• <b>30 to 45 Day Turnaround:</b> Farmers wait over a month for basic KCC credit.<br/>"
                "• <b>Rs. 3,500+ Lost per Loan:</b> Travel, wage losses & private documentation agents.<br/>"
                "• <b>24%-36% Moneylender Trap:</b> High borrowing costs due to bank delays.<br/>"
                "• <b>Zero Visibility:</b> Opacity leads to repeated physical branch visits.<br/>"
                "• <b>Cyber Scams:</b> Farmers victimized by WhatsApp/SMS OTP phishing.",
                body_style
            ),
            Paragraph(
                "• <b>Rs. 2,200+ Cost per File:</b> High physical processing and manual survey costs.<br/>"
                "• <b>38% Rejection Rate:</b> Disconnected, outdated, or defective land titles.<br/>"
                "• <b>Ghost Borrowers & Fraud:</b> Impersonation and forged physical land records.<br/>"
                "• <b>Multi-Bank Lien Risk:</b> Same land mortgaged across multiple institutions.<br/>"
                "• <b>PSL Pressure:</b> High compliance stress meeting RBI Priority Sector quotas.",
                body_style
            ),
            Paragraph(
                "✔ <b>Turnaround &lt; 7 Days:</b> 80% acceleration via instant digital validation.<br/>"
                "✔ <b>Rs. 1,500 Saved per Loan:</b> Origination cost reduced from Rs. 2,200 to Rs. 700.<br/>"
                "✔ <b>100% Verified Identity:</b> Direct Bhoomi RTC & FRUITS crop integration.<br/>"
                "✔ <b>Zero Ghost Borrowers:</b> Aadhaar-locked biometric and title provenance.<br/>"
                "✔ <b>Proactive Cyber Shield:</b> Heuristic phishing detection protecting accounts.",
                bold_body_style
            )
        ]
    ]
    prob_table = Table(prob_data, colWidths=[245, 255, 260])
    prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#FEF2F2")),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#FFF7ED")),
        ('BACKGROUND', (2, 0), (2, 0), c_card_bg),
        ('BOX', (0, 0), (0, 1), 1, colors.HexColor("#FCA5A5")),
        ('BOX', (1, 0), (1, 1), 1, colors.HexColor("#FDBA74")),
        ('BOX', (2, 0), (2, 1), 1.5, c_primary),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(prob_table)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 3: System Architecture (Zero Statutory Displacement)
    # -------------------------------------------------------------
    story.append(Paragraph("System Architecture: Zero Statutory Displacement DPI", slide_title_style))
    story.append(Paragraph("<b>Architectural Mandate:</b> KisanKavach does NOT replace statutory systems of record (Bhoomi or FRUITS). Instead, it serves as an enterprise orchestration and fraud-defense highway connecting state registries directly into Bank Core Banking Systems (CBS).", body_style))
    story.append(Spacer(1, 15))

    arch_data = [
        [
            Paragraph("<b>1. BHOOMI REGISTRY</b><br/><font size=7 color='#044E29'>Land Titles & Encumbrance</font>", card_header_style),
            Paragraph("<b>2. FRUITS PLATFORM</b><br/><font size=7 color='#0D9488'>Farmer Identity & Crops</font>", card_header_style),
            Paragraph("<b>3. BANK LOS & CBS</b><br/><font size=7 color='#0284C7'>Maker-Checker Portal</font>", card_header_style),
            Paragraph("<b>4. CYBERKAVACH</b><br/><font size=7 color='#EA580C'>AI Fraud & Scam Defense</font>", card_header_style)
        ],
        [
            Paragraph(
                "• Real-time RTC / Pahani API query<br/>"
                "• Survey No. & Hissa validation<br/>"
                "• Exact extent & soil classification<br/>"
                "• Sub-registrar encumbrance check<br/>"
                "• Automated bank charge creation",
                body_style
            ),
            Paragraph(
                "• Direct Farmer ID (FID) verification<br/>"
                "• Seasonal crop declaration history<br/>"
                "• Aadhaar-linked DBT eligibility<br/>"
                "• Scale of Finance validation<br/>"
                "• Zero duplicate benefit leakage",
                body_style
            ),
            Paragraph(
                "• Auto-prefilled loan applications<br/>"
                "• Instant CIBIL bureau credit pull<br/>"
                "• Maker-Checker underwriting queue<br/>"
                "• Mandatory rejection taxonomy<br/>"
                "• Core Banking ISO-8583 / REST push",
                body_style
            ),
            Paragraph(
                "• Rural phishing & SMS heuristic scan<br/>"
                "• Predatory loan APK detector<br/>"
                "• Kannada & English scam parsing<br/>"
                "• Real-time fraud advisory push<br/>"
                "• Disbursement account protection",
                body_style
            )
        ]
    ]
    arch_table = Table(arch_data, colWidths=[190, 190, 190, 190])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(arch_table)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 4: Pilot Metrics
    # -------------------------------------------------------------
    story.append(Paragraph("10-District Karnataka Pilot: Quantified Performance", slide_title_style))
    story.append(Paragraph("Live operational metrics across 10 diverse pilot districts validating speed, scale, and loss elimination.", body_style))
    story.append(Spacer(1, 10))

    kpi_data = [
        [
            Paragraph("<font size=8 color='#64748B'>FARMERS ONBOARDED</font><br/><b><font size=16 color='#044E29'>1,50,000+</font></b><br/><font size=7 color='#64748B'>Across 10 Pilot Districts</font>", styles['Normal']),
            Paragraph("<font size=8 color='#64748B'>KCC LOANS SANCTIONED</font><br/><b><font size=16 color='#0D9488'>1,05,000</font></b><br/><font size=7 color='#64748B'>70.0% Sanction Conversion</font>", styles['Normal']),
            Paragraph("<font size=8 color='#64748B'>CREDIT FACILITATED</font><br/><b><font size=16 color='#EA580C'>Rs. 1,890 Cr</font></b><br/><font size=7 color='#64748B'>Avg Rs. 1.80L per sanction</font>", styles['Normal']),
            Paragraph("<font size=8 color='#64748B'>AVERAGE TURNAROUND</font><br/><b><font size=16 color='#0284C7'>6.2 Days</font></b><br/><font size=7 color='#64748B'>Down from 35 days (82% faster)</font>", styles['Normal'])
        ]
    ]
    kpi_t = Table(kpi_data, colWidths=[190, 190, 190, 190])
    kpi_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(kpi_t)
    story.append(Spacer(1, 12))

    pilot_split_data = [
        [
            Paragraph("<b>PILOT DISTRICT DISTRIBUTION</b>", card_header_style),
            Paragraph("<b>KEY BANKING CONSORTIUM OUTCOMES</b>", card_header_style)
        ],
        [
            Paragraph(
                "• <b>Mysuru:</b> 16,400 Sanctions (Southern Agri Belt)<br/>"
                "• <b>Mandya:</b> 14,800 Sanctions (Sugarcane & Paddy)<br/>"
                "• <b>Belagavi:</b> 15,300 Sanctions (Commercial & Cotton)<br/>"
                "• <b>Hassan:</b> 11,200 Sanctions (Plantation Crops)<br/>"
                "• <b>Kalaburagi:</b> 10,100 Sanctions (Pulses & Tur Hub)<br/>"
                "• <b>Ballari, Tumakuru, Shivamogga, Davanagere, Bagalkote:</b> 37,200 Sanctions",
                body_style
            ),
            Paragraph(
                "✔ <b>Zero Ghost Borrowers:</b> Zero counterfeit land records or ghost claims.<br/>"
                "✔ <b>Application Accuracy:</b> Incomplete files dropped from 38% to under 2.1%.<br/>"
                "✔ <b>Field Appraisals:</b> Field officers executed 4.2x more appraisals per day.<br/>"
                "✔ <b>Branch Operational Savings:</b> Participating branches saved ~Rs. 15.75L each.<br/>"
                "✔ <b>Farmer Satisfaction:</b> 94.2% satisfaction index across district centers.",
                bold_body_style
            )
        ]
    ]
    pilot_split_table = Table(pilot_split_data, colWidths=[375, 385])
    pilot_split_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(pilot_split_table)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 5: Underwriting Portal & Maker-Checker Workflow
    # -------------------------------------------------------------
    story.append(Paragraph("Underwriting Revolution: Bank Maker-Checker Portal", slide_title_style))
    story.append(Paragraph("Standardizing credit underwriting with zero paperwork, instant bureau scores, and automated SLA compliance.", body_style))
    story.append(Spacer(1, 15))

    los_data = [
        [
            Paragraph("<b>STAGE 1: MAKER APPRAISAL</b><br/><font size=7 color='#044E29'>Field & Loan Officers</font>", card_header_style),
            Paragraph("<b>STAGE 2: CHECKER SANCTION</b><br/><font size=7 color='#0284C7'>Branch Managers</font>", card_header_style),
            Paragraph("<b>STAGE 3: CBS DISBURSEMENT</b><br/><font size=7 color='#EA580C'>Core Banking Push</font>", card_header_style)
        ],
        [
            Paragraph(
                "• <b>Zero Manual Data Entry:</b> Land, crop, and applicant details auto-prefilled.<br/>"
                "• <b>Scale of Finance Engine:</b> Instant credit limit calculation based on crop acreage.<br/>"
                "• <b>Real-Time Credit Bureau:</b> 1-click CIBIL / Experian pull embedded in workflow.<br/>"
                "• <b>Geo-Tagged Verification:</b> Field officers upload verified crop photos.<br/>"
                "• <b>Auto Appraisal Note:</b> Standardized risk assessment draft in 60 seconds.",
                body_style
            ),
            Paragraph(
                "• <b>Live SLA Countdown:</b> Real-time timer preventing 7-day regulatory breach.<br/>"
                "• <b>Anomaly Alerts:</b> Flags multi-bank exposures or encumbrance conflicts.<br/>"
                "• <b>1-Click Sanction Letter:</b> Bilingual statutory sanction memo generated.<br/>"
                "• <b>Mandatory Rejection Codes:</b> Rejections require structured rationale.<br/>"
                "• <b>Transparent Recourse:</b> Farmer receives instant SMS notification.",
                body_style
            ),
            Paragraph(
                "• <b>Direct CBS Integration:</b> Finacle, BaNCS, Flexcube via ISO-8583 / REST.<br/>"
                "• <b>Digital Lien Creation:</b> Charge registration communicated to Bhoomi.<br/>"
                "• <b>Subvention Tracking:</b> Automated interest subvention registry active.<br/>"
                "• <b>e-Parihara Alignment:</b> Linked to state disaster compensation registry.<br/>"
                "• <b>Automated SLBC Filing:</b> Eliminates manual branch reporting.",
                body_style
            )
        ]
    ]
    los_table = Table(los_data, colWidths=[250, 255, 255])
    los_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(los_table)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 6: Unit Economics & Bank Profitability
    # -------------------------------------------------------------
    story.append(Paragraph("Unit Economics: Direct Bank Operational Savings", slide_title_style))
    story.append(Paragraph("Demonstrating significant operational savings for participating banks alongside an asset-light, success-based fee structure.", body_style))
    story.append(Spacer(1, 10))

    cost_data = [
        ["Cost Component", "Physical Paper Process", "KisanKavach Digital", "Operational Impact"],
        ["Document Collection & Verification", "Rs. 450", "Rs. 0", "100% Digital via Bhoomi RTC"],
        ["Land & Crop Field Survey", "Rs. 650", "Rs. 250", "62% Cost Reduction / Geo-Photo"],
        ["Data Entry & Maker Appraisal", "Rs. 400", "Rs. 50", "Auto-Prefilled from APIs"],
        ["Branch Overhead & Storage", "Rs. 700", "Rs. 400", "Zero Paper Storage / Audit-Ready"],
        ["TOTAL COST PER APPLICATION", "Rs. 2,200", "Rs. 700", "Rs. 1,500 Saved per Loan (68%)"]
    ]
    cost_table = Table(cost_data, colWidths=[230, 160, 160, 210])
    cost_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 5), (-1, 5), c_orange_bg),
        ('FONTNAME', (0, 5), (-1, 5), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 5), (-1, 5), c_secondary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(cost_table)
    story.append(Spacer(1, 12))

    fin_notes = [
        [
            Paragraph("<b>SCALE ECONOMICS:</b> A commercial bank processing 2,00,000 KCC applications annually saves <b>Rs. 30.00 Crore in direct operating overhead</b> each year.<br/>"
                      "<b>COMMERCIAL MODEL:</b> 0.35% origination fee on disbursed credit (Zero upfront Capex for banks) + Rs. 35,000 annual branch SaaS license.", bold_body_style)
        ]
    ]
    fn_table = Table(fin_notes, colWidths=[760])
    fn_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_primary),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(fn_table)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 7: State Command Center & SLBC Dashboard
    # -------------------------------------------------------------
    story.append(Paragraph("State Command Center & Real-Time SLBC Oversight", slide_title_style))
    story.append(Paragraph("Empowering the SLBC Convener, RBI, NABARD, and State Leadership with live operational visibility.", body_style))
    story.append(Spacer(1, 15))

    cc_data = [
        [
            Paragraph("<b>EXECUTIVE DRILLDOWNS</b><br/><font size=7 color='#044E29'>District & Taluk Analytics</font>", card_header_style),
            Paragraph("<b>BANK PERFORMANCE SCORECARDS</b><br/><font size=7 color='#0284C7'>Branch Benchmarking</font>", card_header_style),
            Paragraph("<b>SLA ENFORCEMENT ENGINE</b><br/><font size=7 color='#EA580C'>Collector Auto-Escalation</font>", card_header_style)
        ],
        [
            Paragraph(
                "• Real-time heatmaps tracking credit velocity across all 31 districts & 240 taluks.<br/>"
                "• Compare disbursement pace against State Credit Plan targets.<br/>"
                "• Instant detection of regional credit gaps and underserved taluks.<br/>"
                "• 1-click export of SLBC review reports in standard PDF and Excel formats.",
                body_style
            ),
            Paragraph(
                "• Live scorecards comparing SBI, Canara Bank, KVGB, Karnataka Bank, and DCCBs.<br/>"
                "• Turnaround time (TAT) tracking identifying branches exceeding 7 days.<br/>"
                "• Rejection taxonomy analysis highlighting branches with abnormal rejection spikes.<br/>"
                "• Officer productivity and field verification volume benchmarking.",
                body_style
            ),
            Paragraph(
                "• Real-time countdown timer on every loan application.<br/>"
                "• Automated escalation to District Collectors when SLA is breached.<br/>"
                "• Integrated citizen grievance system resolving complaints under 10 days.<br/>"
                "• Full statutory audit trail preventing arbitrary rejections.",
                body_style
            )
        ]
    ]
    cc_table = Table(cc_data, colWidths=[250, 255, 255])
    cc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(cc_table)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 8: CyberKavach: Rural Cyber Defense
    # -------------------------------------------------------------
    story.append(Paragraph("CyberKavach: First-of-its-Kind Agrarian Cyber Defense", slide_title_style))
    story.append(Paragraph("Protecting farmers from rising predatory loan apps, SMS phishing, and WhatsApp OTP financial scams.", body_style))
    story.append(Spacer(1, 15))

    cyber_data = [
        [
            Paragraph("<b>CYBER THREAT VECTORS IN RURAL INDIA</b>", card_header_style),
            Paragraph("<b>CYBERKAVACH DEFENSIVE CAPABILITIES</b>", card_header_style)
        ],
        [
            Paragraph(
                "• <b>Fake PM-KISAN Links:</b> Phishing SMS messages luring farmers with fake bonus credits to capture Aadhaar and bank credentials.<br/>"
                "• <b>Predatory Loan APKs:</b> Unregistered instant loan apps charging extortionate fees and siphoning contact lists.<br/>"
                "• <b>OTP Social Engineering:</b> Fraudsters posing as bank branch managers asking for debit card and OTP details.<br/>"
                "• <b>Disbursement Draining:</b> Siphoning freshly disbursed KCC loan funds before the farmer can purchase farm inputs.",
                body_style
            ),
            Paragraph(
                "✔ <b>DigiKavach-Aligned Heuristics:</b> Real-time ML and regex detection of fraudulent URLs and scam syntax.<br/>"
                "✔ <b>Bilingual Scanner (Kannada & English):</b> Farmers paste suspicious messages into the app for instant threat analysis.<br/>"
                "✔ <b>Instant Plain-Language Warning:</b> 'ALERT: Do not share OTP. This link will siphon your bank funds.'<br/>"
                "✔ <b>Bank Account Shield:</b> Ensures disbursed agricultural credit stays protected within legitimate bank accounts.",
                bold_body_style
            )
        ]
    ]
    cyber_table = Table(cyber_data, colWidths=[375, 385])
    cyber_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(cyber_table)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 9: Security & DPDP Compliance
    # -------------------------------------------------------------
    story.append(Paragraph("Data Governance, Security & DPDP Act Compliance", slide_title_style))
    story.append(Paragraph("Strict compliance with Indian data privacy mandates, RBI master directions, and banking cybersecurity norms.", body_style))
    story.append(Spacer(1, 15))

    sec_data = [
        [
            Paragraph("<b>DPDP ACT 2023 COMPLIANCE</b>", card_header_style),
            Paragraph("<b>BANK-GRADE CYBERSECURITY</b>", card_header_style)
        ],
        [
            Paragraph(
                "• <b>Explicit Notice & Consent:</b> Farmer provides explicit digital consent prior to fetching Bhoomi or FRUITS records.<br/>"
                "• <b>Revocable Permissions:</b> Farmers can review and revoke consent records at any time via mobile.<br/>"
                "• <b>Audit Consent Trail:</b> Timestamped consent tokens logged with UIDAI / CeG provenance.<br/>"
                "• <b>Zero Data Monetization:</b> Strict prohibition on third-party commercial profiling.",
                body_style
            ),
            Paragraph(
                "• <b>Encryption Standards:</b> 256-bit TLS encryption in transit and AES-256 encryption at rest.<br/>"
                "• <b>CERT-In Empaneled Audit:</b> Platform primed for formal CERT-In vulnerability assessment.<br/>"
                "• <b>Role-Based Access Control (RBAC):</b> Separation of duties between Maker, Checker, and Admin.<br/>"
                "• <b>Sovereign Hosting:</b> 100% data residency within MeitY-empaneled Indian cloud data centers.",
                body_style
            )
        ]
    ]
    sec_table = Table(sec_data, colWidths=[375, 385])
    sec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(sec_table)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 10: Statewide Rollout Roadmap
    # -------------------------------------------------------------
    story.append(Paragraph("Statewide Rollout Roadmap & CBS Integration Plan", slide_title_style))
    story.append(Paragraph("A structured, phased progression from verified 10-district pilot to statewide Karnataka ubiquity.", body_style))
    story.append(Spacer(1, 15))

    road_data = [
        [
            Paragraph("<b>PHASE 1 (COMPLETED)</b><br/><font size=7 color='#044E29'>10 Pilot Districts (2026)</font>", card_header_style),
            Paragraph("<b>PHASE 2 (CURRENT)</b><br/><font size=7 color='#0284C7'>All 31 KA Districts (2027)</font>", card_header_style),
            Paragraph("<b>PHASE 3 (SCALE)</b><br/><font size=7 color='#0D9488'>Insurance & FPOs (2028-29)</font>", card_header_style),
            Paragraph("<b>PHASE 4 (NATIONAL)</b><br/><font size=7 color='#EA580C'>AgriStack Federation (2030+)</font>", card_header_style)
        ],
        [
            Paragraph(
                "• 10 Pilot districts live<br/>"
                "• Bhoomi/FRUITS sandboxes<br/>"
                "• 1,50,000 farmers registered<br/>"
                "• 1,05,000 KCC sanctions<br/>"
                "• Rs. 1,890 Cr credit flow<br/>"
                "• Zero ghost borrower cases",
                body_style
            ),
            Paragraph(
                "• Full rollout to 240+ taluks<br/>"
                "• CBS ISO-8583 push<br/>"
                "• Automated CIBIL pull<br/>"
                "• 5,00,000 active farmers<br/>"
                "• Rs. 6,750 Cr credit flow<br/>"
                "• 31 Collectorate desks",
                body_style
            ),
            Paragraph(
                "• PMFBY weather index claims<br/>"
                "• KSNDMC weather advisory<br/>"
                "• FPO group credit module<br/>"
                "• Input credit checkout APIs<br/>"
                "• Voice AI in local Kannada<br/>"
                "• 12,00,000 active farmers",
                body_style
            ),
            Paragraph(
                "• National AgriStack UFSP<br/>"
                "• Multi-state registry adaptors<br/>"
                "• e-NWR warehouse financing<br/>"
                "• 50,00,000 active farmers<br/>"
                "• Rs. 72,000 Cr credit flow<br/>"
                "• Sovereign DPI export",
                body_style
            )
        ]
    ]
    road_table = Table(road_data, colWidths=[190, 190, 190, 190])
    road_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(road_table)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 11: Proposed Resolutions for SLBC
    # -------------------------------------------------------------
    story.append(Paragraph("Proposed Resolutions for SLBC Plenary Approval", slide_title_style))
    story.append(Paragraph("Actionable resolutions submitted for consideration and adoption by the State Level Bankers' Committee.", body_style))
    story.append(Spacer(1, 15))

    res_data = [
        [
            Paragraph("<b>RESOLUTION 1: DIGITAL GATEWAY EMPANELMENT</b>", card_header_style),
            Paragraph("<b>RESOLUTION 2: CORE BANKING API CONNECTIVITY</b>", card_header_style)
        ],
        [
            Paragraph(
                "• Formal adoption of KisanKavach as the preferred digital lending orchestration gateway for KCC credit origination across Karnataka.<br/>"
                "• Recognition of digital Bhoomi RTC and FRUITS crop provenance as valid prefill for loan applications.<br/>"
                "• Standardizing the 7-day SLA countdown across all member bank branches.",
                body_style
            ),
            Paragraph(
                "• Authorize technical integration between KisanKavach and member bank CBS gateways (Finacle, BaNCS, Flexcube).<br/>"
                "• Enable automated digital lien registration / charge creation communication with Bhoomi.<br/>"
                "• Provide sandbox access for CIBIL / credit bureau real-time pull integration.",
                body_style
            )
        ],
        [
            Paragraph("<b>RESOLUTION 3: JOINT IMPLEMENTATION TASKFORCE</b>", card_header_style),
            Paragraph("<b>RESOLUTION 4: STATEWIDE EXPANSION MANDATE</b>", card_header_style)
        ],
        [
            Paragraph(
                "• Form a joint 5-member steering committee comprising:<br/>"
                "  - SLBC Convener Representative (Canara Bank)<br/>"
                "  - State Dept of Agriculture & Bhoomi Nodal Officers<br/>"
                "  - Lead District Managers (LDMs) of Pilot Districts<br/>"
                "  - Lead System Architect (Sarath Babu Rayaprolu)",
                body_style
            ),
            Paragraph(
                "• Approve statewide expansion across all 31 Karnataka districts.<br/>"
                "• Set target of onboarding 5,00,000 smallholder farmers in FY 2026-27.<br/>"
                "• Facilitate Rs. 6,750 Crore in prioritized agricultural credit through partner banks.<br/>"
                "• Mandate quarterly progress reviews at future SLBC plenary meetings.",
                body_style
            )
        ]
    ]
    res_table = Table(res_data, colWidths=[375, 385])
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(res_table)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 12: Conclusion & Q&A
    # -------------------------------------------------------------
    story.append(Spacer(1, 15))
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=70, height=82))
        story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Empowering Karnataka's Agrarian Economy</b>", concl_title_style))
    story.append(Paragraph("<b>Rapid, Transparent & Fraud-Free Digital Agricultural Credit</b>", concl_subtitle_style))
    story.append(Spacer(1, 10))

    concl_data = [
        [
            Paragraph("<b>Author & Presenter:</b>", bold_body_style),
            Paragraph("<b>Sarath Babu Rayaprolu</b> (Founder & Lead System Architect)", bold_body_style)
        ],
        [
            Paragraph("<b>Production Web Platform:</b>", bold_body_style),
            Paragraph("https://kisan.digikavach.net", body_style)
        ],
        [
            Paragraph("<b>Live Demonstration:</b>", bold_body_style),
            Paragraph("Bank Maker-Checker Portal & District Command Center", body_style)
        ],
        [
            Paragraph("<b>Mobile Application:</b>", bold_body_style),
            Paragraph("Native Android APK Ready for Field Demonstration", body_style)
        ],
        [
            Paragraph("<b>Operations & Head Office:</b>", bold_body_style),
            Paragraph("Bengaluru, Karnataka  |  Email: sarath@digikavach.net", body_style)
        ]
    ]
    concl_table = Table(concl_data, colWidths=[180, 560])
    concl_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(concl_table)

    doc.build(story, canvasmaker=NumberedCanvasLandscape)
    print(f"PDF Presentation saved successfully to: {pdf_path}")


if __name__ == "__main__":
    os.makedirs(PROJECT_DOCS_DIR, exist_ok=True)
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    pptx_path = os.path.join(PROJECT_DOCS_DIR, PPTX_FILENAME)
    pdf_path = os.path.join(PROJECT_DOCS_DIR, PDF_FILENAME)

    print("Generating SLBC PowerPoint presentation (.pptx)...")
    create_pptx_deck(pptx_path, LOGO_PATH)

    print("Generating SLBC Landscape PDF presentation (.pdf)...")
    create_pdf_deck(pdf_path, LOGO_PATH)

    print("Copying to artifacts and public directories...")
    for f in [PPTX_FILENAME, PDF_FILENAME]:
        src = os.path.join(PROJECT_DOCS_DIR, f)
        # Copy to public
        dst_pub = os.path.join(PUBLIC_DIR, f)
        with open(src, "rb") as s, open(dst_pub, "wb") as d:
            d.write(s.read())
        # Copy to artifacts
        dst_art = os.path.join(ARTIFACTS_DIR, f)
        with open(src, "rb") as s, open(dst_art, "wb") as d:
            d.write(s.read())
        print(f"Distributed {f} to public and artifacts directory.")

    print("\nALL SLBC ANCHOR PRESENTATION DELIVERABLES CREATED SUCCESSFULLY!")
