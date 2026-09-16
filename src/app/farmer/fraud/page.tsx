'use client';

import { useState } from 'react';
import Header from '@/components/layout/Header';
import FarmerBottomNav from '@/components/layout/FarmerBottomNav';
import { ShieldCheck, AlertTriangle, CheckCircle2, ShieldAlert, Sparkles, Send } from 'lucide-react';

export default function CyberKavachPage() {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState<any>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [reported, setReported] = useState(false);

  const sampleMessages = [
    { label: 'Sample 1: Fake KCC Approval Link', text: 'Your KCC is approved. Click http://bit.ly/kcc-claim-subsidy immediately to claim your subsidy.' },
    { label: 'Sample 2: OTP KYC Theft', text: 'Your bank KYC is pending. Please share OTP 4821 immediately to unlock your account.' },
    { label: 'Sample 3: Official Bank Branch Notice', text: 'Dear Ramesh Gowda, please visit Karnataka Bank Nanjangud branch to complete standard documentation.' },
  ];

  const handleAnalyze = async (textToUse?: string) => {
    const text = textToUse || inputText;
    if (!text.trim()) return;

    setAnalyzing(true);
    setResult(null);
    setReported(false);

    try {
      const res = await fetch('/api/fraud/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      if (data.success) {
        setResult(data.analysis);
      }
      setAnalyzing(false);
    } catch (err) {
      setAnalyzing(false);
    }
  };

  const handleReportFraud = async () => {
    if (!result) return;
    try {
      await fetch('/api/fraud/report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category: result.category,
          textAnalyzed: inputText,
          riskScore: result.riskScore,
          riskLevel: result.riskLevel,
        }),
      });
      setReported(true);
    } catch (err) {}
  };

  return (
    <div className="min-h-screen bg-slate-50 pb-20 sm:pb-8">
      <Header />

      <main className="max-w-3xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900">CYBER KAVACH — FRAUD CHECKER</h1>
          <p className="text-xs text-slate-500">Protecting farmers against phishing SMS, fake bank calls, and subsidy scams</p>
        </div>

        {/* Quick Demo Pre-fill Buttons */}
        <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm space-y-2">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wide">Test Demo Message Samples:</span>
          <div className="flex flex-wrap gap-2">
            {sampleMessages.map((sample) => (
              <button
                key={sample.label}
                onClick={() => {
                  setInputText(sample.text);
                  handleAnalyze(sample.text);
                }}
                className="px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold transition-colors text-left"
              >
                {sample.label}
              </button>
            ))}
          </div>
        </div>

        {/* Analysis Form */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">
              Paste SMS Text, WhatsApp Message, or Link
            </label>
            <textarea
              rows={4}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="e.g., 'Your KCC loan is approved. Click link to pay processing fee...'"
              className="w-full px-4 py-3 rounded-xl border border-slate-300 text-xs font-medium focus:ring-2 focus:ring-sky-500 outline-none"
            />
          </div>

          <button
            onClick={() => handleAnalyze()}
            disabled={analyzing || !inputText.trim()}
            className="w-full py-3 bg-sky-600 hover:bg-sky-700 text-white font-extrabold text-xs rounded-xl shadow inline-flex items-center justify-center space-x-2 transition-colors disabled:opacity-50"
          >
            <Sparkles className="w-4 h-4" />
            <span>{analyzing ? 'Analyzing Risk Patterns...' : 'Check Risk Level Now'}</span>
          </button>
        </div>

        {/* Results Presentation */}
        {result && (
          <div className={`rounded-2xl border p-6 shadow-lg space-y-4 ${
            result.riskLevel === 'HIGH' || result.riskLevel === 'CRITICAL'
              ? 'bg-red-50 border-red-300 text-red-950'
              : 'bg-emerald-50 border-emerald-300 text-emerald-950'
          }`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                {result.riskLevel === 'HIGH' ? (
                  <ShieldAlert className="w-8 h-8 text-red-600 shrink-0" />
                ) : (
                  <ShieldCheck className="w-8 h-8 text-emerald-600 shrink-0" />
                )}
                <div>
                  <h3 className="text-lg font-extrabold">{result.riskLevel === 'HIGH' ? result.reasons[0] : 'LOW RISK / SAFE MESSAGE'}</h3>
                  <p className="text-xs opacity-80">Category: {result.category} • Risk Score: {result.riskScore}/100</p>
                </div>
              </div>

              <span className={`px-3 py-1 rounded-full text-xs font-extrabold ${
                result.riskLevel === 'HIGH' ? 'bg-red-600 text-white animate-pulse' : 'bg-emerald-600 text-white'
              }`}>
                {result.riskLevel} RISK
              </span>
            </div>

            <div className="bg-white/80 p-4 rounded-xl space-y-2 border text-xs">
              <h4 className="font-bold text-slate-900">Recommendation:</h4>
              <p className="font-semibold text-slate-800">{result.recommendation}</p>
              <p className="font-semibold text-emerald-900 italic pt-1">{result.recommendationKn}</p>
            </div>

            {result.riskLevel === 'HIGH' && (
              <div className="pt-2 flex justify-end">
                <button
                  onClick={handleReportFraud}
                  disabled={reported}
                  className="px-4 py-2 bg-red-700 hover:bg-red-800 text-white font-bold text-xs rounded-xl shadow"
                >
                  {reported ? '✓ Reported to Cyber Cell' : 'Report This Message to Police Cyber Cell'}
                </button>
              </div>
            )}
          </div>
        )}
      </main>

      <FarmerBottomNav />
    </div>
  );
}
