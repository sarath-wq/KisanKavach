# KisanKavach: Enterprise Production Deployment Architecture
**Document Reference**: KK-ARCH-DEP-2026-001  
**Project**: KisanKavach (ಕಿಸಾನ್ ಕವಚ) — Agricultural Credit, Benefits & Fraud Defense DPI  
**Author & Lead Architect**: Sarath Babu Rayaprolu  
**Target Environments**: UAT, Staging, Statewide Karnataka Production (31 Districts), Multi-Region DR  
**Compliance Mandates**: DPDP Act 2023, RBI IT Framework Master Directions, CERT-In Cyber Guidelines, MeitY Cloud Mandate  

---

## 1. Executive Architectural Blueprint

KisanKavach requires a **Bank-Grade, Multi-Tier, Sovereign Cloud-Native Architecture** designed to handle:
* **Scale**: 5,000,000+ registered farmers, 16,000+ bank branches, 4,000,000 annual loan originations.
* **Latency**: < 250ms API response time across 2G/3G/4G rural networks.
* **Availability**: 99.95% uptime SLA with active-passive multi-region Disaster Recovery (RPO = 0, RTO < 15 mins).
* **Security**: Zero Trust, end-to-end 256-bit encryption, hardware security modules (HSM) for digital signatures, and dedicated private tunnels (IPsec/DirectConnect) to Bank Core Banking Systems (Finacle, BaNCS, Flexcube).

```
                            [ FARMER MOBILE APP / WEB PWA / CSC OPERATORS ]
                                                 │
                                                 ▼ (HTTPS / TLS 1.3)
                       ┌──────────────────────────────────────────────────┐
                       │  EDGE LAYER: Cloudflare Enterprise / AWS WAF     │
                       │  - DDoS Protection (L3/L4/L7)                    │
                       │  - Geo-blocking (India Sovereign Traffic Only)   │
                       │  - Web Application Firewall (OWASP Top 10)       │
                       │  - Edge Asset Caching & Brotli Compression       │
                       └─────────────────────────┬────────────────────────┘
                                                 │
                                                 ▼ (Mutual TLS / Reverse Proxy)
                       ┌──────────────────────────────────────────────────┐
                       │  INGRESS & API GATEWAY (Kong / NGINX Ingress)    │
                       │  - OAuth2 / JWT Token Validation                 │
                       │  - Rate Limiting (Per-IP / Per-Device / Per-CSC) │
                       │  - Request ID Tracing & DPI Consent Headers      │
                       └────────┬───────────────────────────────┬─────────┘
                                │                               │
         ┌──────────────────────▼─────────────────┐   ┌─────────▼────────────────────────┐
         │ WEB FRONTEND PODS (Next.js 15 SSR)    │   │ CORE API MICROSERVICES (Node/FastAPI)│
         │ - Responsive PWA & Admin Dashboards   │   │ - Loan Origination Service (LOS)  │
         │ - Bank Maker-Checker Console          │   │ - Bhoomi & FRUITS Adapter Engine │
         │ - SLBC & Collector Command Center     │   │ - CyberKavach AI Fraud Engine     │
         │ - Autoscaled HPA (Kubernetes / EKS)   │   │ - SLA Countdown & Grievance Svc   │
         └──────────────────────┬─────────────────┘   └─────────┬────────────────────────┘
                                │                               │
                                └───────────────┬───────────────┘
                                                │
                 ┌──────────────────────────────┼──────────────────────────────┐
                 ▼                              ▼                              ▼
    ┌─────────────────────────┐    ┌─────────────────────────┐    ┌─────────────────────────┐
    │ DISTRIBUTED REDIS CLUSTER│    │ ASYNC MESSAGE QUEUE     │    │ ENTERPRISE DATABASE     │
    │ - Session State & Cache │    │ (Apache Kafka / BullMQ) │    │ (Managed PostgreSQL 16) │
    │ - Real-Time SLA Timers  │    │ - SMS DLT Dispatch      │    │ - Supabase / AWS Aurora │
    │ - API Rate Limits       │    │ - Credit Bureau Queue   │    │ - Multi-AZ Synchronous  │
    │ - Bhoomi Record Caching │    │ - Webhook Notifications │    │ - Row-Level Security RLS│
    └─────────────────────────┘    └─────────────────────────┘    └────────────┬────────────┘
                                                                               │
                                    ┌──────────────────────────────────────────┴────────────┐
                                    ▼ (Read Replica)                                        ▼ (S3 Storage)
                       ┌─────────────────────────┐                             ┌─────────────────────────┐
                       │ ANALYTICS READ REPLICA  │                             │ DOCUMENT VAULT (S3)     │
                       │ - District Drilldowns   │                             │ - Encrypted RTC Deeds   │
                       │ - SLBC Scorecards       │                             │ - Field Survey Photos   │
                       │ - Lead District Mgrs    │                             │ - Sanction Letters      │
                       └─────────────────────────┘                             └─────────────────────────┘
                                                │
                                                ▼ (Dedicated Secure IPsec VPN / DirectConnect)
                       ┌──────────────────────────────────────────────────┐
                       │ EXTERNAL STATUTORY & BANKING INTEGRATION TUNNEL  │
                       │ • Karnataka Bhoomi (Revenue Dept - Land Records) │
                       │ • Karnataka FRUITS (Dept. of Agriculture)        │
                       │ • Partner Bank CBS (SBI, Canara, KVGB, KBL)      │
                       │ • Credit Bureaus (CIBIL / Experian)              │
                       │ • UIDAI Aadhaar eKYC Gateway & SMS-DLT Route     │
                       └──────────────────────────────────────────────────┘
```

