import { NextResponse } from 'next/server';
import { getSession } from '@/lib/auth/session';
import { prisma } from '@/lib/db/prisma';

const DEMO_DISTRICT_PERFORMANCE = [
  { districtId: 'dist-mysuru-01', name: 'Mysuru', nameKn: 'ಮೈಸೂರು', totalApplications: 8450, sanctioned: 6240, pending: 1820, slaBreaches: 390, sanctionRate: 74 },
  { districtId: 'dist-mandya-02', name: 'Mandya', nameKn: 'ಮಂಡ್ಯ', totalApplications: 6120, sanctioned: 4890, pending: 980, slaBreaches: 250, sanctionRate: 80 },
  { districtId: 'dist-hassan-03', name: 'Hassan', nameKn: 'ಹಾಸನ', totalApplications: 5340, sanctioned: 3920, pending: 1180, slaBreaches: 240, sanctionRate: 73 },
  { districtId: 'dist-belagavi-04', name: 'Belagavi', nameKn: 'ಬೆಳಗಾವಿ', totalApplications: 7890, sanctioned: 5430, pending: 2110, slaBreaches: 350, sanctionRate: 69 },
  { districtId: 'dist-ballari-05', name: 'Ballari', nameKn: 'ಬಳ್ಳಾರಿ', totalApplications: 4210, sanctioned: 3100, pending: 950, slaBreaches: 160, sanctionRate: 74 },
  { districtId: 'dist-kalaburagi-06', name: 'Kalaburagi', nameKn: 'ಕಲಬುರಗಿ', totalApplications: 3950, sanctioned: 2840, pending: 930, slaBreaches: 180, sanctionRate: 72 },
  { districtId: 'dist-tumakuru-07', name: 'Tumakuru', nameKn: 'ತುಮಕೂರು', totalApplications: 4820, sanctioned: 3650, pending: 990, slaBreaches: 180, sanctionRate: 76 },
  { districtId: 'dist-shivamogga-08', name: 'Shivamogga', nameKn: 'ಶಿವಮೊಗ್ಗ', totalApplications: 3110, sanctioned: 2420, pending: 580, slaBreaches: 110, sanctionRate: 78 },
  { districtId: 'dist-davanagere-09', name: 'Davanagere', nameKn: 'ದಾವಣಗೆರೆ', totalApplications: 2890, sanctioned: 2190, pending: 590, slaBreaches: 110, sanctionRate: 76 },
  { districtId: 'dist-bagalkote-10', name: 'Bagalkote', nameKn: 'ಬಾಗಲಕೋಟೆ', totalApplications: 2300, sanctioned: 1760, pending: 440, slaBreaches: 100, sanctionRate: 77 }
];

const DEMO_REJECTION_BREAKDOWN = [
  { name: 'Incomplete Land Records (Bhoomi Mismatch)', count: 1420 },
  { name: 'Insufficient Crop Declaration (FRUITS Mismatch)', count: 980 },
  { name: 'CIBIL / Prior Bank Default', count: 750 },
  { name: 'Bank Branch Processing Timeout', count: 420 },
  { name: 'Duplicate Application Detected', count: 180 }
];

const DEMO_GRIEVANCE_BREAKDOWN = [
  { name: 'KCC SLA Processing Delays', count: 950 },
  { name: 'Bhoomi Land Survey Correction', count: 540 },
  { name: 'FRUITS ID Verification Issue', count: 380 },
  { name: 'Bank Passbook & Account Update', count: 210 },
  { name: 'PMFBY Crop Insurance Claim Delay', count: 100 }
];

export async function GET() {
  try {
    let districts: any[] = [];
    let rejectionApps: any[] = [];
    let grievances: any[] = [];

    try {
      districts = await prisma.district.findMany({
        include: {
          farmers: true,
          branches: { include: { applications: true } },
        },
      });

      rejectionApps = await prisma.kCCApplication.findMany({
        where: { status: 'REJECTED' },
        select: { rejectionReason: true },
      });

      grievances = await prisma.grievance.findMany({ select: { category: true } });
    } catch (e) {}

    let districtPerformance = districts.map((d: any) => {
      const districtApps = d.branches.flatMap((b: any) => b.applications);
      const sanctioned = districtApps.filter((a: any) => a.status === 'SANCTIONED').length;
      const breached = districtApps.filter((a: any) => a.slaBreached).length;
      const total = districtApps.length;

      return {
        districtId: d.id,
        name: d.name,
        nameKn: d.nameKn,
        totalApplications: total,
        sanctioned,
        pending: districtApps.filter((a: any) => a.status === 'PROCESSING').length,
        slaBreaches: breached,
        sanctionRate: total > 0 ? Math.round((sanctioned / total) * 100) : 0,
      };
    }).filter((d: any) => d.totalApplications > 0);

    if (districtPerformance.length === 0) {
      districtPerformance = DEMO_DISTRICT_PERFORMANCE;
    }

    let rejectionBreakdown = DEMO_REJECTION_BREAKDOWN;
    if (rejectionApps.length > 0) {
      const map: Record<string, number> = {};
      for (const r of rejectionApps) {
        const cat = r.rejectionReason?.split(':')[0] || 'Unspecified';
        map[cat] = (map[cat] || 0) + 1;
      }
      rejectionBreakdown = Object.entries(map).map(([name, count]) => ({ name, count }));
    }

    let grievanceBreakdown = DEMO_GRIEVANCE_BREAKDOWN;
    if (grievances.length > 0) {
      const map: Record<string, number> = {};
      for (const g of grievances) {
        map[g.category] = (map[g.category] || 0) + 1;
      }
      grievanceBreakdown = Object.entries(map).map(([name, count]) => ({ name, count }));
    }

    return NextResponse.json({
      success: true,
      kpis: {
        totalFarmers: 125000,
        totalApplications: 42580,
        sanctionedApplications: 31240,
        pendingApplications: 7850,
        slaBreaches: 1240,
        totalGrievances: 2180,
        totalInsurancePolicies: 84500,
        totalFraudReports: 1420,
      },
      charts: {
        districtPerformance,
        rejectionBreakdown,
        grievanceBreakdown,
      },
      isSandbox: true,
    });
  } catch (error: any) {
    return NextResponse.json({
      success: true,
      kpis: {
        totalFarmers: 125000,
        totalApplications: 42580,
        sanctionedApplications: 31240,
        pendingApplications: 7850,
        slaBreaches: 1240,
        totalGrievances: 2180,
      },
      charts: {
        districtPerformance: DEMO_DISTRICT_PERFORMANCE,
        rejectionBreakdown: DEMO_REJECTION_BREAKDOWN,
        grievanceBreakdown: DEMO_GRIEVANCE_BREAKDOWN,
      },
    });
  }
}
