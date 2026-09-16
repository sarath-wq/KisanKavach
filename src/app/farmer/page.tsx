'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { ArrowRight, Shield, FileText, Gift, AlertTriangle, ShieldCheck, Clock, CheckCircle2, AlertCircle, RefreshCw } from 'lucide-react';
import Header from '@/components/layout/Header';
import FarmerBottomNav from '@/components/layout/FarmerBottomNav';

export default function FarmerHome() {
  const [farmerData, setFarmerData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('/api/farmers/me')
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setFarmerData(data.farmer);
        } else {
          setError(data.error || 'Failed to load profile');
        }
        setLoading(false);
      })
      .catch(() => {
        setError('Network connection error');
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="flex items-center space-x-3 text-emerald-700">
          <RefreshCw className="w-6 h-6 animate-spin" />
          <span className="font-bold text-sm">Loading KisanKavach Portal...</span>
        </div>
      </div>
    );
  }

  const latestApp = farmerData?.applications?.[0];
  const activeBenefitsCount = farmerData?.benefits?.length || 3;
  const activePoliciesCount = farmerData?.policies?.length || 1;

  return (
    <div className="min-h-screen bg-slate-50 pb-20 sm:pb-8">
      <Header />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        {/* Welcome Banner */}
        <div className="bg-gradient-to-br from-emerald-800 via-teal-900 to-slate-900 text-white rounded-3xl p-6 shadow-xl relative overflow-hidden">
          <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center space-x-2 bg-emerald-500/20 px-3 py-1 rounded-full text-emerald-300 text-xs font-semibold mb-2">
                <span>Farmer ID: {farmerData?.farmerIdCode || 'KK-KA-100245'}</span>
                <span>•</span>
                <span className="text-emerald-400">✓ Verified</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
                Namaskara, {farmerData?.name || 'Ramesh Gowda'} 👋
              </h1>
              <p className="text-xs sm:text-sm text-emerald-100/80 mt-1">
                {farmerData?.village?.name || 'Hullahalli'}, {farmerData?.taluk?.name || 'Nanjangud'}, {farmerData?.district?.name || 'Mysuru'} • {farmerData?.landSizeAcres || 3.5} acres
              </p>
            </div>

            <Link
              href="/farmer/kcc/new"
              className="inline-flex items-center justify-center px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-emerald-950 font-bold text-sm rounded-xl shadow-lg shadow-emerald-900/40 transition-all transform active:scale-95"
            >
              <span>Apply For KCC Loan</span>
              <ArrowRight className="w-4 h-4 ml-1.5" />
            </Link>
          </div>
        </div>

        {/* Primary KCC Status Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center border border-amber-200">
                <FileText className="w-5 h-5" />
              </div>
              <div>
                <h2 className="font-bold text-slate-900 text-base">KCC Application Status</h2>
                <p className="text-xs text-slate-500">ID: {latestApp?.applicationId || 'KK-KA-2026-000123'}</p>
              </div>
            </div>

            <span className={`px-3 py-1 rounded-full text-xs font-bold ${
              latestApp?.slaBreached ? 'bg-red-100 text-red-700 border border-red-200 animate-pulse' : 'bg-amber-100 text-amber-800 border border-amber-200'
            }`}>
              {latestApp?.slaBreached ? '🔴 SLA BREACHED' : '🟡 Processing'}
            </span>
          </div>

          <div className="bg-slate-50 rounded-xl p-4 border border-slate-100 space-y-3">
            <div className="flex items-center justify-between text-xs text-slate-600 font-medium">
              <span>Current Stage:</span>
              <span className="font-bold text-slate-900">{latestApp?.currentStage?.replace(/_/g, ' ') || 'Bank Credit Assessment'}</span>
            </div>
            <div className="flex items-center justify-between text-xs text-slate-600 font-medium">
              <span>Responsible Branch:</span>
              <span className="font-semibold text-emerald-800">{latestApp?.bankBranch?.branchName || 'Nanjangud Main Branch'}</span>
            </div>
            <div className="flex items-center justify-between text-xs text-slate-600 font-medium">
              <span>SLA Processing Period:</span>
              <span>{latestApp?.slaDaysElapsed || 3} of {latestApp?.slaDaysTotal || 7} working days elapsed</span>
            </div>

            {/* Stepper overview */}
            <div className="grid grid-cols-4 gap-1.5 pt-2">
              <div className="h-2 rounded-full bg-emerald-500" title="Submitted" />
              <div className="h-2 rounded-full bg-emerald-500" title="Farmer Verified" />
              <div className="h-2 rounded-full bg-amber-400" title="Credit Assessment" />
              <div className="h-2 rounded-full bg-slate-200" title="Sanction" />
            </div>
          </div>

          <div className="flex items-center justify-between pt-1">
            <Link
              href={latestApp ? `/farmer/kcc` : '/farmer/kcc/new'}
              className="text-xs font-bold text-emerald-700 hover:text-emerald-800 flex items-center space-x-1"
            >
              <span>Track Application Details</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>

            {latestApp?.slaBreached && (
              <Link
                href="/farmer/grievances/new"
                className="px-3 py-1.5 bg-red-600 text-white rounded-lg font-bold text-xs shadow-sm hover:bg-red-700"
              >
                Raise SLA Delay Grievance
              </Link>
            )}
          </div>
        </div>

        {/* Quick Access Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <Link
            href="/farmer/benefits"
            className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:border-emerald-300 transition-all group"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="w-9 h-9 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
                <Gift className="w-5 h-5" />
              </div>
              <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-blue-100 text-blue-800">
                {activeBenefitsCount} Active
              </span>
            </div>
            <h3 className="font-bold text-slate-900 text-sm group-hover:text-emerald-700">My Benefits</h3>
            <p className="text-xs text-slate-500 mt-1">PM-KISAN, PMFBY & Subsidies</p>
          </Link>

          <Link
            href="/farmer/insurance"
            className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:border-emerald-300 transition-all group"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="w-9 h-9 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center">
                <Shield className="w-5 h-5" />
              </div>
              <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-teal-100 text-teal-800">
                Active
              </span>
            </div>
            <h3 className="font-bold text-slate-900 text-sm group-hover:text-emerald-700">Crop Insurance</h3>
            <p className="text-xs text-slate-500 mt-1">Policy & KSNDMC Weather Alerts</p>
          </Link>

          <Link
            href="/farmer/fraud"
            className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:border-emerald-300 transition-all group"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="w-9 h-9 rounded-lg bg-sky-50 text-sky-600 flex items-center justify-center">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-100 text-emerald-800">
                Safe
              </span>
            </div>
            <h3 className="font-bold text-slate-900 text-sm group-hover:text-emerald-700">Cyber Kavach</h3>
            <p className="text-xs text-slate-500 mt-1">Check Phishing SMS & Links</p>
          </Link>
        </div>

        {/* AI Kisan Assistant Prompt */}
        <div className="bg-gradient-to-r from-teal-50 to-emerald-50 rounded-2xl p-5 border border-teal-200 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-slate-900 text-sm">Ask Kisan AI Assistant</span>
              <span className="px-2 py-0.5 bg-teal-200 text-teal-900 text-[10px] font-bold rounded">Kannada / English</span>
            </div>
            <p className="text-xs text-slate-600 mt-1">"Why is my KCC application pending?" or "What benefits am I eligible for?"</p>
          </div>
          <Link
            href="/farmer/ai"
            className="px-4 py-2 bg-teal-700 hover:bg-teal-800 text-white font-bold text-xs rounded-xl shadow transition-colors whitespace-nowrap"
          >
            Start Chat
          </Link>
        </div>
      </main>

      <FarmerBottomNav />
    </div>
  );
}
