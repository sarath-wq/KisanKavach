'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Header from '@/components/layout/Header';
import FarmerBottomNav from '@/components/layout/FarmerBottomNav';
import { FileText, Clock, AlertTriangle, CheckCircle2, Circle, Landmark, FileCheck, ArrowRight, ShieldAlert, RefreshCw } from 'lucide-react';

export default function KCCTrackingPage() {
  const [apps, setApps] = useState<any[]>([]);
  const [selectedApp, setSelectedApp] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/kcc/applications')
      .then((res) => res.json())
      .then((data) => {
        if (data.success && data.applications.length > 0) {
          setApps(data.applications);
          setSelectedApp(data.applications[0]);
        }
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

  const app = selectedApp;

  const timelineSteps = [
    { label: 'Application Submitted', stage: 'SUBMITTED' },
    { label: 'Farmer Profile Verification', stage: 'FARMER_VERIFICATION' },
    { label: 'Land Information (Bhoomi)', stage: 'LAND_VERIFICATION' },
    { label: 'Documents Verification', stage: 'DOCUMENT_VERIFICATION' },
    { label: 'Bank Credit Assessment', stage: 'CREDIT_ASSESSMENT' },
    { label: 'Sanction Decision', stage: 'SANCTION_PENDING' },
    { label: 'Disbursement', stage: 'DISBURSED' },
  ];

  const getStepStatus = (stepStage: string, currentStage: string) => {
    const order = ['SUBMITTED', 'FARMER_VERIFICATION', 'LAND_VERIFICATION', 'DOCUMENT_VERIFICATION', 'CREDIT_ASSESSMENT', 'SANCTION_PENDING', 'SANCTIONED', 'DISBURSED'];
    const currIndex = order.indexOf(currentStage);
    const stepIndex = order.indexOf(stepStage);

    if (stepIndex < currIndex) return 'COMPLETED';
    if (stepIndex === currIndex) return 'CURRENT';
    return 'PENDING';
  };

  return (
    <div className="min-h-screen bg-slate-50 pb-20 sm:pb-8">
      <Header />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-extrabold text-slate-900">KCC APPLICATION TRACKER</h1>
            <p className="text-xs text-slate-500">Real-time SLA velocity and bank processing accountability</p>
          </div>

          <Link
            href="/farmer/kcc/new"
            className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow transition-colors inline-flex items-center space-x-1.5"
          >
            <span>+ Apply For New KCC Loan</span>
          </Link>
        </div>

        {!app ? (
          <div className="bg-white rounded-2xl p-8 text-center border border-slate-200 shadow-sm space-y-4">
            <p className="text-slate-600 text-sm">No active KCC applications found.</p>
            <Link
              href="/farmer/kcc/new"
              className="px-5 py-2.5 bg-emerald-600 text-white font-bold text-sm rounded-xl inline-block"
            >
              Start KCC Application Wizard
            </Link>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Status Summary Banner */}
            <div className={`rounded-2xl p-6 border shadow-sm ${
              app.slaBreached
                ? 'bg-red-50 border-red-200 text-red-900'
                : app.status === 'SANCTIONED'
                ? 'bg-emerald-50 border-emerald-200 text-emerald-950'
                : 'bg-white border-slate-200 text-slate-900'
            }`}>
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Application Reference</span>
                  <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900">{app.applicationId}</h2>
                  <p className="text-xs text-slate-500">Submitted: {new Date(app.submittedAt).toLocaleDateString()}</p>
                </div>

                <div className="flex flex-col items-start sm:items-end">
                  <span className={`px-3 py-1 rounded-full text-xs font-extrabold ${
                    app.slaBreached ? 'bg-red-600 text-white animate-pulse' : 'bg-amber-100 text-amber-900 border border-amber-300'
                  }`}>
                    {app.slaBreached ? '🔴 SLA BREACHED' : `🟡 Status: ${app.status}`}
                  </span>
                  <span className="text-xs font-semibold text-slate-600 mt-1">
                    Responsible: {app.bankBranch?.branchName || 'Bank Branch'}
                  </span>
                </div>
              </div>

              {/* SLA KPI Metrics */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-4">
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                  <span className="text-[11px] font-medium text-slate-500">SLA Standard</span>
                  <p className="text-base font-extrabold text-slate-900">{app.slaDaysTotal} Working Days</p>
                </div>
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                  <span className="text-[11px] font-medium text-slate-500">Elapsed</span>
                  <p className={`text-base font-extrabold ${app.slaBreached ? 'text-red-600' : 'text-slate-900'}`}>
                    {app.slaDaysElapsed} Days
                  </p>
                </div>
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                  <span className="text-[11px] font-medium text-slate-500">Loan Amount</span>
                  <p className="text-base font-extrabold text-emerald-700">₹{app.loanAmountRequested?.toLocaleString()}</p>
                </div>
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                  <span className="text-[11px] font-medium text-slate-500">Stage SLA</span>
                  <p className="text-xs font-bold text-slate-800">{app.currentStage.replace(/_/g, ' ')}</p>
                </div>
              </div>

              {/* SLA Breach Warning & Grievance trigger */}
              {app.slaBreached && (
                <div className="mt-4 p-4 rounded-xl bg-red-100 border border-red-300 text-red-900 flex flex-col sm:flex-row items-center justify-between gap-3">
                  <div className="flex items-start space-x-3">
                    <ShieldAlert className="w-6 h-6 text-red-600 shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-extrabold text-sm">SLA BREACH DETECTED</h4>
                      <p className="text-xs text-red-800">This application has exceeded the expected 7 working days processing period.</p>
                    </div>
                  </div>
                  <Link
                    href="/farmer/grievances/new"
                    className="px-4 py-2 bg-red-700 hover:bg-red-800 text-white font-bold text-xs rounded-xl shadow whitespace-nowrap"
                  >
                    Raise Escalation Grievance
                  </Link>
                </div>
              )}
            </div>

            {/* Visual Timeline Stepper */}
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
              <h3 className="text-base font-bold text-slate-900">Application Stage Progress</h3>

              <div className="space-y-4">
                {timelineSteps.map((step, idx) => {
                  const status = getStepStatus(step.stage, app.currentStage);
                  return (
                    <div key={step.stage} className="flex items-start space-x-4">
                      <div className="flex flex-col items-center">
                        {status === 'COMPLETED' ? (
                          <div className="w-8 h-8 rounded-full bg-emerald-500 text-white flex items-center justify-center font-bold text-sm">
                            ✓
                          </div>
                        ) : status === 'CURRENT' ? (
                          <div className="w-8 h-8 rounded-full bg-amber-400 text-amber-950 flex items-center justify-center font-bold text-sm animate-bounce">
                            🟡
                          </div>
                        ) : (
                          <div className="w-8 h-8 rounded-full bg-slate-100 border border-slate-300 text-slate-400 flex items-center justify-center text-xs">
                            ○
                          </div>
                        )}
                        {idx < timelineSteps.length - 1 && (
                          <div className={`w-0.5 h-6 my-1 ${status === 'COMPLETED' ? 'bg-emerald-500' : 'bg-slate-200'}`} />
                        )}
                      </div>

                      <div className="pt-1">
                        <h4 className={`text-sm font-bold ${status === 'CURRENT' ? 'text-amber-900 font-extrabold' : status === 'COMPLETED' ? 'text-slate-900' : 'text-slate-400'}`}>
                          {step.label}
                        </h4>
                        <p className="text-xs text-slate-500">
                          {status === 'COMPLETED'
                            ? 'Verified & Approved'
                            : status === 'CURRENT'
                            ? `In progress at ${app.bankBranch?.branchName || 'Bank'}`
                            : 'Pending previous stage approval'}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Verified Documents List */}
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
              <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2">
                <FileCheck className="w-5 h-5 text-emerald-600" />
                <span>Uploaded Documents</span>
              </h3>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {app.documents?.map((doc: any) => (
                  <div key={doc.id} className="p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
                    <div>
                      <span className="font-bold text-slate-900 block">{doc.docType}</span>
                      <span className="text-slate-500 text-[10px]">{doc.docName}</span>
                    </div>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                      ✓ Verified
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>

      <FarmerBottomNav />
    </div>
  );
}
