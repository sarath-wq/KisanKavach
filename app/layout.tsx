import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'KisanKavach Karnataka — Digital Farmer Platform',
  description: 'Digital Credit, Governance & Farmer Protection System for Karnataka',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-slate-50 text-slate-900">
        {children}
      </body>
    </html>
  );
}
