'use client';

import Header from '@/components/layout/Header';
import FarmerBottomNav from '@/components/layout/FarmerBottomNav';
import { Gift, CheckCircle2, AlertCircle, Info, ExternalLink } from 'lucide-react';

export default function BenefitsPage() {
  const benefits = [
    {
      name: 'PM-KISAN Samman Nidhi',
      provider: 'Central Government of India',
      status: 'Active',
      amount: '₹6,000 / year (₹2,000 x 3 installments)',
      lastPaid: '15 Jan 2026',
      eligibility: '✓ Eligible based on 3.5 acres land holding record',
      nextAction: '17th Installment expected April 2026',
    },
    {
      name: 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
      provider: 'Central & Karnataka State Govt',
      status: 'Active Policy',
      amount: 'Coverage sum ₹45,000 for Kharif Ragi',
      lastPaid: 'Premium Paid Aug 2025',
      eligibility: '✓ Active for Mysuru District Kharif 2026',
      nextAction: 'Policy Active — No action required',
    },
    {
      name: 'KCC Interest Subvention Scheme',
      provider: 'NABARD / Reserve Bank of India',
      status: 'Eligible',
      amount: '3% Prompt Repayment Incentive',
      lastPaid: 'Applied at sanction',
      eligibility: '✓ Automatically applied on KCC short-term credit',
      nextAction: 'Ensure prompt loan repayment before due date',
    },
    {
      name: 'Krishi Bhagya Scheme (Farm Ponds & Irrigation)',
      provider: 'Department of Agriculture, Govt of Karnataka',
      status: 'Potentially Eligible',
      amount: 'Up to 80% Subsidy for Farm Ponds & Pumpsets',
      lastPaid: 'Not applied yet',
      eligibility: '✓ Eligible based on rainfed land category in Nanjangud',
      nextAction: 'Click to apply through Raitha Samparka Kendra',
    },
  ];

  return (
    <div className="min-h-screen bg-slate-50 pb-20 sm:pb-8">
      <Header />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-2xl font-extrabold text-slate-900">BENEFITS KAVACH</h1>
            <span className="px-2 py-0.5 bg-emerald-100 text-emerald-800 text-[10px] font-bold rounded">
              Sandbox Integration
            </span>
          </div>
          <p className="text-xs text-slate-500">Discovered Government schemes tailored to your verified landholding</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {benefits.map((b) => (
            <div key={b.name} className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wide">{b.provider}</span>
                  <h2 className="font-bold text-slate-900 text-sm">{b.name}</h2>
                </div>
                <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                  b.status === 'Active' || b.status === 'Active Policy'
                    ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                    : 'bg-blue-100 text-blue-800 border border-blue-200'
                }`}>
                  {b.status}
                </span>
              </div>

              <div className="bg-slate-50 rounded-xl p-3 space-y-1 text-xs text-slate-600">
                <p><strong>Benefit Value:</strong> {b.amount}</p>
                <p><strong>Eligibility:</strong> <span className="text-emerald-700 font-semibold">{b.eligibility}</span></p>
                <p><strong>Status Info:</strong> {b.nextAction}</p>
              </div>
            </div>
          ))}
        </div>
      </main>

      <FarmerBottomNav />
    </div>
  );
}
