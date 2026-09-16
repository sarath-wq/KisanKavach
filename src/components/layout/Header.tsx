'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Globe, LogOut } from 'lucide-react';
import en from '@/locales/en.json';
import kn from '@/locales/kn.json';

export default function Header() {
  const [lang, setLang] = useState<'en' | 'kn'>('en');
  const [session, setSession] = useState<any>(null);

  useEffect(() => {
    const savedLang = localStorage.getItem('kisankavach_lang') as 'en' | 'kn';
    if (savedLang) setLang(savedLang);

    fetch('/api/auth/me')
      .then((res) => res.json())
      .then((data) => {
        if (data.authenticated) setSession(data.user);
      })
      .catch(() => {});
  }, []);

  const toggleLang = () => {
    const nextLang = lang === 'en' ? 'kn' : 'en';
    setLang(nextLang);
    localStorage.setItem('kisankavach_lang', nextLang);
    window.dispatchEvent(new Event('kisankavach_lang_change'));
  };

  const handleLogout = async () => {
    await fetch('/api/auth/logout', { method: 'POST' });
    window.location.href = '/';
  };

  const t = lang === 'en' ? en : kn;

  return (
    <header className="bg-white border-b border-emerald-100 sticky top-0 z-50 shadow-sm">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-emerald-950 via-teal-900 to-slate-900 text-white text-xs py-1.5 px-4 flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center space-x-2">
          <span className="bg-orange-500 text-slate-950 px-2 py-0.5 rounded text-[10px] font-black tracking-wide uppercase shadow-sm">
            {t.app.sandboxBadge}
          </span>
          <span className="opacity-90">{t.app.pilotDisclaimer}</span>
        </div>
        <div className="flex items-center space-x-3 text-[11px] opacity-90">
          <span className="font-semibold text-emerald-300">kisan.digikavach.net</span>
          <span className="hidden sm:inline">|</span>
          <span className="hidden sm:inline">Govt of Karnataka Pilot Architecture</span>
        </div>
      </div>

      {/* Main Header */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5 flex items-center justify-between">
        <Link href="/" className="flex items-center space-x-3 group">
          <div className="w-11 h-11 relative rounded-xl overflow-hidden shadow-md border border-emerald-200 bg-white p-0.5 shrink-0 group-hover:scale-105 transition-transform">
            <Image
              src="/logo-shield.png"
              alt="KisanKavach Official Shield Logo"
              width={44}
              height={44}
              className="object-contain w-full h-full"
            />
          </div>
          <div>
            <div className="flex items-center space-x-1 font-black text-2xl tracking-tight leading-none">
              <span className="text-[#044E29]">Kisan</span>
              <span className="text-[#EA580C]">Kavach</span>
              <span className="text-xs font-bold text-slate-400 ml-1.5 hidden md:inline">Karnataka</span>
            </div>
            <p className="text-[10px] font-black tracking-widest text-[#044E29] uppercase mt-0.5">
              PROTECTING PROSPERITY
            </p>
          </div>
        </Link>

        <div className="flex items-center space-x-3">
          {/* Language Switcher */}
          <button
            onClick={toggleLang}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg border border-emerald-300 bg-emerald-50 hover:bg-emerald-100 text-emerald-950 font-bold text-xs transition-colors shadow-sm"
          >
            <Globe className="w-3.5 h-3.5 text-emerald-700" />
            <span>{lang === 'en' ? 'ಕನ್ನಡ' : 'English'}</span>
          </button>

          {/* User Session Info / Logout */}
          {session ? (
            <div className="flex items-center space-x-2 border-l border-slate-200 pl-3">
              <div className="hidden md:block text-right">
                <p className="text-xs font-bold text-slate-800">{session.name}</p>
                <span className="inline-block px-1.5 py-0.5 rounded text-[10px] font-bold bg-orange-100 text-orange-900">
                  {session.role}
                </span>
              </div>
              <button
                onClick={handleLogout}
                title="Logout"
                className="p-2 text-slate-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <Link
              href="/"
              className="px-4 py-1.5 bg-gradient-to-r from-emerald-700 to-emerald-800 hover:from-emerald-800 hover:to-emerald-900 text-white rounded-lg font-bold text-xs shadow-sm transition-all"
            >
              {t.nav.login}
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
