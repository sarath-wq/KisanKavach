# 🌾 KisanKavach (ಕಿಸಾನ್ ಕವಚ)

> **Unified Farmer Benefit, KCC Loan Operations & Cyber Security Platform for Karnataka**

KisanKavach is an enterprise digital public infrastructure (DPI) platform designed for Karnataka farmers, commercial & cooperative banks, and state government officials. It streamlines Kisan Credit Card (KCC) loan processing, centralizes agricultural benefit schemes, provides automated crop insurance tracking, and protects rural citizens with AI-driven cyber risk detection.

---

## 🚀 Key Features

* **🌾 Farmer Experience**: 9-step KCC Loan Application Wizard, visual SLA countdown tracker, benefit discovery (PM-KISAN, PMFBY, MSP), crop insurance & KSNDMC weather advisories, Cyber Kavach phishing link/SMS risk analyzer, and multilingual AI Kisan Assistant (English & ಕನ್ನಡ).
* **🏦 Bank Officer Queue**: Live application queue, instant document verification, SLA breach warnings, multi-stage approval workflow, and structured rejection reason tracking.
* **🏛️ Government Command Dashboard**: Statewide KPIs across 10 pilot districts, bank processing velocity metrics, rejection analytics, grievance management, and 1-click CSV report export.
* **⚙️ System Admin Console**: Role-based access control (RBAC), SLA thresholds manager, and audit event logging.

---

## 🛠️ Technology Stack

* **Framework**: Next.js 15 (App Router, React 19)
* **Language**: TypeScript
* **Styling**: Tailwind CSS
* **Database & ORM**: Supabase PostgreSQL & Prisma ORM 6
* **Icons & Visuals**: Lucide React & Recharts
* **Authentication**: JWT Cookie Session Auth

---

## 📂 Getting Started

### 1. Prerequisites
* Node.js >= 18.18.0
* Supabase PostgreSQL Database

### 2. Environment Setup
Create a `.env` file in the root directory:

```env
DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres"
AUTH_SECRET="your_secret_key_here"
NEXT_PUBLIC_APP_URL="http://localhost:3000"
```

### 3. Installation & Database Seeding

```bash
# Install dependencies
npm install

# Push database schema to Supabase
npm run db:push

# Seed pilot data (10 Districts, 100+ Farmers, 250+ KCC Apps)
npm run db:seed

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🔐 Pre-seeded Demo Accounts

| Role | Email | Password |
| :--- | :--- | :--- |
| 🌾 **Farmer** | `farmer@demo.kisankavach.in` | `demo123` |
| 🏦 **Bank Officer** | `bank@demo.kisankavach.in` | `demo123` |
| 🏛️ **Govt Officer** | `gov@demo.kisankavach.in` | `demo123` |
| 📍 **District Officer** | `district@demo.kisankavach.in` | `demo123` |
| ⚙️ **System Admin** | `admin@demo.kisankavach.in` | `demo123` |

---

## 📜 License
Licensed under the Apache 2.0 License.
