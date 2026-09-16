import { NextResponse } from 'next/server';
import { clearSessionCookie, getSession } from '@/lib/auth/session';
import { logAuditEvent } from '@/lib/audit/logger';

export async function POST() {
  const session = await getSession();
  if (session) {
    await logAuditEvent({
      userId: session.userId,
      userRole: session.role,
      action: 'LOGOUT',
      entity: 'User',
      entityId: session.userId,
    });
  }
  await clearSessionCookie();
  return NextResponse.json({ success: true });
}
