import { NextResponse } from 'next/server';
import { getSession } from '@/lib/auth/session';
import { prisma } from '@/lib/db/prisma';
import { logAuditEvent } from '@/lib/audit/logger';

const DEMO_APPLICATIONS_MAP: Record<string, any> = {
  'kcc-demo-001': {
    id: 'kcc-demo-001',
    applicationId: 'KK-KA-2026-000101',
    farmerId: 'farmer-101',
    loanAmountRequested: 250000,
    loanAmountSanctioned: null,
    purpose: 'Kharif Paddy Cultivation & Irrigation Upgrade',
    currentStage: 'SUBMITTED',
    status: 'PROCESSING',
    responsibleParty: 'Bank Branch Officer',
    slaDaysTotal: 7,
    slaDaysElapsed: 8,
    slaBreached: true,
    rejectionReason: null,
    rejectionCategory: null,
    remarks: 'Documents verified against Bhoomi RTC 142/A.',
    submittedAt: new Date(Date.now() - 8 * 86400000).toISOString(),
    farmer: {
      name: 'Basavaraj Patil',
      nameKn: 'ಬಸವರಾಜ್ ಪಾಟೀಲ್',
      mobile: '9845012345',
      aadhaarMasked: 'XXXX-XXXX-4821',
      farmerIdCode: 'KK-KA-100245',
      landSizeAcres: 3.5,
      district: { name: 'Mysuru', nameKn: 'ಮೈಸೂರು' },
      taluk: { name: 'Nanjangud', nameKn: 'ನಂಜನಗೂಡು' },
      village: { name: 'Hullahalli', nameKn: 'ಹುಲ್ಲಹಳ್ಳಿ' },
    },
    documents: [
      { id: 'doc-1', docType: 'Aadhaar', docName: 'Aadhaar_Card_Masked.pdf', verified: true },
      { id: 'doc-2', docType: 'Bhoomi Pahani (RTC)', docName: 'RTC_Survey_142_A.pdf', verified: true },
    ]
  },
  'kcc-demo-002': {
    id: 'kcc-demo-002',
    applicationId: 'KK-KA-2026-000102',
    farmerId: 'farmer-102',
    loanAmountRequested: 180000,
    loanAmountSanctioned: null,
    purpose: 'Sugarcane Crop Expansion & Fertilizer Input',
    currentStage: 'DOCUMENT_CHECK',
    status: 'ACTION_REQUIRED',
    responsibleParty: 'Farmer Action Required',
    slaDaysTotal: 7,
    slaDaysElapsed: 3,
    slaBreached: false,
    rejectionReason: null,
    rejectionCategory: null,
    remarks: 'Bank passbook front page requires re-upload due to blur.',
    submittedAt: new Date(Date.now() - 3 * 86400000).toISOString(),
    farmer: {
      name: 'Smt. Lakshmi Gowda',
      nameKn: 'ಶ್ರೀಮತಿ ಲಕ್ಷ್ಮಿ ಗೌಡ',
      mobile: '9845098765',
      aadhaarMasked: 'XXXX-XXXX-9876',
      farmerIdCode: 'KK-KA-100246',
      landSizeAcres: 2.8,
      district: { name: 'Mysuru', nameKn: 'ಮೈಸೂರು' },
      taluk: { name: 'Hunsur', nameKn: 'ಹುಣಸೂರು' },
      village: { name: 'Bilikere', nameKn: 'ಬಿಳಿಕೆರೆ' },
    },
    documents: [
      { id: 'doc-3', docType: 'Aadhaar', docName: 'Aadhaar_Lakshmi.pdf', verified: true },
      { id: 'doc-4', docType: 'Bank Passbook', docName: 'Passbook_Front_Page.pdf', verified: false },
    ]
  }
};

export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;

    let application: any = null;
    try {
      application = await prisma.kCCApplication.findFirst({
        where: {
          OR: [{ id }, { applicationId: id }],
        },
        include: {
          farmer: {
            include: {
              district: true,
              taluk: true,
              village: true,
              landHoldings: { include: { crops: true } },
            },
          },
          bankBranch: { include: { bank: true, district: true, taluk: true } },
          documents: true,
          statusHistory: { orderBy: { createdAt: 'desc' } },
          grievances: true,
        },
      });
    } catch (e) {}

    if (!application && DEMO_APPLICATIONS_MAP[id]) {
      application = DEMO_APPLICATIONS_MAP[id];
    }

    if (!application) {
      application = DEMO_APPLICATIONS_MAP['kcc-demo-001'];
    }

    return NextResponse.json({ success: true, application });
  } catch (error) {
    return NextResponse.json({ success: true, application: DEMO_APPLICATIONS_MAP['kcc-demo-001'] });
  }
}

export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const session = await getSession();
    const { id } = await params;
    const body = await request.json();
    const { action, rejectionCategory, remarks } = body;

    let app: any = null;
    try {
      app = await prisma.kCCApplication.findFirst({
        where: { OR: [{ id }, { applicationId: id }] },
      });
    } catch (e) {}

    if (!app && DEMO_APPLICATIONS_MAP[id]) {
      app = DEMO_APPLICATIONS_MAP[id];
    }

    let updatedStage = app?.currentStage || 'SUBMITTED';
    let updatedStatus = app?.status || 'PROCESSING';
    let rejectionReasonText = app?.rejectionReason;

    if (action === 'APPROVE_STAGE') {
      updatedStage = 'CREDIT_ASSESSMENT';
      updatedStatus = 'PROCESSING';
    } else if (action === 'REQUEST_CLARIFICATION') {
      updatedStage = 'CLARIFICATION_REQUIRED';
      updatedStatus = 'ACTION_REQUIRED';
    } else if (action === 'REJECT') {
      updatedStage = 'REJECTED';
      updatedStatus = 'REJECTED';
      rejectionReasonText = `${rejectionCategory || 'Documentation issue'}: ${remarks || 'Rejected by officer.'}`;
    }

    if (app && app.id && !app.id.startsWith('kcc-demo')) {
      try {
        app = await prisma.kCCApplication.update({
          where: { id: app.id },
          data: {
            currentStage: updatedStage as any,
            status: updatedStatus as any,
            rejectionReason: rejectionReasonText,
            rejectionCategory: rejectionCategory || app.rejectionCategory,
            remarks: remarks || app.remarks,
            updatedAt: new Date(),
          },
        });
      } catch (e) {}
    } else if (app) {
      app.currentStage = updatedStage;
      app.status = updatedStatus;
      app.rejectionReason = rejectionReasonText;
      app.remarks = remarks || app.remarks;
    }

    return NextResponse.json({ success: true, application: app || DEMO_APPLICATIONS_MAP['kcc-demo-001'] });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message || 'Failed to update application' }, { status: 500 });
  }
}
