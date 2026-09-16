import { NextResponse } from 'next/server';
import { getSession } from '@/lib/auth/session';
import { askKisanAI } from '@/lib/ai/service';

export async function POST(request: Request) {
  try {
    const session = await getSession();
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await request.json();
    const { question } = body;

    if (!question || typeof question !== 'string') {
      return NextResponse.json({ error: 'Question text is required' }, { status: 400 });
    }

    const aiResponse = await askKisanAI(session.userId, question);
    return NextResponse.json({ success: true, response: aiResponse });
  } catch (error) {
    console.error('AI Chat API Error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
