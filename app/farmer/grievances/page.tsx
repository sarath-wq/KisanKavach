'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Header from '@/components/layout/Header';
import FarmerBottomNav from '@/components/layout/FarmerBottomNav';
import { AlertTriangle, Plus, Clock, CheckCircle2, MessageSquare, RefreshCw } from 'lucide-react';

export default function GrievancesPage() {
  const [grievances, setGrievances] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/grievances')
      .then((res) => res.json())
      .then((data) => {
        if (data.success) setGrievances(data.grievances);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <RefreshCw className="w-6 h-6 animate-spin text-emerald-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 pb-20 sm:pb-8">
      <Header />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-extrabold text-slate-900">GRIEVANCE KAVACH</h1>
            <p className="text-xs text-slate-500">Official escalation queue monitored by District Collectorate</p>
          </div>

          <Link
            href="/farmer/grievances/new"
            className="px-4 py-2.5 bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs rounded-xl shadow inline-flex items-center space-x-1.5"
          >
            <Plus className="w-4 h-4" />
            <span>Raise New Grievance</span>
          </Link>
        </div>

        {grievances.length === 0 ? (
          <div className="bg-white rounded-2xl p-8 text-center border border-slate-200 shadow-sm space-y-4">
            <p className="text-slate-600 text-sm">No registered grievances found.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {grievances.map((g) => (
              <div key={g.id} className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700">
                        {g.category}
                      </span>
                      <span className="text-xs font-bold text-slate-900">{g.grievanceId}</span>
                    </div>
                    <h2 className="font-bold text-slate-900 text-base mt-1">{g.subject}</h2>
                  </div>

                  <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                    g.status === 'RESOLVED'
                      ? 'bg-emerald-100 text-emerald-800'
                      : 'bg-amber-100 text-amber-800 border border-amber-300'
                  }`}>
                    {g.status}
                  </span>
                </div>

                <p className="text-xs text-slate-600 leading-relaxed bg-slate-50 p-3 rounded-xl">
                  {g.description}
                </p>

                <div className="flex items-center justify-between text-[11px] text-slate-500 pt-1">
                  <span>Registered: {new Date(g.createdAt).toLocaleDateString()}</span>
                  <span className="font-bold text-slate-700">Assigned: District Collectorate Mysuru</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      <FarmerBottomNav />
    </div>
  );
}
