export interface SLACalculation {
  totalDays: number;
  elapsedDays: number;
  remainingDays: number;
  isBreached: boolean;
  statusColor: 'GREEN' | 'AMBER' | 'RED';
  percentageConsumed: number;
}

export const DEFAULT_STAGE_SLA: Record<string, number> = {
  SUBMITTED: 1,
  FARMER_VERIFICATION: 2,
  LAND_VERIFICATION: 2,
  DOCUMENT_VERIFICATION: 2,
  CREDIT_ASSESSMENT: 5,
  SANCTION_PENDING: 3,
  SANCTIONED: 0,
  DISBURSED: 0,
  CLARIFICATION_REQUIRED: 3,
  REJECTED: 0,
  CANCELLED: 0,
};

export function calculateSLA(submittedAt: Date, totalAllowedDays: number = 7): SLACalculation {
  const now = new Date();
  const diffTime = Math.abs(now.getTime() - new Date(submittedAt).getTime());
  const elapsedDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  const remainingDays = Math.max(0, totalAllowedDays - elapsedDays);
  
  const percentageConsumed = totalAllowedDays > 0 ? (elapsedDays / totalAllowedDays) * 100 : 0;
  const isBreached = elapsedDays >= totalAllowedDays;
  
  let statusColor: 'GREEN' | 'AMBER' | 'RED' = 'GREEN';
  if (isBreached) {
    statusColor = 'RED';
  } else if (percentageConsumed >= 80) {
    statusColor = 'AMBER';
  }

  return {
    totalDays: totalAllowedDays,
    elapsedDays,
    remainingDays,
    isBreached,
    statusColor,
    percentageConsumed: Math.min(100, Math.round(percentageConsumed)),
  };
}

export function getStageName(stage: string): string {
  const stageMap: Record<string, string> = {
    DRAFT: 'Draft Application',
    SUBMITTED: 'Application Submitted',
    FARMER_VERIFICATION: 'Farmer Profile Verification',
    LAND_VERIFICATION: 'Land Record Verification (Bhoomi)',
    DOCUMENT_VERIFICATION: 'Document Verification',
    CREDIT_ASSESSMENT: 'Bank Credit Assessment',
    SANCTION_PENDING: 'Loan Sanction Pending',
    SANCTIONED: 'Loan Sanctioned',
    DISBURSED: 'Credit Disbursed',
    CLARIFICATION_REQUIRED: 'Clarification Required',
    REJECTED: 'Application Rejected',
    CANCELLED: 'Application Cancelled',
  };
  return stageMap[stage] || stage;
}
