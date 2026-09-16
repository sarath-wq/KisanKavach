import { NextResponse } from 'next/server';
import { getSession } from '@/lib/auth/session';
import { prisma } from '@/lib/db/prisma';
import { logAuditEvent } from '@/lib/audit/logger';
import { GrievanceCategory } from '@prisma/client';

export async function GET(request: Request) {
  try {
    const session = await getSession();
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { searchParams } = new URL(request.url);
    const category = searchParams.get('category');
    const status = searchParams.get('status');

    const where: any = {};
    if (session.role === 'FARMER') {
      const farmer = await prisma.farmer.findFirst({ where: { userId: session.userId } });
      if (farmer) where.farmerId = farmer.id;
    } else if (session.role === 'DISTRICT_OFFICER') {
      if (session.districtId) {
        where.farmer = { districtId: session.districtId };
      }
    }

    if (category) where.category = category as GrievanceCategory;
    if (status) where.status = status;

    const grievances = await prisma.grievance.findMany({
      where,
      orderBy: { createdAt: 'desc' },
      take: 100,
      include: {
        farmer: { include: { district: true } },
        application: true,
        comments: { include: { user: true } },
      },
    });

    return NextResponse.json({ success: true, count: grievances.length, grievances });
  } catch (error) {
    console.error('Grievances GET API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const session = await getSession();
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await request.json();
    const { category, subject, description, applicationId, priority } = body;

    if (!category || !subject || !description) {
      return NextResponse.json({ error: 'Category, subject, and description are required' }, { status: 400 });
    }

    const farmer = await prisma.farmer.findFirst({ where: { userId: session.userId } });
    if (!farmer) {
      return NextResponse.json({ error: 'Farmer record not found' }, { status: 404 });
    }

    const count = await prisma.grievance.count();
    const grievanceId = `KK-GR-2026-${String(count + 1).padStart(6, '0')}`;

    const grievance = await prisma.grievance.create({
      data: {
        grievanceId,
        farmerId: farmer.id,
        applicationId: applicationId || null,
        category: category as GrievanceCategory,
        subject,
        description,
        status: 'REGISTERED',
        priority: priority || 'MEDIUM',
      },
    });

    await logAuditEvent({
      userId: session.userId,
      userRole: session.role,
      action: 'GRIEVANCE_CREATED',
      entity: 'Grievance',
      entityId: grievance.id,
      metadata: { grievanceId, category, subject },
    });

    return NextResponse.json({ success: true, grievance });
  } catch (error) {
    console.error('Grievance POST API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
