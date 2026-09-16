import { NextResponse } from 'next/server';
import { getSession } from '@/lib/auth/session';
import { prisma } from '@/lib/db/prisma';

let DEMO_PENDING_REGISTRATIONS = [
  {
    id: 'reg-pending-101',
    name: 'Mahesh Kumar',
    email: 'mahesh.farmer@demo.kisankavach.in',
    role: 'FARMER',
    mobile: '9845011999',
    district: 'Mysuru',
    branch: 'N/A',
    idProof: 'Aadhaar: XXXX-XXXX-9128',
    status: 'PENDING_APPROVAL',
    submittedAt: new Date(Date.now() - 3600000).toISOString(),
  },
  {
    id: 'reg-pending-102',
    name: 'Smt. Archana Rao',
    email: 'archana.bank@demo.kisankavach.in',
    role: 'BANK_OFFICER',
    mobile: '9845022888',
    district: 'Mandya',
    branch: 'SBI — Mandya Branch',
    idProof: 'Employee ID: SBI-MND-4421',
    status: 'PENDING_APPROVAL',
    submittedAt: new Date(Date.now() - 7200000).toISOString(),
  }
];

export async function GET() {
  try {
    const session = await getSession();
    if (session && session.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized admin access' }, { status: 403 });
    }

    return NextResponse.json({
      success: true,
      pendingRegistrations: DEMO_PENDING_REGISTRATIONS,
    });
  } catch (error) {
    return NextResponse.json({ success: true, pendingRegistrations: DEMO_PENDING_REGISTRATIONS });
  }
}

export async function POST(request: Request) {
  try {
    const session = await getSession();
    const body = await request.json();
    const { registrationId, action, rejectionReason } = body;

    if (!registrationId || !action) {
      return NextResponse.json({ error: 'registrationId and action are required' }, { status: 400 });
    }

    // Process approval/rejection
    const foundIdx = DEMO_PENDING_REGISTRATIONS.findIndex(r => r.id === registrationId);
    if (foundIdx !== -1) {
      if (action === 'APPROVE') {
        DEMO_PENDING_REGISTRATIONS[foundIdx].status = 'APPROVED';
      } else {
        DEMO_PENDING_REGISTRATIONS[foundIdx].status = 'REJECTED';
      }
    }

    return NextResponse.json({
      success: true,
      message: `User registration ${action === 'APPROVE' ? 'APPROVED and account activated' : 'REJECTED'}.`,
    });
  } catch (error: any) {
    return NextResponse.json({ error: 'Failed to update registration status' }, { status: 500 });
  }
}
