'use client';

import { useEffect, useState } from 'react';
import Header from '@/components/layout/Header';
import FarmerBottomNav from '@/components/layout/FarmerBottomNav';
import { User, MapPin, FileCheck, ShieldCheck, Database, RefreshCw } from 'lucide-react';

export default function FarmerProfilePage() {
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/farmers/me')
      .then((res) => res.json())
      .then((data) => {
        if (data.success) setProfile(data.farmer);
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
            <h1 className="text-2xl font-extrabold text-slate-900">MY FARMER PROFILE</h1>
            <p className="text-xs text-slate-500">Verified digital record integrated with FRUITS & Bhoomi sandboxes</p>
          </div>
          <span className="px-3 py-1 bg-emerald-100 text-emerald-800 text-xs font-bold rounded-full border border-emerald-300">
            ✓ Aadhaar & Bhoomi Verified
          </span>
        </div>

        {/* Core Profile Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="flex items-center space-x-3 pb-3 border-b border-slate-100">
              <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold text-lg">
                <User className="w-6 h-6" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-slate-900">{profile?.name || 'Ramesh Gowda'}</h2>
                <p className="text-xs text-slate-500">Farmer ID: <span className="font-bold text-slate-800">{profile?.farmerIdCode || 'KK-KA-100245'}</span></p>
              </div>
            </div>

            <div className="space-y-2 text-xs text-slate-600">
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span className="font-medium text-slate-500">Mobile Number:</span>
                <span className="font-bold text-slate-800">+91 {profile?.mobile || '9845012345'}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span className="font-medium text-slate-500">Aadhaar Status:</span>
                <span className="font-bold text-emerald-700">{profile?.aadhaarMasked || 'XXXX-XXXX-4821'} (Verified)</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span className="font-medium text-slate-500">FRUITS Sandbox ID:</span>
                <span className="font-bold text-slate-800">{profile?.fruitsId || 'FRUITS-MYS-8821'}</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="font-medium text-slate-500">Bhoomi RTC Ref:</span>
                <span className="font-bold text-slate-800">{profile?.bhoomiId || 'BHOOMI-RTC-142-1A'}</span>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-center space-x-3 pb-3 border-b border-slate-100">
              <div className="w-12 h-12 rounded-xl bg-teal-100 text-teal-800 flex items-center justify-center">
                <MapPin className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900">Farm Location & Land</h3>
                <p className="text-xs text-slate-500">Karnataka Land Registry</p>
              </div>
            </div>

            <div className="space-y-2 text-xs text-slate-600">
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span className="font-medium text-slate-500">District:</span>
                <span className="font-bold text-slate-800">{profile?.district?.name || 'Mysuru'}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span className="font-medium text-slate-500">Taluk:</span>
                <span className="font-bold text-slate-800">{profile?.taluk?.name || 'Nanjangud'}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span className="font-medium text-slate-500">Village:</span>
                <span className="font-bold text-slate-800">{profile?.village?.name || 'Hullahalli'}</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="font-medium text-slate-500">Total Landholding:</span>
                <span className="font-bold text-emerald-700">{profile?.landSizeAcres || 3.5} acres</span>
              </div>
            </div>
          </div>
        </div>

        {/* Landholdings & Crops */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2">
            <Database className="w-5 h-5 text-emerald-600" />
            <span>Landholdings & Survey Parcels</span>
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {profile?.landHoldings?.map((lh: any) => (
              <div key={lh.id} className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs text-slate-900">Survey No: {lh.surveyNumberMasked}</span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800">
                    {lh.areaAcres} Acres
                  </span>
                </div>
                <div className="text-xs text-slate-600 space-y-1">
                  <p>Soil Type: <span className="font-medium">{lh.soilType}</span></p>
                  <p>Irrigation: <span className="font-medium">{lh.irrigationStatus}</span></p>
                  <div className="pt-1 flex flex-wrap gap-1">
                    {lh.crops?.map((c: any) => (
                      <span key={c.id} className="px-2 py-0.5 bg-white border border-slate-200 rounded text-[10px] font-bold text-emerald-800">
                        🌾 {c.cropName} ({c.season})
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )) || (
              <p className="text-xs text-slate-500">No landholdings mapped yet.</p>
            )}
          </div>
        </div>
      </main>

      <FarmerBottomNav />
    </div>
  );
}
