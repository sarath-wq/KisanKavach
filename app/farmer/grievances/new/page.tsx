'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/layout/Header';
import FarmerBottomNav from '@/components/layout/FarmerBottomNav';
import { AlertTriangle, Send } from 'lucide-react';

export default function NewGrievancePage() {
  const router = useRouter();
  const [category, setCategory] = useState('KCC');
  const [subject, setSubject] = useState('SLA Delay in KCC Credit Assessment');
  const [description, setDescription] = useState('My application KK-KA-2026-000123 has exceeded the 7 working days processing period. Requesting district escalation.');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const res = await fetch('/api/grievances', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category, subject, description, priority: 'HIGH' }),
      });

      const data = await res.json();
      if (data.success) {
        router.push('/farmer/grievances');
      } else {
        alert(data.error || 'Failed to file grievance');
        setSubmitting(false);
      }
    } catch (err) {
      alert('Error connecting to server');
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 pb-20 sm:pb-8">
      <Header />

      <main className="max-w-2xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900">REGISTER NEW GRIEVANCE</h1>
          <p className="text-xs text-slate-500">Escalate loan delays, banking issues, or subsidy concerns</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-5">
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Grievance Category</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-xs font-bold focus:ring-2 focus:ring-amber-500 outline-none"
            >
              <option value="KCC">KCC Loan / Bank SLA Delay</option>
              <option value="BANK">Bank Branch Issue</option>
              <option value="INSURANCE">PMFBY Crop Insurance Claim</option>
              <option value="GOVT_BENEFIT">PM-KISAN / Subsidy Issue</option>
              <option value="FRAUD">Cyber Fraud / Suspicious Contact</option>
              <option value="OTHER">Other Issue</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Subject</label>
            <input
              type="text"
              required
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-xs font-bold focus:ring-2 focus:ring-amber-500 outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Detailed Description</label>
            <textarea
              rows={4}
              required
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-xs font-medium focus:ring-2 focus:ring-amber-500 outline-none"
            />
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="w-full py-3 bg-amber-600 hover:bg-amber-700 text-white font-extrabold text-xs rounded-xl shadow inline-flex items-center justify-center space-x-2 transition-colors disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
            <span>{submitting ? 'Registering Complaint...' : 'Submit Grievance To District Collectorate'}</span>
          </button>
        </form>
      </main>

      <FarmerBottomNav />
    </div>
  );
}