---

## 2. Seven-Tier Component Architecture Breakdown

### Tier 1: Client & Distribution Layer
* **Web Client**: Next.js 15 PWA optimized for desktop and touch mobile (`kisan.digikavach.net`).
* **Mobile Client**: Capacitor 6 Native Android Application APK with offline caching and camera hardware bridge.
* **Assisted Mode**: Dedicated Grama One / CSC Kiosk mode with multi-applicant queueing and biometric scanner compatibility.

### Tier 2: Perimeter Security & Ingress Layer
* **Cloud WAF & CDN**: Cloudflare Enterprise or AWS CloudFront + WAF configured with:
  * OWASP Top 10 managed rules (SQLi, XSS, CSRF).
  * Geofencing: Restrict access strictly to Indian IP ranges (`IN`), blocking foreign proxy attacks.
  * DDoS Shield: Layer 3, 4, and 7 automated rate scrubbing.
* **API Gateway**: Kong Gateway or Kubernetes NGINX Ingress Controller terminating TLS 1.3 and managing mutual TLS (mTLS) for bank connections.

### Tier 3: Compute & Microservices Orchestration (Kubernetes / EKS)
* Containerized stateless Docker microservices running on managed Kubernetes (AWS EKS or Azure AKS) deployed across 3 Availability Zones (AZs):
  1. `kisan-web`: Next.js 15 SSR / Static Edge frontend.
  2. `kisan-los-api`: Loan Origination & Maker-Checker underwriting state machine.
  3. `kisan-bhoomi-fruits`: Connector microservice handling statutory API handshakes, rate throttling, and payload transformation.
  4. `kisan-cyberkavach`: High-performance Python/FastAPI service hosting ML and heuristic scam/phishing analysis models.
  5. `kisan-sla-scheduler`: Distributed cron service monitoring the 7-day SLA countdown and auto-escalations to District Collectors.
* **Autoscaling**: Kubernetes Horizontal Pod Autoscaler (HPA) scaling between 10 pods (baseline) and 120 pods (peak sowing season demand).

