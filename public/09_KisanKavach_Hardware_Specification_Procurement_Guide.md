# KisanKavach: Hardware Infrastructure Specification & Procurement Blueprint
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
