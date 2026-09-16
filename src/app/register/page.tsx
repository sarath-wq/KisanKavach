'use client';

import { useState } from 'react';
import Link from 'next/link';
import Header from '@/components/layout/Header';
import { UserPlus, ShieldCheck, CheckCircle2, ArrowRight, ArrowLeft, RefreshCw, AlertCircle } from 'lucide-react';

export default function PublicRegistrationPage() {
  const [role, setRole] = useState('FARMER');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [mobile, setMobile] = useState('');
  const [district, setDistrict] = useState('Mysuru');
  const [bankBranch, setBankBranch] = useState('');
  const [idProof, setIdProof] = useState('');
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg('');

    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name,
          email,
          password,
          role,
          mobile,
          districtName: district,
          bankBranchName: bankBranch,
          idProofNumber: idProof,
        }),
      });

      const data = await res.json();
      if (data.success) {
        setSubmitted(true);
      } else {
        setErrorMsg(data.error || 'Registration failed. Please check your entries.');
      }
      setLoading(false);
    } catch (err) {
      setErrorMsg('Network error. Please try again.');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 font-sans pb-16 text-slate-100">
      <Header />

      <main className="max-w-2xl mx-auto px-4 py-10 space-y-6">
        <Link
          href="/"
          className="inline-flex items-center space-x-1.5 text-xs font-bold text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Home</span>
        </Link>

        {submitted ? (
          <div className="bg-slate-800 rounded-3xl border border-emerald-500/30 p-8 shadow-2xl text-center space-y-5">
            <div className="w-16 h-16 rounded-2xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 flex items-center justify-center mx-auto">
              <CheckCircle2 className="w-8 h-8" />
            </div>

            <div className="space-y-2">
              <h1 className="text-2xl font-extrabold text-white">Registration Submitted Successfully!</h1>
              <p className="text-xs text-slate-300 leading-relaxed max-w-md mx-auto">
                Your account registration request for <strong className="text-emerald-300">{name}</strong> ({role}) has been submitted to the <strong className="text-white">Karnataka e-Gov System Administrator</strong> for verification.
              </p>
            </div>

            <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-700/60 text-xs text-slate-400 text-left space-y-1">
              <div><strong className="text-slate-200">Email:</strong> {email}</div>
              <div><strong className="text-slate-200">Mobile:</strong> {mobile}</div>
              <div><strong className="text-slate-200">Account Status:</strong> <span className="text-amber-400 font-bold">PENDING_APPROVAL</span></div>
            </div>

            <p className="text-xs text-slate-400">
              You will receive an official notification once your profile is verified and approved.
            </p>

            <div className="pt-2">
              <Link
                href="/"
                className="px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg inline-block transition-all"
              >
                Return to Home Page
              </Link>
            </div>
          </div>
        ) : (
          <div className="bg-slate-800/90 rounded-3xl border border-slate-700/80 p-6 sm:p-8 shadow-2xl space-y-6">
            <div className="border-b border-slate-700 pb-4">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-400/30 text-emerald-300 text-[11px] font-bold uppercase tracking-wider mb-2">
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>Karnataka Digital Identity Portal</span>
              </div>
              <h1 className="text-2xl font-extrabold text-white">Account Registration & Access Request</h1>
              <p className="text-xs text-slate-400 mt-1">Submit your details for System Administrator verification and role clearance</p>
            </div>

            {errorMsg && (
              <div className="p-4 rounded-xl bg-red-950/60 border border-red-800 text-red-200 text-xs flex items-start space-x-2">
                <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
                <span>{errorMsg}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5 text-xs">
              <div>
                <label className="block font-bold text-slate-300 mb-1.5">Select Role Designation</label>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {[
                    { id: 'FARMER', label: '🌾 Farmer' },
                    { id: 'BANK_OFFICER', label: '🏦 Bank Officer' },
                    { id: 'DISTRICT_OFFICER', label: '📍 District Officer' },
                    { id: 'GOVT_OFFICER', label: '🏛️ Govt Officer' },
                  ].map((r) => (
                    <button
                      key={r.id}
                      type="button"
                      onClick={() => setRole(r.id)}
                      className={`py-2.5 px-3 rounded-xl font-bold border transition-all ${
                        role === r.id
                          ? 'bg-emerald-600 text-white border-emerald-400 shadow-md scale-105'
                          : 'bg-slate-900/60 text-slate-400 border-slate-700 hover:bg-slate-700/50'
                      }`}
                    >
                      {r.label}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block font-bold text-slate-300 mb-1">Full Legal Name</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Ramesh Gowda"
                  className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white font-medium outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block font-bold text-slate-300 mb-1">Email Address</label>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="e.g. ramesh@demo.kisankavach.in"
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white font-medium outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>

                <div>
                  <label className="block font-bold text-slate-300 mb-1">Mobile Number</label>
                  <input
                    type="text"
                    required
                    value={mobile}
                    onChange={(e) => setMobile(e.target.value)}
                    placeholder="98450XXXXX"
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white font-medium outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block font-bold text-slate-300 mb-1">Password</label>
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white font-medium outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>

                <div>
                  <label className="block font-bold text-slate-300 mb-1">District Geography</label>
                  <select
                    value={district}
                    onChange={(e) => setDistrict(e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white font-bold outline-none focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="Mysuru">Mysuru (ಮೈಸೂರು)</option>
                    <option value="Mandya">Mandya (ಮಂಡ್ಯ)</option>
                    <option value="Hassan">Hassan (ಹಾಸನ)</option>
                    <option value="Belagavi">Belagavi (ಬೆಳಗಾವಿ)</option>
                    <option value="Ballari">Ballari (ಬಳ್ಳಾರಿ)</option>
                    <option value="Kalaburagi">Kalaburagi (ಕಲಬುರಗಿ)</option>
                    <option value="Tumakuru">Tumakuru (ತುಮಕೂರು)</option>
                    <option value="Shivamogga">Shivamogga (ಶಿವಮೊಗ್ಗ)</option>
                  </select>
                </div>
              </div>

              {role === 'BANK_OFFICER' && (
                <div>
                  <label className="block font-bold text-slate-300 mb-1">Bank Branch Name & Employee ID</label>
                  <input
                    type="text"
                    value={bankBranch}
                    onChange={(e) => setBankBranch(e.target.value)}
                    placeholder="e.g. Karnataka Bank — Nanjangud Branch"
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white font-medium outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              )}

              <div>
                <label className="block font-bold text-slate-300 mb-1">Aadhaar / Employee ID Proof Reference</label>
                <input
                  type="text"
                  value={idProof}
                  onChange={(e) => setIdProof(e.target.value)}
                  placeholder="e.g. Aadhaar: XXXX-XXXX-9128 or Employee ID"
                  className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white font-medium outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>

              <div className="pt-2">
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-3.5 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm shadow-lg flex items-center justify-center space-x-2 transition-all disabled:opacity-50"
                >
                  {loading ? (
                    <RefreshCw className="w-4 h-4 animate-spin" />
                  ) : (
                    <>
                      <span>Submit Registration for Approval</span>
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        )}
      </main>
    </div>
  );
}