### Tier 4: Asynchronous Processing & In-Memory Caching
* **Redis Cluster (Multi-AZ)**:
  * Cache layer for static land classifications, taluk codes, and crop Scale of Finance rates.
  * Fast distributed locks preventing race conditions on concurrent loan applications.
* **Event Broker / Queue (Apache Kafka / Redis BullMQ)**:
  * Handles non-blocking asynchronous jobs: SMS DLT alerts, WhatsApp notifications, CIBIL bureau pulls, and webhook retries.
  * Guaranteed at-least-once delivery with Dead Letter Queues (DLQ).

### Tier 5: Enterprise Data & Document Storage
* **Primary Database**: Managed PostgreSQL 16 (AWS Aurora PostgreSQL Multi-AZ or Supabase Self-Hosted on K8s):
  * Primary read-write instance with 2 synchronous standby read replicas in separate AZs.
  * Enforced **Row-Level Security (RLS)** ensuring bank branch officers only see loan files within their designated bank code and district jurisdiction.
  * Encrypted at rest using AWS KMS Customer Managed Keys (CMK) / AES-256.
* **Document Vault (Object Storage)**:
  * AWS S3 or MinIO with Server-Side Encryption (SSE-KMS).
  * Lifecycle policies: Uploaded Pahani/RTC PDFs and geo-tagged field verification photos stored with immutable object locking (WORM) for 7 years to satisfy banking statutory audit rules.

### Tier 6: Banking & Statutory Secure Integration Highway
* **Bank CBS Connectivity**:
  * Dedicated IPsec VPN Tunnels or AWS DirectConnect circuits connecting KisanKavach VPC to anchor bank data centers (Canara Bank, SBI, KVGB).
  * Standardized ISO-8583 / REST JSON adapters for Finacle, BaNCS, and Flexcube.
* **State Government Gateway**:
  * Direct dedicated connection to Karnataka State Data Centre (SDC) for Bhoomi and FRUITS APIs via private lease-line / SSL VPN.
* **UIDAI & Credit Bureaus**:
  * ASA/KUA-compliant gateway for Aadhaar OTP eKYC and licensed bureau connectors for instant CIBIL credit scoring.

### Tier 7: Observability, SIEM & Security Auditing
* **Telemetry**: OpenTelemetry collectors feeding metrics, traces, and structured logs into Prometheus & Grafana.
* **SIEM / Audit**: Centralized Wazuh / Datadog SIEM monitoring system events for anomalous logins, privilege escalation, and suspicious database queries.
* **Audit Trail Compliance**: Immutable audit log table recording every viewing, approval, or rejection of farmer records to ensure 100% compliance with CERT-In and DPDP Act 2023.

---

## 3. Recommended Deployment Options Comparison

| Dimension | Option A: Sovereign Cloud-Native (AWS / Azure India) — **RECOMMENDED** | Option B: Karnataka State Data Centre (SDC) / MeghRaj (NIC) | Option C: Managed PaaS (Vercel + Supabase Enterprise) |
| :--- | :--- | :--- | :--- |
| **Best Suited For** | **Statewide & Pan-India Scale (Phase 2 to 4)** | **Strict B2G Government-Owned Infra** | **Rapid Pilot & Staging Demonstration** |
| **Hosting Geography** | AWS Mumbai (`ap-south-1`) + Hyderabad (`ap-south-2`) | Bengaluru SDC / NIC MeghRaj Data Center | AWS Mumbai Region (via Vercel & Supabase) |
| **Scalability** | Automated elastic autoscaling (1,000 to 500,000 req/min) | Manual VM provisioning & physical hardware allocation | High automated serverless scale |
| **Bank CBS Integration** | DirectConnect / PrivateLink / IPsec VPN supported | Direct SDC intra-network routing | Requires secure IPsec proxy/NAT gateway |
| **Compliance** | CERT-In, SOC2 Type II, ISO-27001, RBI Master Directions | Government Security Audited, NIC Approved | SOC2 Type II, HIPAA, ISO-27001 |
| **Setup Timeline** | **2 to 3 Weeks (via Terraform IaC)** | 8 to 12 Weeks (Govt procurement cycle) | **Immediate (< 24 Hours)** |
| **Monthly Run-Rate (Statewide)** | ~$2,800 – $4,500 / month | Subsidized Govt budgeting | ~$1,200 – $2,000 / month |

