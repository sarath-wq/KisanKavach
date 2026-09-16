import { NextResponse } from 'next/server';
import { analyzeFraudRisk } from '@/lib/fraud/analyzer';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { text } = body;

    if (!text || typeof text !== 'string') {
      return NextResponse.json({ error: 'Text to analyze is required' }, { status: 400 });
    }

    const analysis = analyzeFraudRisk(text);
    return NextResponse.json({ success: true, analysis });
  } catch (error) {
    console.error('Fraud Check API Error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
