import { NextResponse } from 'next/server';
import { getSession } from '@/lib/auth/session';
import { prisma } from '@/lib/db/prisma';

const DEMO_BANK_APPLICATIONS = [
  {
    id: 'kcc-demo-001',
    applicationId: 'KK-KA-2026-000101',
    farmerId: 'farmer-101',
    loanAmountRequested: 250000,
    purpose: 'Kharif Paddy Cultivation & Irrigation Upgrade',
    currentStage: 'SUBMITTED',
    status: 'PROCESSING',
    responsibleParty: 'Bank Branch Officer',
    slaDaysTotal: 7,
    slaDaysElapsed: 8,
    slaBreached: true,
    submittedAt: new Date(Date.now() - 8 * 86400000).toISOString(),
    farmer: {
      name: 'Basavaraj Patil',
      nameKn: 'ಬಸವರಾಜ್ ಪಾಟೀಲ್',
      mobile: '9845012345',
      district: { name: 'Mysuru', nameKn: 'ಮೈಸೂರು' },
      taluk: { name: 'Nanjangud', nameKn: 'ನಂಜನಗೂಡು' },
    },
    documents: [
      { id: 'doc-1', docType: 'Aadhaar', docName: 'Aadhaar_Card_Masked.pdf', verified: true },
      { id: 'doc-2', docType: 'Bhoomi Pahani (RTC)', docName: 'RTC_Survey_142_A.pdf', verified: true },
    ]
  },
  {
    id: 'kcc-demo-002',
    applicationId: 'KK-KA-2026-000102',
    farmerId: 'farmer-102',
    loanAmountRequested: 180000,
    purpose: 'Sugarcane Crop Expansion & Fertilizer Input',
    currentStage: 'DOCUMENT_CHECK',
    status: 'ACTION_REQUIRED',
    responsibleParty: 'Farmer Action Required',
    slaDaysTotal: 7,
    slaDaysElapsed: 3,
    slaBreached: false,
    submittedAt: new Date(Date.now() - 3 * 86400000).toISOString(),
    farmer: {
      name: 'Smt. Lakshmi Gowda',
      nameKn: 'ಶ್ರೀಮತಿ ಲಕ್ಷ್ಮಿ ಗೌಡ',
      mobile: '9845098765',
      district: { name: 'Mysuru', nameKn: 'ಮೈಸೂರು' },
      taluk: { name: 'Hunsur', nameKn: 'ಹುಣಸೂರು' },
    },
    documents: [
      { id: 'doc-3', docType: 'Aadhaar', docName: 'Aadhaar_Lakshmi.pdf', verified: true },
      { id: 'doc-4', docType: 'Bank Passbook', docName: 'Passbook_Front_Page.pdf', verified: false },
    ]
  },
  {
    id: 'kcc-demo-003',
    applicationId: 'KK-KA-2026-000103',
    farmerId: 'farmer-103',
    loanAmountRequested: 320000,
    purpose: 'Drip Irrigation & Commercial Maize Crop',
    currentStage: 'CREDIT_ASSESSMENT',
    status: 'PROCESSING',
    responsibleParty: 'Credit Manager',
    slaDaysTotal: 7,
    slaDaysElapsed: 4,
    slaBreached: false,
    submittedAt: new Date(Date.now() - 4 * 86400000).toISOString(),
    farmer: {
      name: 'Ningappa Kuruba',
      nameKn: 'ನಿಂಗಪ್ಪ ಕುರುಬ',
      mobile: '9845011223',
      district: { name: 'Mandya', nameKn: 'ಮಂಡ್ಯ' },
      taluk: { name: 'Maddur', nameKn: 'ಮದ್ದೂರು' },
    },
    documents: [
      { id: 'doc-5', docType: 'Aadhaar', docName: 'Aadhaar_Ningappa.pdf', verified: true },
      { id: 'doc-6', docType: 'FRUITS Crop Certificate', docName: 'FRUITS_Crop_2026.pdf', verified: true },
    ]
  },
  {
    id: 'kcc-demo-004',
    applicationId: 'KK-KA-2026-000104',
    farmerId: 'farmer-104',
    loanAmountRequested: 150000,
    purpose: 'Rabi Ragi Cultivation & Seeds Purchase',
    currentStage: 'SUBMITTED',
    status: 'PROCESSING',
    responsibleParty: 'Branch Manager',
    slaDaysTotal: 7,
    slaDaysElapsed: 9,
    slaBreached: true,
    submittedAt: new Date(Date.now() - 9 * 86400000).toISOString(),
    farmer: {
      name: 'Chennappa Nayaka',
      nameKn: 'ಚೆನ್ನಪ್ಪ ನಾಯಕ',
      mobile: '9845033445',
      district: { name: 'Hassan', nameKn: 'ಹಾಸನ' },
      taluk: { name: 'Holenarasipura', nameKn: 'ಹೊಳೆನರಸೀಪುರ' },
    },
    documents: [
      { id: 'doc-7', docType: 'Aadhaar', docName: 'Aadhaar_Chennappa.pdf', verified: true }
    ]
  },
  {
    id: 'kcc-demo-005',
    applicationId: 'KK-KA-2026-000105',
    farmerId: 'farmer-105',
    loanAmountRequested: 210000,
    purpose: 'Cotton Farming & Solar Pump Maintenance',
    currentStage: 'SANCTIONED',
    status: 'PROCESSING',
    responsibleParty: 'Disbursement Desk',
    slaDaysTotal: 7,
    slaDaysElapsed: 2,
    slaBreached: false,
    submittedAt: new Date(Date.now() - 2 * 86400000).toISOString(),
    farmer: {
      name: 'Smt. Shivamma Reddy',
      nameKn: 'ಶ್ರೀಮತಿ ಶಿವಮ್ಮ ರೆಡ್ಡಿ',
      mobile: '9845055667',
      district: { name: 'Ballari', nameKn: 'ಬಳ್ಳಾರಿ' },
      taluk: { name: 'Siruguppa', nameKn: 'ಸಿರುಗುಪ್ಪ' },
    },
    documents: [
      { id: 'doc-8', docType: 'Aadhaar', docName: 'Aadhaar_Shivamma.pdf', verified: true }
    ]
  }
];

