'use client';

import { useState, useEffect, use } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/layout/Header';
import { CheckCircle2, XCircle, AlertCircle, FileText, Landmark, ShieldCheck, ArrowLeft, RefreshCw } from 'lucide-react';

export default function BankReviewDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const router = useRouter();
  const [app, setApp] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [remarks, setRemarks] = useState('');
  const [rejectionCategory, setRejectionCategory] = useState('Incomplete documentation');
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetch(`/api/kcc/applications/${resolvedParams.id}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.success) setApp(data.application);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [resolvedParams.id]);

  const handleAction = async (action: string) => {
    if (action === 'REJECT' && !showRejectModal) {
      setShowRejectModal(true);
      return;
    }

    setSubmitting(true);
    try {
      const res = await fetch(`/api/kcc/applications/${resolvedParams.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action,
          rejectionCategory: action === 'REJECT' ? rejectionCategory : undefined,
          remarks,
        }),
      });

      const data = await res.json();
      if (data.success) {
        setApp(data.application);
        setShowRejectModal(false);
        alert(`Application successfully updated with action: ${action}`);
      } else {
        alert(data.error || 'Failed to update application');
      }
      setSubmitting(false);
    } catch (err) {
      alert('Error updating application');
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <RefreshCw className="w-6 h-6 animate-spin text-blue-600" />
      </div>
    );
  }

  if (!app) {
    return <div className="p-8 text-center text-slate-500">Application not found.</div>;
  }

  return (
    <div className="min-h-screen bg-slate-100 font-sans pb-12">
      <Header />

      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        <button
          onClick={() => router.push('/bank')}
          className="inline-flex items-center space-x-1.5 text-xs font-bold text-slate-600 hover:text-slate-900"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Operations Queue</span>
        </button>

        {/* Top Header Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold text-slate-400 uppercase">KCC Loan Review</span>
              <span className={`px-2.5 py-0.5 rounded text-[10px] font-bold ${
                app.slaBreached ? 'bg-red-100 text-red-700' : 'bg-emerald-100 text-emerald-800'
              }`}>
                {app.slaBreached ? 'SLA BREACHED' : 'SLA Normal'}
              </span>
            </div>
            <h1 className="text-2xl font-extrabold text-slate-900 mt-1">{app.applicationId}</h1>
            <p className="text-xs text-slate-500">Submitted by {app.farmer?.name} ({app.farmer?.farmerIdCode})</p>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => handleAction('REQUEST_CLARIFICATION')}
              disabled={submitting}
              className="px-4 py-2.5 bg-purple-100 text-purple-900 hover:bg-purple-200 font-bold text-xs rounded-xl transition-colors"
            >
              Request Clarification
            </button>
            <button
              onClick={() => handleAction('REJECT')}
              disabled={submitting}
              className="px-4 py-2.5 bg-red-100 text-red-800 hover:bg-red-200 font-bold text-xs rounded-xl transition-colors"
            >
              Reject Application
            </button>
            <button
              onClick={() => handleAction('APPROVE_STAGE')}
              disabled={submitting}
              className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-extrabold text-xs rounded-xl shadow transition-colors"
            >
              Approve & Advance Stage
            </button>
          </div>
        </div>

        {/* Farmer & Application Details Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <h3 className="font-bold text-slate-900 text-base border-b border-slate-100 pb-3">Farmer & Farm Profile</h3>
            <div className="space-y-2 text-xs text-slate-600">
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span>Farmer Name:</span>
                <span className="font-bold text-slate-900">{app.farmer?.name}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span>Aadhaar:</span>
                <span className="font-bold text-slate-900">{app.farmer?.aadhaarMasked}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span>Location:</span>
                <span className="font-bold text-slate-900">{app.farmer?.village?.name}, {app.farmer?.district?.name}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span>Landholding:</span>
                <span className="font-bold text-emerald-700">{app.farmer?.landSizeAcres} Acres</span>
              </div>
              <div className="flex justify-between py-1">
                <span>FRUITS & Bhoomi Sandbox:</span>
                <span className="font-bold text-emerald-800">✓ Verified Records</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <h3 className="font-bold text-slate-900 text-base border-b border-slate-100 pb-3">Credit Request Details</h3>
            <div className="space-y-2 text-xs text-slate-600">
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span>Loan Amount Requested:</span>
                <span className="font-extrabold text-emerald-700 text-sm">₹{app.loanAmountRequested?.toLocaleString()}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span>Purpose:</span>
                <span className="font-bold text-slate-900">{app.purpose}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span>Current Stage:</span>
                <span className="font-bold text-slate-900">{app.currentStage?.replace(/_/g, ' ')}</span>
              </div>
              <div className="flex justify-between py-1">
                <span>Days Pending in SLA:</span>
                <span className="font-bold text-slate-900">{app.slaDaysElapsed} of {app.slaDaysTotal} Days</span>
              </div>
            </div>
          </div>
        </div>

        {/* Remarks Entry Box */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-3">
          <label className="block text-xs font-bold text-slate-700">Bank Official Remarks / Assessment Notes</label>
          <textarea
            rows={3}
            value={remarks}
            onChange={(e) => setRemarks(e.target.value)}
            placeholder="Enter officer notes or clarification details here..."
            className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-xs font-medium focus:ring-2 focus:ring-blue-500 outline-none"
          />
        </div>

        {/* Mandatory Rejection Modal */}
        {showRejectModal && (
          <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl space-y-4">
              <h3 className="text-lg font-bold text-slate-900">Mandatory Rejection Category</h3>
              <p className="text-xs text-slate-600">Select a structured rejection reason. Unexplained rejections are not permitted under KisanKavach governance rules.</p>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Reason Category</label>
                <select
                  value={rejectionCategory}
                  onChange={(e) => setRejectionCategory(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-xs font-bold focus:ring-2 focus:ring-red-500 outline-none"
                >
                  <option value="Incomplete documentation">Incomplete documentation</option>
                  <option value="Eligibility issue">Eligibility issue</option>
                  <option value="Credit assessment issue">Credit assessment issue</option>
                  <option value="Duplicate application">Duplicate application</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div className="flex items-center justify-end space-x-2 pt-2">
                <button
                  onClick={() => setShowRejectModal(false)}
                  className="px-4 py-2 bg-slate-100 text-slate-700 font-bold text-xs rounded-xl"
                >
                  Cancel
                </button>
                <button
                  onClick={() => handleAction('REJECT')}
                  disabled={submitting}
                  className="px-4 py-2 bg-red-600 text-white font-bold text-xs rounded-xl shadow"
                >
                  Confirm Rejection
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
