'use client';

import Header from '@/components/layout/Header';
import FarmerBottomNav from '@/components/layout/FarmerBottomNav';
import { Shield, CloudRain, AlertTriangle, CheckCircle2 } from 'lucide-react';

export default function InsurancePage() {
  return (
    <div className="min-h-screen bg-slate-50 pb-20 sm:pb-8">
      <Header />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900">MY CROP INSURANCE & WEATHER KAVACH</h1>
          <p className="text-xs text-slate-500">Pradhan Mantri Fasal Bima Yojana (PMFBY) & KSNDMC Weather Alerts</p>
        </div>

        {/* Policy Details */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-teal-100 text-teal-800 flex items-center justify-center font-bold">
                <Shield className="w-5 h-5" />
              </div>
              <div>
                <h2 className="font-bold text-slate-900 text-base">PMFBY Crop Policy</h2>
                <p className="text-xs text-slate-500">Policy No: <span className="font-bold text-slate-800">KK-INS-2026-000123</span></p>
              </div>
            </div>
            <span className="px-3 py-1 bg-emerald-100 text-emerald-800 text-xs font-bold rounded-full border border-emerald-300">
              ✓ Policy Active
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 p-4 rounded-xl text-xs">
            <div>
              <span className="text-slate-500 block">Insured Crop</span>
              <span className="font-bold text-slate-900">Ragi & Paddy</span>
            </div>
            <div>
              <span className="text-slate-500 block">Season / Year</span>
              <span className="font-bold text-slate-900">Kharif 2026</span>
            </div>
            <div>
              <span className="text-slate-500 block">Sum Insured</span>
              <span className="font-bold text-emerald-700">₹45,000</span>
            </div>
            <div>
              <span className="text-slate-500 block">Claim Status</span>
              <span className="font-bold text-slate-900">No Active Claim</span>
            </div>
          </div>
        </div>

        {/* Weather Risk Warning */}
        <div className="bg-gradient-to-r from-amber-500/10 via-orange-500/10 to-amber-500/10 rounded-2xl border border-amber-300 p-5 space-y-3">
          <div className="flex items-center space-x-3 text-amber-900">
            <CloudRain className="w-6 h-6 text-amber-600 shrink-0" />
            <div>
              <h3 className="font-extrabold text-sm">KSNDMC WEATHER RISK ALERT — MYSURU DISTRICT</h3>
              <p className="text-xs text-amber-800">Simulated Weather Data • Last Updated: Today 08:30 AM</p>
            </div>
          </div>

          <div className="bg-white/80 rounded-xl p-4 text-xs text-slate-800 space-y-2 border border-amber-200">
            <p className="font-bold text-red-700">⚠️ Heavy Rainfall Risk Detected in Nanjangud Taluk</p>
            <p>KSNDMC forecasts 75mm heavy rainfall over the next 48 hours. Risk of localized waterlogging in harvested Ragi crops.</p>
            <div className="pt-2">
              <span className="font-bold text-slate-900 block mb-1">Recommended Farmer Action:</span>
              <ul className="list-disc list-inside space-y-1 text-slate-700">
                <li>Clear field drainage outlets for paddy plots immediately.</li>
                <li>Move harvested crop produce to elevated tarpaulin storage shelters.</li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      <FarmerBottomNav />
    </div>
  );
}