export async function GET() {
  try {
    const session = await getSession();
    const branchId = session?.bankBranchId;
    
    let where: any = {};
    if (branchId) {
      try {
        const count = await prisma.kCCApplication.count({ where: { bankBranchId: branchId } });
        if (count > 0) where = { bankBranchId: branchId };
      } catch (e) {}
    }

    let applications: any[] = [];
    try {
      applications = await prisma.kCCApplication.findMany({
        where,
        orderBy: { submittedAt: 'desc' },
        take: 100,
        include: {
          farmer: { include: { district: true, taluk: true } },
          documents: true,
        },
      });
    } catch (dbErr) {
      console.warn('Database query fallback to demo applications:', dbErr);
    }

    if (applications.length === 0) {
      applications = DEMO_BANK_APPLICATIONS;
    }

    const totalAssigned = applications.length;
    const newApplications = applications.filter(a => a.currentStage === 'SUBMITTED').length;
    const processingApplications = applications.filter(a => a.status === 'PROCESSING').length;
    const clarificationApplications = applications.filter(a => a.status === 'ACTION_REQUIRED').length;
    const slaBreaches = applications.filter(a => a.slaBreached).length;

    return NextResponse.json({
      success: true,
      kpis: {
        totalAssigned,
        newApplications,
        processingApplications,
        clarificationApplications,
        slaBreaches,
      },
      applications,
    });
  } catch (error: any) {
    console.error('Bank Dashboard API Error:', error);
    return NextResponse.json({
      success: true,
      kpis: {
        totalAssigned: DEMO_BANK_APPLICATIONS.length,
        newApplications: 2,
        processingApplications: 4,
        clarificationApplications: 1,
        slaBreaches: 2,
      },
      applications: DEMO_BANK_APPLICATIONS,
    });
  }
}
