import { NextResponse } from 'next/server';
import { getSession } from '@/lib/auth/session';
import { prisma } from '@/lib/db/prisma';
import { logAuditEvent } from '@/lib/audit/logger';
import { ApplicationStage, ApplicationStatus } from '@prisma/client';

export async function GET(request: Request) {
  try {
    const session = await getSession();
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { searchParams } = new URL(request.url);
    const status = searchParams.get('status');
    const stage = searchParams.get('stage');
    const districtId = searchParams.get('districtId');
    const bankBranchId = searchParams.get('bankBranchId');
    const slaBreached = searchParams.get('slaBreached');

    // Build filter based on role & query params
    const where: any = {};

    if (session.role === 'FARMER') {
      const farmer = await prisma.farmer.findFirst({ where: { userId: session.userId } });
      if (farmer) where.farmerId = farmer.id;
    } else if (session.role === 'BANK_OFFICER') {
      if (session.bankBranchId) where.bankBranchId = session.bankBranchId;
    } else if (session.role === 'DISTRICT_OFFICER') {
      if (session.districtId) {
        where.bankBranch = { districtId: session.districtId };
      }
    }

    if (status) where.status = status as ApplicationStatus;
    if (stage) where.currentStage = stage as ApplicationStage;
    if (districtId) where.bankBranch = { ...where.bankBranch, districtId };
    if (bankBranchId) where.bankBranchId = bankBranchId;
    if (slaBreached === 'true') where.slaBreached = true;

    const applications = await prisma.kCCApplication.findMany({
      where,
      orderBy: { submittedAt: 'desc' },
      take: 100,
      include: {
        farmer: { include: { district: true, taluk: true } },
        bankBranch: { include: { bank: true, district: true } },
        documents: true,
      },
    });

    return NextResponse.json({ success: true, count: applications.length, applications });
  } catch (error) {
    console.error('KCC Applications API GET Error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const session = await getSession();
    if (!session || session.role !== 'FARMER') {
      return NextResponse.json({ error: 'Only farmers can submit KCC applications' }, { status: 403 });
    }

    const body = await request.json();
    const { loanAmountRequested, purpose, bankBranchId } = body;

    const farmer = await prisma.farmer.findFirst({ where: { userId: session.userId } });
    if (!farmer) {
      return NextResponse.json({ error: 'Farmer record not found' }, { status: 404 });
    }

    const branch = await prisma.bankBranch.findUnique({
      where: { id: bankBranchId || (await prisma.bankBranch.findFirst())?.id },
      include: { bank: true },
    });

    if (!branch) {
      return NextResponse.json({ error: 'Selected bank branch is invalid' }, { status: 400 });
    }

    const count = await prisma.kCCApplication.count();
    const applicationId = `KK-KA-2026-${String(count + 1).padStart(6, '0')}`;

    const app = await prisma.kCCApplication.create({
      data: {
        applicationId,
        farmerId: farmer.id,
        bankBranchId: branch.id,
        loanAmountRequested: parseFloat(loanAmountRequested || '100000'),
        purpose: purpose || 'Crop Cultivation & Agricultural Maintenance',
        currentStage: ApplicationStage.SUBMITTED,
        status: ApplicationStatus.PROCESSING,
        responsibleParty: branch.branchName,
        slaDaysTotal: 7,
        slaDaysElapsed: 0,
        slaBreached: false,
        remarks: 'Application submitted via KisanKavach portal with Bhoomi land record verification.',
      },
    });

    // Create status history
    await prisma.kCCApplicationStatusHistory.create({
      data: {
        applicationId: app.id,
        stage: ApplicationStage.SUBMITTED,
        status: ApplicationStatus.PROCESSING,
        actionByUser: session.name,
        remarks: 'Submitted initial application.',
      },
    });

    // Add standard mock documents
    await prisma.kCCDocument.createMany({
      data: [
        { applicationId: app.id, docType: 'Aadhaar Card', docName: 'aadhaar_verified.pdf', fileUrl: '/docs/mock_aadhaar.pdf', verified: true },
        { applicationId: app.id, docType: 'Bhoomi RTC Pahani', docName: 'bhoomi_rtc_verified.pdf', fileUrl: '/docs/mock_rtc.pdf', verified: true },
        { applicationId: app.id, docType: 'Bank Passbook', docName: 'bank_passbook.pdf', fileUrl: '/docs/mock_passbook.pdf', verified: true },
      ],
    });

    await logAuditEvent({
      userId: session.userId,
      userRole: session.role,
      action: 'APPLICATION_CREATED',
      entity: 'KCCApplication',
      entityId: app.id,
      metadata: { applicationId: app.applicationId, loanAmount: app.loanAmountRequested },
    });

    return NextResponse.json({ success: true, application: app });
  } catch (error) {
    console.error('KCC Applications API POST Error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
