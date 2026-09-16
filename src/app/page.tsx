'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { Shield, FileText, Gift, AlertTriangle, ShieldCheck, ArrowRight, UserCheck, Lock, Building, Landmark, CheckCircle2, UserPlus } from 'lucide-react';
import Header from '@/components/layout/Header';

export default function LandingPage() {
  const router = useRouter();
  const [loadingRole, setLoadingRole] = useState<string | null>(null);
  const [error, setError] = useState('');

  const demoAccounts = [
    {
      role: 'Farmer Portal',
      email: 'farmer@demo.kisankavach.in',
      pass: 'demo123',
      badge: 'Farmer User',
      desc: 'View profile, 9-step KCC application wizard, benefits, insurance, grievances, AI assistant.',
      color: 'from-emerald-700 to-teal-800',
      target: '/farmer',
      icon: UserCheck,
    },
    {
      role: 'Bank Officer Portal',
      email: 'bank@demo.kisankavach.in',
      pass: 'demo123',
      badge: 'Bank Manager',
      desc: 'Application processing queue, SLA monitoring, document inspection, sanction & structured rejection workflow.',
      color: 'from-blue-600 to-indigo-700',
      target: '/bank',
      icon: Landmark,
    },
    {
      role: 'State Command Dashboard',
      email: 'gov@demo.kisankavach.in',
      pass: 'demo123',
      badge: 'Government Officer',
      desc: 'Statewide KPIs, district performance, bank velocity, SLA breaches, grievance & fraud monitoring, CSV export.',
      color: 'from-slate-800 to-slate-900',
      target: '/government',
      icon: Building,
    },
    {
      role: 'District Officer Portal',
      email: 'district@demo.kisankavach.in',
      pass: 'demo123',
      badge: 'District Collector',
      desc: 'Mysuru district & taluk level drilldown, overdue cases, local bank branch oversight & grievance assignment.',
      color: 'from-amber-600 to-orange-700',
      target: '/government',
      icon: Building,
    },
    {
      role: 'System Admin Console',
      email: 'admin@demo.kisankavach.in',
      pass: 'demo123',
      badge: 'System Admin',
      desc: 'User management, registration approvals queue, SLA threshold rules, audit logs & integration monitor.',
      color: 'from-purple-700 to-indigo-900',
      target: '/admin',
      icon: Lock,
    },
  ];

  const handleQuickLogin = async (email: string, pass: string, target: string, roleName: string) => {
    setLoadingRole(roleName);
    setError('');
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password: pass }),
      });
      const data = await res.json();
      if (data.success) {
        router.push(target);
      } else {
        setError(data.error || 'Failed to login');
        setLoadingRole(null);
      }
    } catch (err) {
      setError('Connection error');
      setLoadingRole(null);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Header />

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 via-emerald-950 to-slate-950 text-white py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto text-center relative z-10 flex flex-col items-center">
          
          {/* Logo Branding Display */}
          <div className="w-24 h-24 sm:w-28 sm:h-28 relative rounded-3xl overflow-hidden shadow-2xl border-2 border-emerald-500/40 bg-white p-2 mb-6">
            <Image
              src="/logo-shield.png"
              alt="KisanKavach Official Shield Logo"
              width={112}
              height={112}
              className="object-contain w-full h-full"
            />
          </div>

          <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-emerald-500/20 border border-emerald-400/30 text-emerald-300 text-xs font-bold uppercase tracking-wider mb-4">
            <Shield className="w-4 h-4 text-orange-400" />
            <span>Official Karnataka Pilot • kisan.digikavach.net</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-white mb-2 leading-tight">
            <span className="text-emerald-400">Kisan</span>
            <span className="text-orange-500">Kavach</span>
            <span className="text-slate-300 font-light ml-3">Karnataka</span>
          </h1>

          <p className="text-xs sm:text-sm font-black tracking-widest text-orange-400 uppercase mb-6">
            PROTECTING PROSPERITY
          </p>

          <p className="max-w-3xl mx-auto text-lg sm:text-xl text-emerald-100/90 font-light mb-8 leading-relaxed">
            One secure digital public infrastructure layer for farmer credit, benefits, crop insurance, grievances, and cyber-fraud protection.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 mb-10">
            <Link
              href="/register"
              className="px-6 py-3 bg-gradient-to-r from-orange-500 to-amber-600 hover:from-orange-600 hover:to-amber-700 text-slate-950 font-black text-xs rounded-xl shadow-lg inline-flex items-center space-x-2 transition-all hover:scale-105"
            >
              <UserPlus className="w-4 h-4" />
              <span>Self-Service User Registration</span>
            </Link>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/15 rounded-2xl p-4 sm:p-6 max-w-2xl mx-auto mb-6 text-left text-xs sm:text-sm text-slate-200">
            <div className="flex items-start space-x-3">
              <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
              <p>
                <strong className="text-white font-semibold">Architectural Principle:</strong> KisanKavach does <span className="underline decoration-orange-400 decoration-2">NOT</span> replace Karnataka's FRUITS or Bhoomi databases. It acts as an integration-ready orchestration, accountability, and protection layer on top of authorised state & banking systems.
              </p>
            </div>
          </div>

          {error && (
            <div className="mb-6 p-3 bg-red-500/20 border border-red-500/50 text-red-200 rounded-lg text-sm max-w-md mx-auto">
              {error}
            </div>
          )}
        </div>
      </section>

      {/* Role Quick-Login Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-10 relative z-20 pb-16">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-slate-900">Demonstration Journeys — One-Click Login</h2>
          <p className="text-slate-600 text-sm mt-1">Select a role below to experience the end-to-end platform workflows</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {demoAccounts.map((acc) => {
            const Icon = acc.icon;
            const isLoading = loadingRole === acc.role;
            return (
              <div
                key={acc.role}
                className="bg-white rounded-2xl border border-slate-200 shadow-xl shadow-slate-200/50 overflow-hidden flex flex-col justify-between hover:shadow-2xl transition-all hover:-translate-y-1"
              >
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-tr ${acc.color} text-white flex items-center justify-center shadow-md`}>
                      <Icon className="w-6 h-6" />
                    </div>
                    <span className="px-2.5 py-1 bg-slate-100 text-slate-700 text-xs font-bold rounded-md">
                      {acc.badge}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-slate-900 mb-2">{acc.role}</h3>
                  <p className="text-xs text-slate-600 leading-relaxed mb-4">{acc.desc}</p>

                  <div className="bg-slate-50 rounded-lg p-2.5 text-xs text-slate-500 space-y-1">
                    <div><span className="font-semibold text-slate-700">Email:</span> {acc.email}</div>
                    <div><span className="font-semibold text-slate-700">Password:</span> {acc.pass}</div>
                  </div>
                </div>

                <div className="p-6 pt-0">
                  <button
                    onClick={() => handleQuickLogin(acc.email, acc.pass, acc.target, acc.role)}
                    disabled={isLoading}
                    className={`w-full py-3 px-4 rounded-xl bg-gradient-to-r ${acc.color} text-white font-bold text-sm shadow-md hover:opacity-95 flex items-center justify-center space-x-2 transition-all disabled:opacity-50`}
                  >
                    <span>{isLoading ? 'Authenticating...' : `Launch ${acc.role}`}</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Feature Pillar Cards */}
      <section className="bg-white py-16 border-t border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-12">
            <h2 className="text-3xl font-extrabold text-slate-900">Five Pillars of KisanKavach</h2>
            <p className="text-slate-600 mt-2">Comprehensive protection and transparency for every Karnataka farmer</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
            <div className="p-6 rounded-2xl bg-emerald-50 border border-emerald-100">
              <div className="w-10 h-10 rounded-lg bg-emerald-600 text-white flex items-center justify-center mb-4">
                <FileText className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 text-base mb-1">CREDIT</h3>
              <p className="text-xs text-slate-600">Track KCC credit applications with visual SLA countdowns & breach escalation.</p>
            </div>

            <div className="p-6 rounded-2xl bg-blue-50 border border-blue-100">
              <div className="w-10 h-10 rounded-lg bg-blue-600 text-white flex items-center justify-center mb-4">
                <Gift className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 text-base mb-1">BENEFITS</h3>
              <p className="text-xs text-slate-600">Single discovery portal for PM-KISAN, PMFBY, and Karnataka subsidies.</p>
            </div>

            <div className="p-6 rounded-2xl bg-teal-50 border border-teal-100">
              <div className="w-10 h-10 rounded-lg bg-teal-600 text-white flex items-center justify-center mb-4">
                <Shield className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 text-base mb-1">INSURANCE</h3>
              <p className="text-xs text-slate-600">Monitor crop insurance policy status and live KSNDMC weather-risk advisories.</p>
            </div>

            <div className="p-6 rounded-2xl bg-amber-50 border border-amber-100">
              <div className="w-10 h-10 rounded-lg bg-amber-600 text-white flex items-center justify-center mb-4">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 text-base mb-1">GRIEVANCES</h3>
              <p className="text-xs text-slate-600">Raise complaints directly to District Collectors for bank or SLA delays.</p>
            </div>

            <div className="p-6 rounded-2xl bg-orange-50 border border-orange-100">
              <div className="w-10 h-10 rounded-lg bg-orange-600 text-white flex items-center justify-center mb-4">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 text-base mb-1">CYBER KAVACH</h3>
              <p className="text-xs text-slate-600">Verify suspicious SMS & links to prevent banking fraud and phishing scams.</p>
            </div>
          </div>
        </div>
      </section>

      <footer className="bg-slate-900 text-slate-400 text-xs py-8 px-4 text-center border-t border-slate-800 mt-auto">
        <p className="font-semibold text-slate-200">KisanKavach Karnataka Pilot Project • kisan.digikavach.net</p>
        <p className="mt-1">Designed for Karnataka Agriculture Department, Banks, and Farmer Organisations.</p>
      </footer>
    </div>
  );
}
