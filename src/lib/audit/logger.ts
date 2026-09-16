import { prisma } from '../db/prisma';

export interface AuditEventInput {
  userId?: string;
  userRole?: string;
  action: string;
  entity: string;
  entityId?: string;
  metadata?: Record<string, unknown>;
  ipAddress?: string;
}

export async function logAuditEvent(input: AuditEventInput) {
  try {
    await prisma.auditLog.create({
      data: {
        userId: input.userId,
        userRole: input.userRole,
        action: input.action,
        entity: input.entity,
        entityId: input.entityId,
        metadataJson: input.metadata ? JSON.stringify(input.metadata) : null,
        ipAddress: input.ipAddress || '127.0.0.1',
      },
    });
  } catch (error) {
    console.error('Failed to log audit event:', error);
  }
}
