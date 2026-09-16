import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db/prisma';

export async function GET() {
  try {
    const districtsCount = await prisma.district.count();
    const farmersCount = await prisma.farmer.count();
    const appsCount = await prisma.kCCApplication.count();

    return NextResponse.json({
      success: true,
      message: 'KisanKavach SQLite Database is active and seeded!',
      stats: {
        districts: districtsCount,
        farmers: farmersCount,
        applications: appsCount,
      },
    });
  } catch (error: any) {
    return NextResponse.json({
      success: false,
      error: error.message || 'Database check failed',
    }, { status: 500 });
  }
}
