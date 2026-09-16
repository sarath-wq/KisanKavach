import { NextResponse } from 'next/server';
import { getSession } from '@/lib/auth/session';
import { prisma } from '@/lib/db/prisma';
import { logAuditEvent } from '@/lib/audit/logger';

export async function POST(request: Request) {
  try {
    const session = await getSession();
    const body = await request.json();
    const { category, textAnalyzed, source, riskScore, riskLevel } = body;

    const count = await prisma.fraudReport.count();
    const reportId = `KK-FR-2026-${String(count + 1).padStart(5, '0')}`;

    const report = await prisma.fraudReport.create({
      data: {
        reportId,
        farmerId: session?.farmerId || null,
        category: category || 'Phishing / SMS Scams',
        textAnalyzed: textAnalyzed || 'Reported message text',
        source: source || 'SMS',
        riskScore: parseFloat(riskScore || '85'),
        riskLevel: riskLevel || 'HIGH',
        reportedToGovt: true,
      },
    });

    if (session) {
      await logAuditEvent({
        userId: session.userId,
        userRole: session.role,
        action: 'FRAUD_REPORTED',
        entity: 'FraudReport',
        entityId: report.id,
        metadata: { reportId, riskLevel },
      });
    }

    return NextResponse.json({ success: true, report });
  } catch (error) {
    console.error('Fraud Report POST Error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
