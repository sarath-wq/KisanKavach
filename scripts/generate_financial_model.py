import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_financial_model(output_path):
    wb = openpyxl.Workbook()
    
    # Styles
    font_family = "Segoe UI"
    title_font = Font(name=font_family, size=16, bold=True, color="FFFFFF")
    section_font = Font(name=font_family, size=12, bold=True, color="044E29")
    header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
    bold_font = Font(name=font_family, size=10, bold=True, color="1E293B")
    normal_font = Font(name=font_family, size=10, color="334155")
    italic_font = Font(name=font_family, size=9, italic=True, color="64748B")
    kpi_val_font = Font(name=font_family, size=14, bold=True, color="044E29")
    kpi_sub_font = Font(name=font_family, size=9, bold=True, color="475569")
    
    # Fills
    primary_fill = PatternFill(start_color="044E29", end_color="044E29", fill_type="solid") # Deep Forest Green
    secondary_fill = PatternFill(start_color="EA580C", end_color="EA580C", fill_type="solid") # Saffron Orange
    accent_fill = PatternFill(start_color="059669", end_color="059669", fill_type="solid") # Emerald Green
    light_green_fill = PatternFill(start_color="E8F5E9", end_color="E8F5E9", fill_type="solid")
    light_orange_fill = PatternFill(start_color="FFF7ED", end_color="FFF7ED", fill_type="solid")
    light_gray_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    total_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    card_fill = PatternFill(start_color="ECFDF5", end_color="ECFDF5", fill_type="solid")
    
    # Borders
    thin_border_side = Side(style='thin', color="CBD5E1")
    border_all = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    double_bottom_side = Side(style='double', color="044E29")
    total_border = Border(top=thin_border_side, bottom=double_bottom_side)
    
    # Alignments
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    # ==========================================
    # SHEET 1: EXECUTIVE SUMMARY & KPIS
    # ==========================================
    ws1 = wb.active
    ws1.title = "Executive Summary"
    ws1.views.sheetView[0].showGridLines = True
    
    # Title Block
    ws1.merge_cells("A1:G2")
    ws1["A1"] = "KISANKAVACH - STRATEGIC FINANCIAL MODEL & BUSINESS ROADMAP"
    ws1["A1"].font = title_font
    ws1["A1"].fill = primary_fill
    ws1["A1"].alignment = align_center
    
    ws1.merge_cells("A3:G3")
    ws1["A3"] = "Digital Public Infrastructure for Farmer Credit, Benefits, Insurance & Fraud Defense | Project Report by Sarath Babu Rayaprolu"
    ws1["A3"].font = Font(name=font_family, size=10, bold=True, color="EA580C")
    ws1["A3"].alignment = align_left
    
    # Author Credit Box
    ws1["A4"] = "DOCUMENT METADATA & CONTROL"
    ws1["A4"].font = section_font
    
    meta_info = [
        ["Project Name:", "KisanKavach Karnataka (National DPI Scale)", "Author / Lead:", "Sarath Babu Rayaprolu"],
        ["Target Geography:", "Karnataka (31 Districts) & Pan-India Scale", "Financial Horizon:", "5-Year Plan (2026 - 2031)"],
        ["Platform Domain:", "kisan.digikavach.net", "Classification:", "Confidential - Institutional Investor Memorandum"]
    ]
    for r_idx, row_m in enumerate(meta_info, 5):
        ws1.cell(row=r_idx, column=1, value=row_m[0]).font = bold_font
        ws1.cell(row=r_idx, column=1).border = border_all
        ws1.cell(row=r_idx, column=2, value=row_m[1]).font = normal_font
        ws1.cell(row=r_idx, column=2).border = border_all
        ws1.cell(row=r_idx, column=3, value=row_m[2]).font = bold_font
        ws1.cell(row=r_idx, column=3).border = border_all
        ws1.cell(row=r_idx, column=4, value=row_m[3]).font = Font(name=font_family, size=10, bold=True, color="044E29")
        ws1.cell(row=r_idx, column=4).border = border_all
    
    # KPI Highlights Cards
    kpis = [
        ("TOTAL ADDRESSABLE MARKET", "Rs. 20+ Lakh Cr", "140M Indian Farmers"),
        ("5-YR CUMULATIVE REVENUE", "Rs. 588.65 Cr", "Across 4 Streams"),
        ("5-YR NET CASH FLOW", "Rs. 275.40 Cr", "Positive from M9"),
        ("CUSTOMER ACQ. COST (CAC)", "Rs. 174.75 / Farmer", "Assisted & Digital"),
        ("LIFETIME VALUE (LTV)", "Rs. 3,115.80 / Farmer", "5-Year Retention"),
        ("LTV / CAC RATIO", "17.8x", "Superior Unit Econ.")
    ]
    
    ws1.row_dimensions[9].height = 20
    ws1.row_dimensions[10].height = 24
    ws1.row_dimensions[11].height = 18
    
    for idx, (title, val, sub) in enumerate(kpis):
        col = get_column_letter(idx + 2)
        ws1[f"{col}9"] = title
        ws1[f"{col}9"].font = Font(name=font_family, size=8, bold=True, color="64748B")
        ws1[f"{col}9"].alignment = align_center
        ws1[f"{col}9"].fill = light_gray_fill
        ws1[f"{col}9"].border = border_all
        
        ws1[f"{col}10"] = val
        ws1[f"{col}10"].font = kpi_val_font
        ws1[f"{col}10"].alignment = align_center
        ws1[f"{col}10"].fill = card_fill
        ws1[f"{col}10"].border = border_all
        
        ws1[f"{col}11"] = sub
        ws1[f"{col}11"].font = kpi_sub_font
        ws1[f"{col}11"].alignment = align_center
        ws1[f"{col}11"].fill = card_fill
        ws1[f"{col}11"].border = border_all

    # Executive Overview Table
    ws1["A13"] = "KEY FINANCIAL & OPERATIONAL TRAJECTORY (AUTHORED BY SARATH BABU RAYAPROLU)"
    ws1["A13"].font = section_font
    
    summary_headers = ["Metric / Indicator", "Year 1 (Pilot)", "Year 2 (Karnataka)", "Year 3 (Scale)", "Year 4 (Regional)", "Year 5 (National)", "CAGR / Benchmark"]
    for col_num, h_text in enumerate(summary_headers, 1):
        cell = ws1.cell(row=14, column=col_num)
        cell.value = h_text
        cell.font = header_font
        cell.fill = primary_fill
        cell.alignment = align_center
        cell.border = border_all
    
    summary_data = [
        ["Active Registered Farmers", "1,50,000", "5,00,000", "12,00,000", "25,00,000", "50,00,000", "140.2%"],
        ["KCC Loan Applications Processed", "1,05,000", "3,75,000", "9,20,000", "19,50,000", "40,00,000", "147.8%"],
        ["Total Credit Facilitated (Rs. Cr)", "Rs. 1,890 Cr", "Rs. 6,750 Cr", "Rs. 16,560 Cr", "Rs. 35,100 Cr", "Rs. 72,000 Cr", "148.0%"],
        ["Participating Bank Branches", "350", "1,850", "4,200", "8,500", "16,000", "160.3%"],
        ["Gross Revenue (Rs. Cr)", "Rs. 8.45 Cr", "Rs. 28.20 Cr", "Rs. 71.50 Cr", "Rs. 156.00 Cr", "Rs. 324.50 Cr", "148.8%"],
        ["Operating Expenses (OpEx) (Rs. Cr)", "Rs. 6.10 Cr", "Rs. 13.80 Cr", "Rs. 26.50 Cr", "Rs. 52.00 Cr", "Rs. 97.50 Cr", "99.8%"],
        ["EBITDA (Rs. Cr)", "Rs. 2.35 Cr", "Rs. 14.40 Cr", "Rs. 45.00 Cr", "Rs. 104.00 Cr", "Rs. 227.00 Cr", "213.6%"],
        ["EBITDA Margin (%)", "27.8%", "51.1%", "62.9%", "66.7%", "70.0%", "+42.2 pts"],
        ["Net Cash Flow (Rs. Cr)", "Rs. 1.45 Cr", "Rs. 9.85 Cr", "Rs. 31.50 Cr", "Rs. 73.60 Cr", "Rs. 159.00 Cr", "224.2%"],
        ["Break-Even Month", "Month 9", "Profitable", "High Yield", "Expansion", "Dominant", "Achieved M9"],
        ["Turnaround Time (SLA)", "< 7 Days", "< 5 Days", "< 4 Days", "< 3 Days", "< 48 Hours", "85% TAT Drop"]
    ]
    
    for row_idx, row_vals in enumerate(summary_data, 15):
        for col_idx, val in enumerate(row_vals, 1):
            cell = ws1.cell(row=row_idx, column=col_idx)
            cell.value = val
            cell.font = bold_font if (col_idx == 1 or "EBITDA" in str(row_vals[0]) or "Gross Revenue" in str(row_vals[0])) else normal_font
            cell.alignment = align_left if col_idx == 1 else align_center
            cell.border = border_all
            if "EBITDA" in str(row_vals[0]) or "Gross Revenue" in str(row_vals[0]):
                cell.fill = light_green_fill

    # ==========================================
    # SHEET 2: STRATEGIC ROADMAP
    # ==========================================
    ws2 = wb.create_sheet(title="Strategic Roadmap")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2.merge_cells("A1:G2")
    ws2["A1"] = "KISANKAVACH 5-YEAR STRATEGIC ROADMAP (2026 - 2031)"
    ws2["A1"].font = title_font
    ws2["A1"].fill = primary_fill
    ws2["A1"].alignment = align_center
    
    ws2["A3"] = "Prepared by Sarath Babu Rayaprolu | Technology, Operations & Scaling Milestones"
    ws2["A3"].font = italic_font
    
    roadmap_headers = ["Phase", "Timeline", "Geographic Scope", "Strategic Objectives", "Technology & DPI Milestones", "Key Commercial Deliverables", "Target Farmers"]
    for col_num, h_text in enumerate(roadmap_headers, 1):
        cell = ws2.cell(row=4, column=col_num)
        cell.value = h_text
        cell.font = header_font
        cell.fill = secondary_fill
        cell.alignment = align_center
        cell.border = border_all
        
    roadmap_data = [
        ["Phase 1: Pilot & Sandbox Hardening", "Months 1 - 6 (Q3-Q4 2026)", "10 Karnataka Districts (Mysuru, Mandya, Hassan, Belagavi, etc.)", 
         "Validate DPI consent architecture, establish SLA compliance baseline, achieve banking partner buy-in", 
         "FRUITS & Bhoomi live API connectors, Next.js 15 PWA, Capacitor Android build, 9-step KCC wizard, CyberKavach ML scanner", 
         "6 Bank integrations (SBI, Canara, KVGB, Karnataka Bank, Apex), Rs. 250 Cr pilot credit, State Command Center live", "1,50,000"],
         
        ["Phase 2: Statewide Karnataka Rollout", "Months 7 - 18 (2027)", "All 31 Karnataka Districts & 240+ Taluks", 
         "Full scale across commercial & RRB branches, automated payment gateway integration, grievance escalation enforcement", 
         "UPI/Razorpay/PhonePe payment gateway, automated CIBIL/Experian credit pull, automated maker-checker CBS ISO-8583 adapter", 
         "Onboarding 22 commercial & cooperative banks, 1,850 branches, Rs. 6,750 Cr KCC volume, District Collector portals live", "5,00,000"],
         
        ["Phase 3: Deep Value-Chain & Insurance", "Months 19 - 36 (2028-2029)", "Karnataka Statewide + Border Districts of AP, MH, TN", 
         "Satellite crop insurance settlement (PMFBY), FPO collective lending, farmer soil & weather micro-advisories", 
         "KSNDMC satellite weather index claim trigger, FPO multi-member loan origination engine, Kannada/Telugu voice AI agent", 
         "PMFBY insurer consortium APIs, agri-input marketplace credit linkages, 4,200 branches, Rs. 16,560 Cr credit", "12,00,000"],
         
        ["Phase 4: National DPI & AgriStack Scale", "Months 37 - 60 (2029-2031)", "Pan-India (Karnataka, Telangana, AP, Maharashtra, MP, Punjab)", 
         "Position KisanKavach as India's premier Agri-Credit & Farmer Protection Operating System aligned with AgriStack / UFSP", 
         "AgriStack native adapter, multi-state land registry APIs (Meebhoomi, Dharani, Mahabhumi), pledge warehouse financing", 
         "16,000 bank branches, Rs. 72,000 Cr annual credit throughput, sovereign DPI export readiness, pre-IPO readiness", "50,00,000"]
    ]
    
    for row_idx, row_vals in enumerate(roadmap_data, 5):
        ws2.row_dimensions[row_idx].height = 45
        for col_idx, val in enumerate(row_vals, 1):
            cell = ws2.cell(row=row_idx, column=col_idx)
            cell.value = val
            cell.font = bold_font if col_idx in [1, 2, 7] else normal_font
            cell.alignment = align_center if col_idx in [1, 2, 7] else Alignment(horizontal="left", vertical="center", wrap_text=True)
            cell.border = border_all
            if col_idx == 1:
                cell.fill = light_green_fill
            elif col_idx == 7:
                cell.fill = light_orange_fill

    # ==========================================
    # SHEET 3: TARGET CUSTOMERS & WHY THEY NEED IT
    # ==========================================
    ws3 = wb.create_sheet(title="Target Customers & Value")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3.merge_cells("A1:F2")
    ws3["A1"] = "TARGET CUSTOMER PERSONAS, PAIN POINTS & VALUE PROPOSITIONS"
    ws3["A1"].font = title_font
    ws3["A1"].fill = primary_fill
    ws3["A1"].alignment = align_center
    
    ws3["A3"] = "Prepared by Sarath Babu Rayaprolu | Multi-Stakeholder Value Creation Model"
    ws3["A3"].font = italic_font
    
    ws3["A4"] = "MARKET SEGMENTATION & ADOPTION DRIVERS"
    ws3["A4"].font = section_font
    
    cust_headers = ["Customer Segment", "Target Entities / Personas", "Current Critical Pain Points", "KisanKavach Transformational Solution", "Quantified Value / Economic Benefit", "Willingness to Pay / Revenue Model"]
    for col_num, h_text in enumerate(cust_headers, 1):
        cell = ws3.cell(row=5, column=col_num)
        cell.value = h_text
        cell.font = header_font
        cell.fill = primary_fill
        cell.alignment = align_center
        cell.border = border_all
        
    cust_data = [
        ["Lending Institutions (Commercial & Cooperative Banks)", "SBI, Canara, Karnataka Bank, KVGB, Apex Bank, DCCBs, RRBs", 
         "• 30-45 day KCC approval cycle\n• High operational cost (Rs. 2,200/file)\n• 38% rejection rate due to Bhoomi errors\n• Ghost borrowers & fake land claims\n• Strict RBI PSL quota pressure",
         "• Real-time automated land verification via Bhoomi\n• FRUITS crop declaration provenance\n• Standardized Maker-Checker digital LOS\n• Structured rejection reason taxonomy\n• Automated SLA countdown & reminders",
         "• Turnaround reduced from 35 to < 7 days\n• 70% reduction in origination cost\n• 0% ghost-borrower fraud risk\n• 100% RBI PSL compliance assurance",
         "0.35% - 0.50% loan origination fee per sanctioned KCC + Rs. 35,000/yr SaaS branch fee"],
         
        ["State Government (Institutional Anchor)", "Karnataka Dept of Agriculture, Dept of Cooperation, District Collectors", 
         "• Blind spots in credit delivery\n• Escalating farmer grievances & protests\n• Subsidized credit leakages\n• Lack of taluk/branch performance data\n• Cyber financial scams targeting farmers",
         "• Statewide Command Center dashboard\n• District & Taluk drilldown metrics\n• Real-time bank processing velocity tracking\n• Auto-escalating grievance resolution system\n• CyberKavach anti-fraud alert engine",
         "• 80% reduction in grievance turnaround\n• Zero subsidy diversion\n• Real-time data for state policy & planning\n• Protection of state agrarian wealth",
         "Rs. 3.5 - Rs. 5.0 Cr annual state DPI maintenance & SLA oversight SaaS contract"],
         
        ["Crop & General Insurance Companies", "AIC (Agriculture Insurance Co), PMFBY empanelled insurers, ICICI Lombard", 
         "• High false claims & disputed crop losses\n• Delayed claim settlements (6-12 months)\n• Disconnect with actual farmer land surveys\n• Friction in farmer premium collection",
         "• Direct integration with Bhoomi survey RTC\n• KSNDMC hyper-local weather risk alerts\n• One-click digital premium settlement\n• Verified farmer Aadhaar-linked payout",
         "• 40% reduction in disputed claims\n• Automated index triggers cut settlement delay\n• High customer trust & retention",
         "0.5% premium collection fee + Rs. 50 per verified claim processing fee"],
         
        ["Farmers (Core Beneficiaries)", "Small & Marginal Farmers, Commercial Planters, Women Farmers", 
         "• Trapped by loan sharks (24-36% interest)\n• Multiple visits to bank & taluk offices (Rs. 3,000+ travel/agent loss)\n• Low digital literacy & English barriers\n• Preyed upon by SMS/WhatsApp loan scams",
         "• 100% paperless 9-step guided KCC wizard\n• Bilingual interface (Kannada & English)\n• Plain language 'Do you need to do anything?'\n• CyberKavach fraud detection scanner\n• Direct voice AI assistant for queries",
         "• Saves Rs. 3,500+ in paperwork & travel\n• Access to 4% subsidized KCC credit\n• Dignified, transparent digital lending\n• Total protection against digital financial fraud",
         "Free for basic KCC & benefits | Rs. 50 - Rs. 100 nominal fee for assisted CSC filings or premium advisory"]
    ]
    
    for row_idx, row_vals in enumerate(cust_data, 6):
        ws3.row_dimensions[row_idx].height = 65
        for col_idx, val in enumerate(row_vals, 1):
            cell = ws3.cell(row=row_idx, column=col_idx)
            cell.value = val
            cell.font = bold_font if col_idx == 1 else normal_font
            cell.alignment = align_left if col_idx in [2, 3, 4, 6] else Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = border_all
            if col_idx == 1:
                cell.fill = light_green_fill

    # ==========================================
    # SHEET 4: UNIT ECONOMICS (CAC & LTV)
    # ==========================================
    ws4 = wb.create_sheet(title="Unit Economics (CAC & LTV)")
    ws4.views.sheetView[0].showGridLines = True
    
    ws4.merge_cells("A1:G2")
    ws4["A1"] = "UNIT ECONOMICS: CUSTOMER ACQUISITION COST (CAC) & LIFETIME VALUE (LTV)"
    ws4["A1"].font = title_font
    ws4["A1"].fill = primary_fill
    ws4["A1"].alignment = align_center
    
    ws4["A3"] = "Prepared by Sarath Babu Rayaprolu | Unit Margin & Retention Economics"
    ws4["A3"].font = italic_font
    
    # Farmer CAC Table
    ws4["A4"] = "1. BLENDED FARMER CAC BREAKDOWN (PER ONBOARDED FARMER)"
    ws4["A4"].font = section_font
    
    cac_headers = ["Cost Component", "Assisted Mode (CSC / Grama One)", "Self-Service Mobile PWA", "Blended Channel Weight", "Blended Cost (Rs.)", "Notes / Efficiency Lever"]
    for col_num, h_text in enumerate(cac_headers, 1):
        cell = ws4.cell(row=5, column=col_num)
        cell.value = h_text
        cell.font = header_font
        cell.fill = primary_fill
        cell.alignment = align_center
        cell.border = border_all
        
    cac_data = [
        ["Field Agent / CSC Operator Incentive", "Rs. 120.00", "Rs. 0.00", "65% Assisted / 35% Mobile", "Rs. 78.00", "Paid only on verified document submission"],
        ["Local Awareness, FPO & Agri-Fair Drives", "Rs. 45.00", "Rs. 30.00", "Direct Rural Engagement", "Rs. 39.75", "Leverages APMC mandis & milk cooperatives"],
        ["Digital Marketing & WhatsApp Campaigns", "Rs. 10.00", "Rs. 40.00", "Targeted Farmer Outreach", "Rs. 20.50", "High virality via farmer community groups"],
        ["Telecom OTP / SMS / WhatsApp Notification", "Rs. 8.00", "Rs. 8.00", "100% of Users", "Rs. 8.00", "Government DLT wholesale SMS pricing"],
        ["Onboarding Verification & Fraud Check", "Rs. 12.00", "Rs. 12.00", "KYC & Bhoomi query cost", "Rs. 12.00", "State API gateway subsidised access"],
        ["Customer Helpline & AI Voice Desk", "Rs. 20.00", "Rs. 10.00", "Helpline & Voice Bot", "Rs. 16.50", "AI Voice bot handles 70% of inbound queries"],
        ["TOTAL BLENDED CAC PER FARMER", "Rs. 215.00", "Rs. 100.00", "Weighted Average", "Rs. 174.75", "Expected to drop to Rs. 120 by Year 3"]
    ]
    
    for row_idx, row_vals in enumerate(cac_data, 6):
        for col_idx, val in enumerate(row_vals, 1):
            cell = ws4.cell(row=row_idx, column=col_idx)
            cell.value = val
            cell.font = bold_font if row_idx == 12 else normal_font
            cell.alignment = align_left if col_idx in [1, 6] else align_center
            cell.border = total_border if row_idx == 12 else border_all
            if row_idx == 12:
                cell.fill = light_orange_fill

    # Farmer LTV Table
    ws4["A14"] = "2. FARMER 5-YEAR LIFETIME VALUE (LTV) PROJECTION"
    ws4["A14"].font = section_font
    
    ltv_headers = ["Revenue Stream per Farmer", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "5-Year Cumulative", "Gross Margin %", "Cumulative Gross Margin"]
    for col_num, h_text in enumerate(ltv_headers, 1):
        cell = ws4.cell(row=15, column=col_num)
        cell.value = h_text
        cell.font = header_font
        cell.fill = secondary_fill
        cell.alignment = align_center
        cell.border = border_all
        
    ltv_data = [
        ["Bank KCC Origination & Processing Fee", "Rs. 720.00", "Rs. 750.00", "Rs. 800.00", "Rs. 850.00", "Rs. 900.00", "Rs. 4,020.00", "88%", "Rs. 3,537.60"],
        ["PMFBY Crop Insurance Processing Share", "Rs. 60.00", "Rs. 70.00", "Rs. 80.00", "Rs. 90.00", "Rs. 100.00", "Rs. 400.00", "80%", "Rs. 320.00"],
        ["Direct Benefit Transfer (DBT) Service", "Rs. 25.00", "Rs. 30.00", "Rs. 35.00", "Rs. 40.00", "Rs. 45.00", "Rs. 175.00", "75%", "Rs. 131.25"],
        ["Agri-Input Credit & Ecosystem Linkage", "Rs. 0.00", "Rs. 50.00", "Rs. 120.00", "Rs. 180.00", "Rs. 250.00", "Rs. 600.00", "70%", "Rs. 420.00"],
        ["TOTAL REVENUE PER FARMER", "Rs. 805.00", "Rs. 900.00", "Rs. 1,035.00", "Rs. 1,160.00", "Rs. 1,295.00", "Rs. 5,195.00", "84.9%", "Rs. 4,408.85"],
        ["Discounted LTV (12% Cost of Capital)", "-", "-", "-", "-", "-", "Rs. 3,670.00", "-", "Rs. 3,115.80"]
    ]
    
    for row_idx, row_vals in enumerate(ltv_data, 16):
        for col_idx, val in enumerate(row_vals, 1):
            cell = ws4.cell(row=row_idx, column=col_idx)
            cell.value = val
            cell.font = bold_font if row_idx in [20, 21] else normal_font
            cell.alignment = align_left if col_idx == 1 else align_center
            cell.border = total_border if row_idx in [20, 21] else border_all
            if row_idx in [20, 21]:
                cell.fill = light_green_fill

    # Key Ratios
    ws4["A23"] = "3. CRITICAL UNIT METRICS & BENCHMARKS"
    ws4["A23"].font = section_font
    
    ratios = [
        ["Blended Customer Acquisition Cost (CAC)", "Rs. 174.75"],
        ["Discounted 5-Year LTV (Net Contribution)", "Rs. 3,115.80"],
        ["LTV / CAC Ratio", "17.8x (SaaS benchmark: >3.0x is great, >10x is world-class)"],
        ["CAC Payback Period", "2.6 Months (Payback achieved on first KCC loan origination)"],
        ["Annual Farmer Retention Rate", "91.5% (High stickiness due to recurring annual KCC cycle)"],
        ["Bank Branch CAC / Annual License", "Rs. 22,500 CAC vs Rs. 35,000 Annual Branch License (Payback 7.7 Months)"]
    ]
    for r_idx, (m_label, m_val) in enumerate(ratios, 24):
        ws4.cell(row=r_idx, column=1).value = m_label
        ws4.cell(row=r_idx, column=1).font = bold_font
        ws4.cell(row=r_idx, column=1).border = border_all
        ws4.merge_cells(start_row=r_idx, start_column=2, end_row=r_idx, end_column=4)
        m_cell = ws4.cell(row=r_idx, column=2)
        m_cell.value = m_val
        m_cell.font = Font(name=font_family, size=10, bold=True, color="044E29" if "Ratio" in m_label or "Payback" in m_label else "1E293B")
        m_cell.alignment = align_left
        m_cell.fill = card_fill if "Ratio" in m_label else light_gray_fill
        m_cell.border = border_all

    # ==========================================
    # SHEET 5: 5-YEAR CASH FLOW MODEL
    # ==========================================
    ws5 = wb.create_sheet(title="5-Year Cashflow Model")
    ws5.views.sheetView[0].showGridLines = True
    
    ws5.merge_cells("A1:G2")
    ws5["A1"] = "KISANKAVACH 5-YEAR STATEMENT OF CASH FLOWS & P&L (RS. IN CRORES)"
    ws5["A1"].font = title_font
    ws5["A1"].fill = primary_fill
    ws5["A1"].alignment = align_center
    
    ws5["A3"] = "Prepared by Sarath Babu Rayaprolu | Complete Institutional Pro-Forma Model"
    ws5["A3"].font = italic_font
    
    cf_headers = ["P&L / Cash Flow Line Item", "Year 1 (2026-27)", "Year 2 (2027-28)", "Year 3 (2028-29)", "Year 4 (2029-30)", "Year 5 (2030-31)", "5-Year Total"]
    for col_num, h_text in enumerate(cf_headers, 1):
        cell = ws5.cell(row=4, column=col_num)
        cell.value = h_text
        cell.font = header_font
        cell.fill = primary_fill
        cell.alignment = align_center
        cell.border = border_all
        
    cf_data = [
        # OPERATING DRIVERS
        ["--- OPERATIONAL SCALE DRIVERS ---", "", "", "", "", "", ""],
        ["Registered Farmers on Platform (Active)", "1,50,000", "5,00,000", "12,00,000", "25,00,000", "50,00,000", "50,00,000"],
        ["KCC Loan Applications Processed", "1,05,000", "3,75,000", "9,20,000", "19,50,000", "40,00,000", "73,50,000"],
        ["Active Participating Bank Branches", "350", "1,850", "4,200", "8,500", "16,000", "16,000"],
        ["Total Credit Facilitated (Rs. Cr)", "Rs. 1,890.00", "Rs. 6,750.00", "Rs. 16,560.00", "Rs. 35,100.00", "Rs. 72,000.00", "Rs. 1,32,300.00"],
        
        # REVENUES
        ["--- REVENUE STREAMS (RS. CR) ---", "", "", "", "", "", ""],
        ["1. Bank Loan Origination Fees (0.35%-0.45%)", "Rs. 5.75", "Rs. 20.25", "Rs. 51.75", "Rs. 117.00", "Rs. 252.00", "Rs. 446.75"],
        ["2. Bank Branch SaaS License Fees", "Rs. 1.20", "Rs. 4.65", "Rs. 10.50", "Rs. 21.25", "Rs. 40.00", "Rs. 77.60"],
        ["3. Crop Insurance & Benefit Processing", "Rs. 0.60", "Rs. 2.25", "Rs. 5.50", "Rs. 11.75", "Rs. 24.00", "Rs. 44.10"],
        ["4. Govt Command Center & DPI SLA Support", "Rs. 0.90", "Rs. 1.05", "Rs. 3.75", "Rs. 6.00", "Rs. 8.50", "Rs. 20.20"],
        ["GROSS OPERATING REVENUE", "Rs. 8.45", "Rs. 28.20", "Rs. 71.50", "Rs. 156.00", "Rs. 324.50", "Rs. 588.65"],
        
        # OPERATING EXPENSES
        ["--- OPERATING EXPENDITURE (OpEx) ---", "", "", "", "", "", ""],
        ["Technology Infrastructure & Cloud Hosting (Supabase/Vercel/AWS)", "Rs. 0.65", "Rs. 1.40", "Rs. 2.80", "Rs. 5.50", "Rs. 10.20", "Rs. 20.55"],
        ["Engineering, AI & Product Development Team", "Rs. 1.80", "Rs. 3.20", "Rs. 5.40", "Rs. 9.50", "Rs. 16.00", "Rs. 35.90"],
        ["Field Operations, CSC Onboarding & Support Desk", "Rs. 1.50", "Rs. 3.80", "Rs. 7.20", "Rs. 14.00", "Rs. 26.50", "Rs. 53.00"],
        ["Sales, Banking Integrations & Regional Liaison", "Rs. 1.10", "Rs. 2.50", "Rs. 4.80", "Rs. 9.20", "Rs. 18.00", "Rs. 35.60"],
        ["Security Audits, Compliance & Legal Regulatory", "Rs. 0.45", "Rs. 0.85", "Rs. 1.60", "Rs. 2.80", "Rs. 5.00", "Rs. 10.70"],
        ["General Administrative & Corporate Overhead", "Rs. 0.60", "Rs. 2.05", "Rs. 4.70", "Rs. 11.00", "Rs. 21.80", "Rs. 40.15"],
        ["TOTAL OPERATING EXPENDITURE (OpEx)", "Rs. 6.10", "Rs. 13.80", "Rs. 26.50", "Rs. 52.00", "Rs. 97.50", "Rs. 195.90"],
        
        # EBITDA & NET EARNINGS
        ["EBITDA (OPERATING PROFIT)", "Rs. 2.35", "Rs. 14.40", "Rs. 45.00", "Rs. 104.00", "Rs. 227.00", "Rs. 392.75"],
        ["EBITDA Margin (%)", "27.8%", "51.1%", "62.9%", "66.7%", "70.0%", "66.7%"],
        ["Depreciation & Amortization (D&A)", "Rs. 0.35", "Rs. 0.65", "Rs. 1.20", "Rs. 2.40", "Rs. 4.50", "Rs. 9.10"],
        ["EBIT (Operating Income)", "Rs. 2.00", "Rs. 13.75", "Rs. 43.80", "Rs. 101.60", "Rs. 222.50", "Rs. 383.65"],
        ["Income Tax Expense (25%)", "Rs. 0.41", "Rs. 3.44", "Rs. 10.95", "Rs. 25.40", "Rs. 55.63", "Rs. 95.83"],
        ["NET INCOME (PAT)", "Rs. 1.59", "Rs. 10.31", "Rs. 32.85", "Rs. 76.20", "Rs. 166.87", "Rs. 287.82"],
        
        # CASH FLOW RECONCILIATION
        ["--- CASH FLOW MOVEMENTS ---", "", "", "", "", "", ""],
        ["Cash Generated from Operations", "Rs. 2.05", "Rs. 11.25", "Rs. 34.80", "Rs. 80.20", "Rs. 172.50", "Rs. 300.80"],
        ["Capital Expenditure (CapEx - IT/Security/Mobile)", "(Rs. 0.60)", "(Rs. 1.40)", "(Rs. 3.30)", "(Rs. 6.60)", "(Rs. 13.50)", "(Rs. 25.40)"],
        ["FREE CASH FLOW TO FIRM (FCFF)", "Rs. 1.45", "Rs. 9.85", "Rs. 31.50", "Rs. 73.60", "Rs. 159.00", "Rs. 275.40"],
        ["Opening Cash Balance", "Rs. 5.00", "Rs. 6.45", "Rs. 16.30", "Rs. 47.80", "Rs. 121.40", "Rs. 5.00"],
        ["CLOSING CASH BALANCE", "Rs. 6.45", "Rs. 16.30", "Rs. 47.80", "Rs. 121.40", "Rs. 280.40", "Rs. 280.40"]
    ]
    
    for row_idx, row_vals in enumerate(cf_data, 5):
        is_subhead = "---" in row_vals[0]
        is_total = any(k in row_vals[0] for k in ["GROSS OPERATING REVENUE", "TOTAL OPERATING EXPENDITURE", "EBITDA", "NET INCOME", "FREE CASH FLOW", "CLOSING CASH"])
        for col_idx, val in enumerate(row_vals, 1):
            cell = ws5.cell(row=row_idx, column=col_idx)
            cell.value = val
            cell.font = bold_font if (is_subhead or is_total or col_idx == 1) else normal_font
            cell.alignment = align_left if col_idx == 1 else align_center
            if is_subhead:
                cell.fill = light_gray_fill
                cell.font = Font(name=font_family, size=9, bold=True, color="044E29")
            elif is_total:
                cell.border = total_border
                cell.fill = light_green_fill if "EBITDA" in row_vals[0] or "REVENUE" in row_vals[0] or "FREE CASH" in row_vals[0] or "CLOSING" in row_vals[0] else light_orange_fill
            else:
                cell.border = border_all

    # ==========================================
    # SHEET 6: BREAK-EVEN & SENSITIVITY
    # ==========================================
    ws6 = wb.create_sheet(title="Break-Even & Sensitivity")
    ws6.views.sheetView[0].showGridLines = True
    
    ws6.merge_cells("A1:F2")
    ws6["A1"] = "BREAK-EVEN ANALYSIS & SENSITIVITY MATRIX"
    ws6["A1"].font = title_font
    ws6["A1"].fill = primary_fill
    ws6["A1"].alignment = align_center
    
    ws6["A3"] = "Prepared by Sarath Babu Rayaprolu | Cost Structure & Downside Buffer Analysis"
    ws6["A3"].font = italic_font
    
    ws6["A4"] = "1. YEAR 1 BREAK-EVEN ECONOMICS"
    ws6["A4"].font = section_font
    
    be_items = [
        ["Annual Fixed Overhead (Tech, Core Team, Legal, Admin)", "Rs. 3,80,00,000", "Baseline fixed commitment for platform operations"],
        ["Average Sanctioned KCC Loan Ticket Size", "Rs. 1,80,000", "Karnataka pilot average KCC limit"],
        ["Average Origination Fee per Loan (0.35% + SaaS Allocation)", "Rs. 720.00", "Realized revenue per sanctioned application"],
        ["Variable Cost per Application (Verification, SMS, Support)", "Rs. 170.00", "Direct incremental delivery cost"],
        ["Net Contribution Margin per Loan Application", "Rs. 550.00", "Unit margin available to cover fixed costs"],
        ["Contribution Margin Ratio", "76.4%", "World-class digital infrastructure margin"],
        ["ANNUAL BREAK-EVEN VOLUME (APPLICATIONS)", "69,090 Units", "Formula: Fixed Costs / Contribution Margin"],
        ["ANNUAL BREAK-EVEN DISBURSED LOAN VOLUME", "Rs. 1,243.60 Cr", "Total farm credit required to reach break-even"],
        ["PROJECTED YEAR 1 ACTUAL SANCTIONS", "1,05,000 Units", "152% of Break-Even volume target"],
        ["ESTIMATED BREAK-EVEN MONTH", "Month 9 (Q3 2026)", "Platform transitions into sustainable net cash generation"]
    ]
    
    for r_idx, (label, val, note) in enumerate(be_items, 5):
        cell_l = ws6.cell(row=r_idx, column=1, value=label)
        cell_v = ws6.cell(row=r_idx, column=2, value=val)
        cell_n = ws6.cell(row=r_idx, column=3, value=note)
        
        is_highlight = "BREAK-EVEN" in label or "MONTH" in label
        cell_l.font = bold_font if is_highlight else normal_font
        cell_v.font = kpi_val_font if is_highlight else bold_font
        cell_n.font = italic_font
        
        cell_l.border = border_all
        cell_v.border = border_all
        cell_n.border = border_all
        
        if is_highlight:
            cell_l.fill = light_orange_fill
            cell_v.fill = light_orange_fill

    # Sensitivity Grid
    ws6["A17"] = "2. SENSITIVITY MATRIX: YEAR 1 EBITDA (RS. CR) VS ORIGINATION FEE & CONVERSION RATE"
    ws6["A17"].font = section_font
    
    sens_headers = ["Loan Sanction Conversion Rate", "Fee: 0.25% (Rs. 450)", "Fee: 0.35% (Rs. 630)", "Fee: 0.45% (Rs. 810)", "Fee: 0.55% (Rs. 990)"]
    for c_num, s_text in enumerate(sens_headers, 1):
        cell = ws6.cell(row=18, column=c_num)
        cell.value = s_text
        cell.font = header_font
        cell.fill = secondary_fill
        cell.alignment = align_center
        cell.border = border_all
        
    sens_matrix = [
        ["Conservative (50% Sanction / 75,000 Loans)", "Rs. 0.25 Cr", "Rs. 1.60 Cr", "Rs. 2.95 Cr", "Rs. 4.30 Cr"],
        ["Base Case (70% Sanction / 1,05,000 Loans)", "Rs. 1.15 Cr", "Rs. 2.35 Cr (Base)", "Rs. 4.90 Cr", "Rs. 6.80 Cr"],
        ["Aggressive (85% Sanction / 1,27,500 Loans)", "Rs. 1.85 Cr", "Rs. 4.15 Cr", "Rs. 6.45 Cr", "Rs. 8.75 Cr"],
        ["Optimistic (92% Sanction / 1,38,000 Loans)", "Rs. 2.20 Cr", "Rs. 4.95 Cr", "Rs. 7.45 Cr", "Rs. 9.95 Cr"]
    ]
    
    for r_idx, r_vals in enumerate(sens_matrix, 19):
        for c_idx, val in enumerate(r_vals, 1):
            cell = ws6.cell(row=r_idx, column=c_idx)
            cell.value = val
            cell.font = bold_font if (c_idx == 1 or "Base" in val) else normal_font
            cell.alignment = align_left if c_idx == 1 else align_center
            cell.border = border_all
            if "Base" in val:
                cell.fill = light_green_fill
            elif c_idx > 1:
                cell.fill = light_gray_fill

    # ==========================================
    # SHEET 7: STAKEHOLDER & INVESTOR ROI
    # ==========================================
    ws7 = wb.create_sheet(title="Stakeholder & Investor ROI")
    ws7.views.sheetView[0].showGridLines = True
    
    ws7.merge_cells("A1:F2")
    ws7["A1"] = "RETURN ON INVESTMENT (ROI) & SYSTEMIC ECONOMIC SURPLUS"
    ws7["A1"].font = title_font
    ws7["A1"].fill = primary_fill
    ws7["A1"].alignment = align_center
    
    ws7["A3"] = "Prepared by Sarath Babu Rayaprolu | Valuation, Returns & Systemic Impact Model"
    ws7["A3"].font = italic_font
    
    # Investor ROI
    ws7["A4"] = "1. VENTURE CAPITAL & EQUITY INVESTOR RETURNS"
    ws7["A4"].font = section_font
    
    inv_headers = ["Investment Parameter", "Baseline Metrics", "Assumptions / Valuation Basis"]
    for c_num, i_text in enumerate(inv_headers, 1):
        cell = ws7.cell(row=5, column=c_num)
        cell.value = i_text
        cell.font = header_font
        cell.fill = primary_fill
        cell.alignment = align_center
        cell.border = border_all
        
    inv_data = [
        ["Initial Seed / Pre-Series A Round", "Rs. 10.00 Cr ($1.2M USD)", "Funding Phase 1 & 2 rollout across Karnataka"],
        ["Projected Year 5 ARR / Revenue", "Rs. 324.50 Cr ($39.0M USD)", "Across 50 Lakh farmers and 16,000 bank branches"],
        ["Projected Year 5 EBITDA", "Rs. 227.00 Cr ($27.2M USD)", "70.0% EBITDA Margin (Asset-light software/DPI)"],
        ["Target Exit Multiple (B2B SaaS / Fintech)", "12.0x EBITDA / 8.4x ARR", "Conservative comparative to Perfios, Zaggle, Lentra"],
        ["Estimated Year 5 Enterprise Valuation", "Rs. 2,724.00 Cr ($327M USD)", "Formula: Rs. 227 Cr EBITDA × 12.0x Multiple"],
        ["5-Year Equity ROI Multiple", "27.2x MOIC (Cash-on-Cash)", "High Return on Investment"],
        ["Projected Internal Rate of Return (IRR)", "118.5%", "High capital efficiency with rapid payback"],
        ["5-Year Cumulative Free Cash Flow Returned", "Rs. 275.40 Cr", "Allows self-funded expansion or special dividends"]
    ]
    
    for r_idx, (p_name, p_val, p_notes) in enumerate(inv_data, 6):
        cell_a = ws7.cell(row=r_idx, column=1, value=p_name)
        cell_b = ws7.cell(row=r_idx, column=2, value=p_val)
        cell_c = ws7.cell(row=r_idx, column=3, value=p_notes)
        is_highlight = "ROI" in p_name or "IRR" in p_name or "Valuation" in p_name
        cell_a.font = bold_font if is_highlight else normal_font
        cell_b.font = kpi_val_font if is_highlight else bold_font
        cell_c.font = italic_font
        cell_a.border = border_all
        cell_b.border = border_all
        cell_c.border = border_all
        if is_highlight:
            cell_a.fill = light_green_fill
            cell_b.fill = light_green_fill

    # Systemic Stakeholder Value Creation
    ws7["A16"] = "2. SYSTEMIC STAKEHOLDER ECONOMIC VALUE DELIVERED (ANNUALIZED AT YEAR 3)"
    ws7["A16"].font = section_font
    
    socio_headers = ["Beneficiary Stakeholder", "Nature of Economic Surplus Delivered", "Per Unit Impact", "Year 3 Aggregate Value (Rs. Cr)"]
    for c_num, s_text in enumerate(socio_headers, 1):
        cell = ws7.cell(row=17, column=c_num)
        cell.value = s_text
        cell.font = header_font
        cell.fill = secondary_fill
        cell.alignment = align_center
        cell.border = border_all
        
    socio_data = [
        ["Karnataka Farmers", "Saved physical travel, lost wages, and documentation agent fees", "Rs. 3,500 saved / farmer", "Rs. 420.00 Cr saved directly by farmers"],
        ["Karnataka Farmers", "Interest arbitrage (4% subsidized institutional KCC vs 24% informal moneylenders)", "Rs. 36,000 interest saved / loan", "Rs. 3,312.00 Cr interest savings across state"],
        ["Commercial & Rural Banks", "Reduced file processing cost & verified instant digital appraisal", "Rs. 1,500 saved / application", "Rs. 138.00 Cr in bank operational savings"],
        ["Commercial & Rural Banks", "Zero ghost-borrower fraud and pre-screened land dispute elimination", "Est. 1.2% NPA reduction", "Rs. 198.70 Cr reduction in potential non-performing assets"],
        ["Karnataka State Government", "Centralized administrative oversight, automated SLA enforcement & subsidy integrity", "Statewide efficiency", "Rs. 150.00 Cr in administrative efficiency & faster redressal"],
        ["TOTAL ANNUAL SYSTEMIC VALUE", "Quantifiable combined economic enhancement delivered to Karnataka", "Transformational", "Rs. 4,218.70 Cr Annually Generated!"]
    ]
    
    for r_idx, (stk, nat, per_u, agg_v) in enumerate(socio_data, 18):
        cell_1 = ws7.cell(row=r_idx, column=1, value=stk)
        cell_2 = ws7.cell(row=r_idx, column=2, value=nat)
        cell_3 = ws7.cell(row=r_idx, column=3, value=per_u)
        cell_4 = ws7.cell(row=r_idx, column=4, value=agg_v)
        
        is_tot = "TOTAL" in stk
        cell_1.font = bold_font if is_tot else normal_font
        cell_2.font = normal_font
        cell_3.font = bold_font if is_tot else normal_font
        cell_4.font = kpi_val_font if is_tot else bold_font
        
        cell_1.border = total_border if is_tot else border_all
        cell_2.border = total_border if is_tot else border_all
        cell_3.border = total_border if is_tot else border_all
        cell_4.border = total_border if is_tot else border_all
        
        if is_tot:
            cell_1.fill = light_orange_fill
            cell_2.fill = light_orange_fill
            cell_3.fill = light_orange_fill
            cell_4.fill = light_orange_fill

    # Auto-fit column widths across all sheets
    for sheet in wb.worksheets:
        for col in sheet.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                if cell.row in [1, 2, 3]:
                    continue
                if cell.value:
                    lines = str(cell.value).split("\n")
                    for line in lines:
                        if len(str(line)) > max_len:
                            max_len = len(str(line))
            sheet.column_dimensions[col_letter].width = max(max_len + 4, 15)
        sheet.column_dimensions["A"].width = 38
        if sheet.title == "Strategic Roadmap":
            sheet.column_dimensions["D"].width = 35
            sheet.column_dimensions["E"].width = 40
            sheet.column_dimensions["F"].width = 38
        if sheet.title == "Target Customers & Value":
            sheet.column_dimensions["C"].width = 35
            sheet.column_dimensions["D"].width = 40
            sheet.column_dimensions["E"].width = 38
            sheet.column_dimensions["F"].width = 35
            
    wb.save(output_path)
    print(f"Financial Model saved successfully to: {output_path}")

if __name__ == "__main__":
    os.makedirs(r"d:\KisanKavach\Project Docs", exist_ok=True)
    target = r"d:\KisanKavach\Project Docs\KisanKavach_Financial_Model_Roadmap.xlsx"
    build_financial_model(target)
