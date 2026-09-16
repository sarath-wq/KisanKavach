'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/layout/Header';
import FarmerBottomNav from '@/components/layout/FarmerBottomNav';
import { CheckCircle2, ArrowRight, ArrowLeft, Upload, ShieldCheck, Landmark, FileText, Check } from 'lucide-react';

export default function KCCWizardPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [farmer, setFarmer] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  // Form State
  const [loanAmount, setLoanAmount] = useState('120000');
  const [purpose, setPurpose] = useState('Kharif Ragi & Paddy Cultivation');
  const [selectedBankBranch, setSelectedBankBranch] = useState('');
  const [consentGranted, setConsentGranted] = useState(true);

  useEffect(() => {
    fetch('/api/farmers/me')
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setFarmer(data.farmer);
        }
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      const res = await fetch('/api/kcc/applications', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          loanAmountRequested: loanAmount,
          purpose,
          bankBranchId: selectedBankBranch || undefined,
        }),
      });

      const data = await res.json();
      if (data.success) {
        router.push('/farmer/kcc');
      } else {
        alert(data.error || 'Failed to submit application');
        setSubmitting(false);
      }
    } catch (err) {
      alert('Error connecting to server');
      setSubmitting(false);
    }
  };

  const stepsList = [
    'Farmer Details',
    'Land Information',
    'Crop Details',
    'Credit Requirement',
    'Bank Selection',
    'Document Upload',
    'Consent',
    'Review',
    'Submit',
  ];

  return (
    <div className="min-h-screen bg-slate-50 pb-20 sm:pb-8">
      <Header />

      <main className="max-w-3xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900">KCC CREDIT APPLICATION WIZARD</h1>
          <p className="text-xs text-slate-500">Step {step} of 9 — Standardized Karnataka Pilot Loan Form</p>
        </div>

        {/* Visual Stepper */}
        <div className="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm overflow-x-auto">
          <div className="flex items-center space-x-2 min-w-max">
            {stepsList.map((s, idx) => {
              const stepNum = idx + 1;
              const isDone = stepNum < step;
              const isCurrent = stepNum === step;
              return (
                <div key={s} className="flex items-center space-x-2">
                  <div
                    className={`w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs ${
                      isDone
                        ? 'bg-emerald-600 text-white'
                        : isCurrent
                        ? 'bg-emerald-500 text-white font-extrabold ring-4 ring-emerald-100'
                        : 'bg-slate-100 text-slate-400'
                    }`}
                  >
                    {isDone ? '✓' : stepNum}
                  </div>
                  <span className={`text-xs ${isCurrent ? 'font-bold text-slate-900' : 'text-slate-500'}`}>
                    {s}
                  </span>
                  {idx < stepsList.length - 1 && <span className="text-slate-300">›</span>}
                </div>
              );
            })}
          </div>
        </div>

        {/* Step Cards */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
          {step === 1 && (
            <div className="space-y-4">
              <h2 className="text-lg font-bold text-slate-900">Step 1: Farmer Information (FRUITS Mapped)</h2>
              <div className="bg-slate-50 p-4 rounded-xl space-y-2 text-xs text-slate-700">
                <p><strong>Name:</strong> {farmer?.name || 'Ramesh Gowda'}</p>
                <p><strong>Farmer ID:</strong> {farmer?.farmerIdCode || 'KK-KA-100245'}</p>
                <p><strong>Aadhaar:</strong> {farmer?.aadhaarMasked || 'XXXX-XXXX-4821'}</p>
                <p><strong>District / Taluk:</strong> {farmer?.district?.name || 'Mysuru'} / {farmer?.taluk?.name || 'Nanjangud'}</p>
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-4">
              <h2 className="text-lg font-bold text-slate-900">Step 2: Land Records (Bhoomi RTC Mapped)</h2>
              <div className="bg-slate-50 p-4 rounded-xl space-y-2 text-xs text-slate-700">
                <p><strong>Total Extent:</strong> {farmer?.landSizeAcres || 3.5} Acres</p>
                <p><strong>Survey Numbers:</strong> 142/1A (2.0 acres), 142/2B (1.5 acres)</p>
                <p><strong>Soil Type:</strong> Red Loamy & Black Cotton</p>
                <p className="text-emerald-700 font-bold">✓ Land records verified with Bhoomi Sandbox API</p>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="space-y-4">
              <h2 className="text-lg font-bold text-slate-900">Step 3: Crop Details</h2>
              <div className="space-y-3">
                <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-100 flex justify-between items-center text-xs">
                  <div>
                    <span className="font-bold text-slate-900">Ragi (Finger Millet)</span>
                    <span className="text-slate-500 block">Kharif 2026 • 2.0 Acres</span>
                  </div>
                  <span className="font-bold text-emerald-800">24 Quintals</span>
                </div>
                <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-100 flex justify-between items-center text-xs">
                  <div>
                    <span className="font-bold text-slate-900">Paddy (Rice)</span>
                    <span className="text-slate-500 block">Kharif 2026 • 1.5 Acres</span>
                  </div>
                  <span className="font-bold text-emerald-800">30 Quintals</span>
                </div>
              </div>
            </div>
          )}

          {step === 4 && (
            <div className="space-y-4">
              <h2 className="text-lg font-bold text-slate-900">Step 4: Credit Requirement</h2>
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Requested KCC Loan Amount (₹)</label>
                <input
                  type="number"
                  value={loanAmount}
                  onChange={(e) => setLoanAmount(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm font-bold focus:ring-2 focus:ring-emerald-500 outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Loan Purpose</label>
                <input
                  type="text"
                  value={purpose}
                  onChange={(e) => setPurpose(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm font-bold focus:ring-2 focus:ring-emerald-500 outline-none"
                />
              </div>
            </div>
          )}

          {step === 5 && (
            <div className="space-y-4">
              <h2 className="text-lg font-bold text-slate-900">Step 5: Bank Selection</h2>
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2 text-xs">
                <span className="font-bold text-slate-900">Karnataka Bank — Nanjangud Main Branch (IFSC: KARB0000412)</span>
                <p className="text-slate-500">Default assigned branch based on farmer land location & village mapping.</p>
              </div>
            </div>
          )}

          {step === 6 && (
            <div className="space-y-4">
              <h2 className="text-lg font-bold text-slate-900">Step 6: Document Verification</h2>
              <div className="space-y-2 text-xs">
                <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200 flex justify-between items-center">
                  <span>Aadhaar Card (Masked)</span>
                  <span className="text-emerald-700 font-bold">✓ Attached & Verified</span>
                </div>
                <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200 flex justify-between items-center">
                  <span>Bhoomi RTC Pahani Record</span>
                  <span className="text-emerald-700 font-bold">✓ Attached & Verified</span>
                </div>
                <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200 flex justify-between items-center">
                  <span>Bank Passbook Copy</span>
                  <span className="text-emerald-700 font-bold">✓ Attached & Verified</span>
                </div>
              </div>
            </div>
          )}

          {step === 7 && (
            <div className="space-y-4">
              <h2 className="text-lg font-bold text-slate-900">Step 7: Data Access Consent</h2>
              <div className="p-4 bg-amber-50 rounded-xl border border-amber-200 space-y-3 text-xs text-amber-900">
                <p className="font-bold">DATA ACCESS CONSENT</p>
                <p>KisanKavach requests permission to access your verified FRUITS farmer profile, Bhoomi land records, and Credit Bureau assessment for KCC loan processing.</p>
                <label className="flex items-center space-x-2 font-bold cursor-pointer pt-2">
                  <input
                    type="checkbox"
                    checked={consentGranted}
                    onChange={(e) => setConsentGranted(e.target.checked)}
                    className="w-4 h-4 text-emerald-600 rounded"
                  />
                  <span>I grant explicit consent to KisanKavach & Karnataka Bank</span>
                </label>
              </div>
            </div>
          )}

          {step === 8 && (
            <div className="space-y-4">
              <h2 className="text-lg font-bold text-slate-900">Step 8: Review Application</h2>
              <div className="bg-slate-50 p-4 rounded-xl space-y-2 text-xs text-slate-700">
                <p><strong>Farmer Name:</strong> {farmer?.name || 'Ramesh Gowda'}</p>
                <p><strong>Requested Amount:</strong> ₹{parseInt(loanAmount).toLocaleString()}</p>
                <p><strong>Purpose:</strong> {purpose}</p>
                <p><strong>Assigned Bank:</strong> Karnataka Bank Nanjangud Branch</p>
                <p><strong>Consent Status:</strong> {consentGranted ? '✓ Granted' : '❌ Denied'}</p>
              </div>
            </div>
          )}

          {step === 9 && (
            <div className="space-y-4 text-center py-4">
              <div className="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto">
                <CheckCircle2 className="w-10 h-10" />
              </div>
              <h2 className="text-xl font-bold text-slate-900">Ready to Submit Application</h2>
              <p className="text-xs text-slate-600">Upon submission, your application will generate a reference ID and trigger the 7 working days SLA tracking clock.</p>
            </div>
          )}

          {/* Stepper Control Buttons */}
          <div className="flex items-center justify-between pt-4 border-t border-slate-100">
            {step > 1 ? (
              <button
                onClick={() => setStep(step - 1)}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs rounded-xl"
              >
                Previous Step
              </button>
            ) : <div />}

            {step < 9 ? (
              <button
                onClick={() => setStep(step + 1)}
                className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow inline-flex items-center space-x-1.5"
              >
                <span>Next Step</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={submitting || !consentGranted}
                className="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-extrabold text-sm rounded-xl shadow-lg disabled:opacity-50"
              >
                {submitting ? 'Submitting...' : 'Submit Application Now'}
              </button>
            )}
          </div>
        </div>
      </main>

      <FarmerBottomNav />
    </div>
  );
}