---

## 4. Disaster Recovery (DR) & High Availability Architecture

To guarantee the **99.95% availability mandate** required by the State Level Bankers' Committee:
* **Primary Site**: AWS Mumbai (`ap-south-1`) — 3 Availability Zones (AZ-1a, AZ-1b, AZ-1c).
* **Secondary / DR Site**: AWS Hyderabad (`ap-south-2`) — Hot Standby read-replica with automated failover.
* **Recovery Point Objective (RPO)**: `0 minutes` for financial transactions (synchronous Aurora multi-AZ replication); `< 5 minutes` for document storage.
* **Recovery Time Objective (RTO)**: `< 15 minutes` via Route53 DNS health check automatic failover to the DR region.

---

## 5. Capacity Sizing & Operational Cost Matrix

| Infrastructure Tier | 10 Pilot Districts (Current) | 31 Karnataka Districts (Phase 2) | Pan-India Scale (Phase 4) |
| :--- | :--- | :--- | :--- |
| **Active Farmers** | 1,50,000 | 5,00,000 – 1,200,000 | 5,00,0000+ |
| **Peak Requests / Sec** | 150 RPS | 1,200 RPS | 10,000+ RPS |
| **Compute Pods** | 4 – 8 EKS Pods (m6i.large) | 16 – 32 EKS Pods (c6i.xlarge) | 100+ Distributed Pods |
| **Database Instance** | db.r6g.xlarge (Multi-AZ) | db.r6g.2xlarge + 2 Replicas | Aurora PostgreSQL Serverless v2 |
| **Storage (Documents)** | 2.5 TB (Encrypted S3) | 18 TB (Encrypted S3) | 120+ TB S3 Intelligent Tiering |
| **Monthly Cloud Budget** | **$850 – $1,200 / month** | **$2,800 – $4,200 / month** | **$12,000 – $18,000 / month** |

---

## 6. Infrastructure-as-Code (IaC) & Deployment Pipeline

```
 [ Git Repository: main branch ]
               │
               ▼
 [ GitHub Actions CI/CD Pipeline ]
   ├─ Step 1: Linting, TypeScript Typecheck & Unit Tests
   ├─ Step 2: Container Security Vulnerability Scan (Trivy)
   ├─ Step 3: SonarQube Static Code Analysis & SAST
   ├─ Step 4: Multi-Arch Docker Container Build (linux/amd64)
   ├─ Step 5: Push Signed Image to AWS ECR (Immutable Tags)
   └─ Step 6: GitOps Deploy via ArgoCD / Helm to Kubernetes Cluster
               │
               ▼
   [ Blue-Green Zero-Downtime Rollout to Production Pods ]
```

---

## 7. Immediate Action Checklist to Deploy Statewide (Phase 2)

1. **Provision Sovereign VPC**: Deploy dual-region AWS India VPC using Terraform scripts with public, private, and database subnets.
2. **Configure Dedicated IPsec VPN**: Establish test and production VPN tunnels with Canara Bank and State Bank of India CBS gateways.
3. **Database Migration & RLS Lockdown**: Migrate Supabase schema and RLS policies to AWS Aurora PostgreSQL 16 with automated nightly backups.
4. **CERT-In Security Audit**: Engage a CERT-In empaneled cybersecurity auditor for VAPT (Vulnerability Assessment & Penetration Testing) of web, mobile, and API endpoints.
5. **Establish SLBC Monitoring Enclave**: Provision dedicated read-only analytics replicas for the State Command Center dashboard.
