'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, FileText, Gift, AlertTriangle, ShieldCheck, User, MessageSquare } from 'lucide-react';

export default function FarmerBottomNav() {
  const pathname = usePathname();

  const navItems = [
    { label: 'Home', href: '/farmer', icon: Home },
    { label: 'KCC', href: '/farmer/kcc', icon: FileText },
    { label: 'Benefits', href: '/farmer/benefits', icon: Gift },
    { label: 'Grievances', href: '/farmer/grievances', icon: AlertTriangle },
    { label: 'Kavach', href: '/farmer/fraud', icon: ShieldCheck },
    { label: 'AI Help', href: '/farmer/ai', icon: MessageSquare },
    { label: 'Profile', href: '/farmer/profile', icon: User },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200 z-40 py-2 px-2 shadow-lg sm:hidden">
      <div className="flex items-center justify-around">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href || (item.href !== '/farmer' && pathname.startsWith(item.href));
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-col items-center px-2 py-1 rounded-lg text-center transition-colors ${
                isActive ? 'text-emerald-700 font-bold bg-emerald-50' : 'text-slate-500 font-medium hover:text-slate-800'
              }`}
            >
              <Icon className={`w-5 h-5 mb-0.5 ${isActive ? 'text-emerald-700' : 'text-slate-400'}`} />
              <span className="text-[10px] tracking-tight">{item.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
