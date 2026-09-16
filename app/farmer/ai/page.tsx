'use client';

import { useState } from 'react';
import Link from 'next/link';
import Header from '@/components/layout/Header';
import FarmerBottomNav from '@/components/layout/FarmerBottomNav';
import { Bot, User, Send, Sparkles, ArrowRight } from 'lucide-react';

interface ChatMessage {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  textKn?: string;
  actions?: { label: string; href: string }[];
}

export default function KisanAIPage() {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'ai',
      text: 'Namaskara! I am your KisanKavach AI Assistant. Ask me anything about your KCC application, eligible benefits, or crop insurance.',
      textKn: 'ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಕಿಸಾನ್‌ಕವಚ AI ಸಹಾಯಕ. ಸಾಲದ ಸ್ಥಿತಿ ಅಥವಾ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ಪ್ರಶ್ನೆ ಕೇಳಿ.',
    },
  ]);

  const suggestedQuestions = [
    'What is my KCC status?',
    'Why is my application pending?',
    'What benefits am I eligible for?',
    'How do I raise a complaint?',
    'Is my SMS message genuine?',
  ];

  const handleSend = async (questionText?: string) => {
    const query = questionText || input;
    if (!query.trim()) return;

    const userMsg: ChatMessage = {
      id: String(Date.now()),
      sender: 'user',
      text: query,
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: query }),
      });

      const data = await res.json();
      if (data.success) {
        const aiMsg: ChatMessage = {
          id: String(Date.now() + 1),
          sender: 'ai',
          text: data.response.answer,
          textKn: data.response.answerKn,
          actions: data.response.suggestedActions,
        };
        setMessages((prev) => [...prev, aiMsg]);
      }
      setLoading(false);
    } catch (err) {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 pb-20 sm:pb-8">
      <Header />

      <main className="max-w-3xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-2xl font-extrabold text-slate-900">KISAN AI ASSISTANT</h1>
              <span className="px-2 py-0.5 bg-teal-100 text-teal-800 text-[10px] font-bold rounded">
                Kannada / English
              </span>
            </div>
            <p className="text-xs text-slate-500">Authorized context assistant • Based on pilot sandbox data</p>
          </div>
        </div>

        {/* Suggested Prompt Chips */}
        <div className="flex flex-wrap gap-2">
          {suggestedQuestions.map((q) => (
            <button
              key={q}
              onClick={() => handleSend(q)}
              className="px-3 py-1.5 bg-white border border-slate-200 rounded-xl text-xs font-semibold text-slate-700 hover:border-teal-400 hover:bg-teal-50 transition-colors"
            >
              💬 {q}
            </button>
          ))}
        </div>

        {/* Chat Log Window */}
        <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm min-h-[380px] flex flex-col justify-between space-y-4">
          <div className="space-y-4 overflow-y-auto max-h-[420px] pr-2">
            {messages.map((m) => (
              <div
                key={m.id}
                className={`flex items-start space-x-3 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {m.sender === 'ai' && (
                  <div className="w-8 h-8 rounded-full bg-teal-600 text-white flex items-center justify-center font-bold text-xs shrink-0 mt-1">
                    <Bot className="w-4 h-4" />
                  </div>
                )}

                <div className={`p-4 rounded-2xl text-xs space-y-2 max-w-[85%] ${
                  m.sender === 'user'
                    ? 'bg-emerald-600 text-white font-medium rounded-tr-none'
                    : 'bg-slate-50 border border-slate-200 text-slate-900 rounded-tl-none'
                }`}>
                  <p className="leading-relaxed font-semibold">{m.text}</p>
                  {m.textKn && (
                    <p className="text-[11px] opacity-90 border-t border-slate-200/50 pt-1.5 font-medium text-emerald-950">
                      {m.textKn}
                    </p>
                  )}

                  {m.actions && m.actions.length > 0 && (
                    <div className="pt-2 flex flex-wrap gap-2">
                      {m.actions.map((act) => (
                        <Link
                          key={act.href}
                          href={act.href}
                          className="px-3 py-1.5 bg-teal-700 hover:bg-teal-800 text-white font-bold text-[11px] rounded-lg shadow-sm inline-flex items-center space-x-1"
                        >
                          <span>{act.label}</span>
                          <ArrowRight className="w-3 h-3" />
                        </Link>
                      ))}
                    </div>
                  )}
                </div>

                {m.sender === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-slate-800 text-white flex items-center justify-center font-bold text-xs shrink-0 mt-1">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex items-center space-x-2 text-xs text-slate-400 font-medium">
                <Sparkles className="w-4 h-4 animate-spin text-teal-600" />
                <span>Kisan AI is fetching authorized farmer context...</span>
              </div>
            )}
          </div>

          {/* Input Box */}
          <div className="pt-2 border-t border-slate-100 flex items-center space-x-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask a question in Kannada or English..."
              className="flex-1 px-4 py-3 rounded-xl border border-slate-300 text-xs font-bold focus:ring-2 focus:ring-teal-500 outline-none"
            />
            <button
              onClick={() => handleSend()}
              disabled={loading || !input.trim()}
              className="p-3 bg-teal-700 hover:bg-teal-800 text-white rounded-xl shadow transition-colors disabled:opacity-50"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      </main>

      <FarmerBottomNav />
    </div>
  );
}
