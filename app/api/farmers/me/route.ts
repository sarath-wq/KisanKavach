import { NextResponse } from 'next/server';
import { getSession } from '@/lib/auth/session';
import { prisma } from '@/lib/db/prisma';

export async function GET() {
  try {
    const session = await getSession();
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const farmer = await prisma.farmer.findFirst({
      where: {
        OR: [
          { userId: session.userId },
          { id: session.farmerId || 'none' },
        ],
      },
      include: {
        district: true,
        taluk: true,
        village: true,
        landHoldings: { include: { crops: true } },
        applications: {
          orderBy: { submittedAt: 'desc' },
          include: { bankBranch: { include: { bank: true } } },
        },
        benefits: { include: { scheme: true } },
        policies: true,
        grievances: { orderBy: { createdAt: 'desc' } },
      },
    });

    if (!farmer) {
      return NextResponse.json({ error: 'Farmer profile not found' }, { status: 404 });
    }

    return NextResponse.json({ success: true, farmer, isSandbox: true });
  } catch (error) {
    console.error('Farmer Profile API Error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
