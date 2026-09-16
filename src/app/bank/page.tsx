'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Header from '@/components/layout/Header';
import { Landmark, FileText, AlertTriangle, CheckCircle2, Search, Filter, RefreshCw, ArrowRight } from 'lucide-react';

export default function BankQueuePage() {
  const [apps, setApps] = useState<any[]>([]);
  const [kpis, setKpis] = useState<any>(null);
  const [filterStage, setFilterStage] = useState('ALL');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/dashboard/bank')
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setKpis(data.kpis);
          setApps(data.applications || []);
        }
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <RefreshCw className="w-6 h-6 animate-spin text-blue-600" />
      </div>
    );
  }

  const filteredApps = apps.filter((a) => {
    if (filterStage === 'SLA_BREACH') return a.slaBreached;
    if (filterStage === 'NEW') return a.currentStage === 'SUBMITTED' || a.status === 'NEW';
    if (filterStage === 'PROCESSING') return a.status === 'PROCESSING' || a.currentStage === 'CREDIT_ASSESSMENT' || a.currentStage === 'SANCTIONED';
    if (filterStage === 'ACTION_REQUIRED') return a.status === 'ACTION_REQUIRED' || a.currentStage === 'DOCUMENT_CHECK';
    return true;
  });

  return (
    <div className="min-h-screen bg-slate-100 font-sans pb-12">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-2xl font-extrabold text-slate-900">BANK OPERATIONS QUEUE</h1>
              <span className="px-2.5 py-0.5 rounded text-xs font-bold bg-blue-100 text-blue-900">
                Karnataka Bank — Nanjangud Branch
              </span>
            </div>
            <p className="text-xs text-slate-500">Manage KCC credit reviews, document verifications, and SLA compliance</p>
          </div>
        </div>

        {/* Top KPI Queue Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-4">
          <button onClick={() => setFilterStage('ALL')} className="text-left bg-white p-4 rounded-2xl border border-slate-200 shadow-sm hover:border-blue-400 transition-colors">
            <span className="text-xs text-slate-500 font-medium">Total Queue</span>
            <p className="text-2xl font-extrabold text-slate-900 mt-1">{apps.length}</p>
          </button>
          <button onClick={() => setFilterStage('NEW')} className="text-left bg-white p-4 rounded-2xl border border-slate-200 shadow-sm hover:border-blue-400 transition-colors">
            <span className="text-xs text-slate-500 font-medium">New Received</span>
            <p className="text-2xl font-extrabold text-blue-600 mt-1">{apps.filter(a => a.currentStage === 'SUBMITTED').length || kpis?.newApplications || 2}</p>
          </button>
          <button onClick={() => setFilterStage('PROCESSING')} className="text-left bg-white p-4 rounded-2xl border border-slate-200 shadow-sm hover:border-amber-400 transition-colors">
            <span className="text-xs text-slate-500 font-medium">In Assessment</span>
            <p className="text-2xl font-extrabold text-amber-600 mt-1">{apps.filter(a => a.status === 'PROCESSING').length || kpis?.processingApplications || 4}</p>
          </button>
          <button onClick={() => setFilterStage('ACTION_REQUIRED')} className="text-left bg-white p-4 rounded-2xl border border-slate-200 shadow-sm hover:border-purple-400 transition-colors">
            <span className="text-xs text-slate-500 font-medium">Clarification Req</span>
            <p className="text-2xl font-extrabold text-purple-600 mt-1">{apps.filter(a => a.status === 'ACTION_REQUIRED').length || kpis?.clarificationApplications || 1}</p>
          </button>
          <button onClick={() => setFilterStage('SLA_BREACH')} className="text-left bg-white p-4 rounded-2xl border border-red-200 bg-red-50/50 shadow-sm hover:border-red-400 transition-colors">
            <span className="text-xs text-red-700 font-bold">SLA Breaches</span>
            <p className="text-2xl font-extrabold text-red-600 mt-1">{apps.filter(a => a.slaBreached).length || kpis?.slaBreaches || 2}</p>
          </button>
        </div>

        {/* Queue Filter Bar & Table */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden space-y-4 p-5">
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4">
            <div className="flex flex-wrap gap-2">
              {['ALL', 'NEW', 'PROCESSING', 'ACTION_REQUIRED', 'SLA_BREACH'].map((st) => (
                <button
                  key={st}
                  onClick={() => setFilterStage(st)}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                    filterStage === st
                      ? 'bg-blue-600 text-white shadow-md shadow-blue-200 scale-105'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {st.replace(/_/g, ' ')}
                </button>
              ))}
            </div>
            <span className="text-xs font-semibold text-slate-500">Showing {filteredApps.length} Applications</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 uppercase tracking-wider text-[11px]">
                <tr>
                  <th className="py-3 px-4">Application ID</th>
                  <th className="py-3 px-4">Farmer Name</th>
                  <th className="py-3 px-4">District / Taluk</th>
                  <th className="py-3 px-4">Amount Requested</th>
                  <th className="py-3 px-4">Current Stage</th>
                  <th className="py-3 px-4">SLA Status</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium text-slate-700">
                {filteredApps.length > 0 ? (
                  filteredApps.map((a) => (
                    <tr key={a.id} className="hover:bg-slate-50 transition-colors">
                      <td className="py-3.5 px-4 font-bold text-slate-900">{a.applicationId}</td>
                      <td className="py-3.5 px-4 font-semibold text-slate-900">{a.farmer?.name}</td>
                      <td className="py-3.5 px-4 text-slate-500">{a.farmer?.district?.name || 'Mysuru'} / {a.farmer?.taluk?.name || 'Nanjangud'}</td>
                      <td className="py-3.5 px-4 font-bold text-emerald-700">₹{a.loanAmountRequested?.toLocaleString()}</td>
                      <td className="py-3.5 px-4">
                        <span className="px-2.5 py-1 rounded-md text-[11px] font-bold bg-slate-100 text-slate-800 border border-slate-200">
                          {a.currentStage.replace(/_/g, ' ')}
                        </span>
                      </td>
                      <td className="py-3.5 px-4">
                        <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                          a.slaBreached ? 'bg-red-100 text-red-700 border border-red-200' : 'bg-emerald-100 text-emerald-800'
                        }`}>
                          {a.slaBreached ? '🔴 BREACHED (8/7 Days)' : `${a.slaDaysElapsed}/7 Days`}
                        </span>
                      </td>
                      <td className="py-3.5 px-4 text-right">
                        <Link
                          href={`/bank/${a.id}`}
                          className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-lg inline-flex items-center space-x-1.5 shadow-sm transition-all"
                        >
                          <span>Review</span>
                          <ArrowRight className="w-3.5 h-3.5" />
                        </Link>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={7} className="py-8 text-center text-slate-500 font-medium">
                      No applications currently match the selected filter stage.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
