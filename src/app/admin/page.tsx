'use client';

import { useState, useEffect } from 'react';
import Header from '@/components/layout/Header';
import { Lock, Users, Clock, ShieldCheck, UserPlus, X, CheckCircle2, AlertTriangle, Building, Landmark, Trash2, Check, XCircle, RefreshCw } from 'lucide-react';

const INITIAL_USERS = [
  { id: 'usr-1', name: 'Ramesh Gowda', email: 'farmer@demo.kisankavach.in', role: 'FARMER', mobile: '9845012345', district: 'Mysuru', branch: 'N/A', status: 'ACTIVE' },
  { id: 'usr-2', name: 'Suresh Kumar', email: 'bank@demo.kisankavach.in', role: 'BANK_OFFICER', mobile: '9845098765', district: 'Mysuru', branch: 'Karnataka Bank — Nanjangud', status: 'ACTIVE' },
  { id: 'usr-3', name: 'Dr. Vijayalakshmi', email: 'gov@demo.kisankavach.in', role: 'GOVT_OFFICER', mobile: '9845011223', district: 'Statewide', branch: 'N/A', status: 'ACTIVE' },
  { id: 'usr-4', name: 'Anand Rao', email: 'district@demo.kisankavach.in', role: 'DISTRICT_OFFICER', mobile: '9845033445', district: 'Mysuru District', branch: 'N/A', status: 'ACTIVE' },
  { id: 'usr-5', name: 'Karnataka e-Gov Admin', email: 'admin@demo.kisankavach.in', role: 'ADMIN', mobile: '9845055667', district: 'Statewide', branch: 'N/A', status: 'ACTIVE' },
];

const INITIAL_SLA_RULES = [
  { id: 'sla-1', stage: 'Farmer Profile & Verification', days: 2, warningPct: 80 },
  { id: 'sla-2', stage: 'Bhoomi Land & FRUITS Data Check', days: 2, warningPct: 80 },
  { id: 'sla-3', stage: 'Bank Credit Assessment Stage', days: 5, warningPct: 85 },
  { id: 'sla-4', stage: 'Final Sanction & Disbursement', days: 3, warningPct: 90 },
];

const AUDIT_LOGS = [
  { time: '2026-09-15 15:30:00', event: 'USER_REGISTERED', user: 'mahesh.farmer@demo.kisankavach.in', role: 'FARMER', details: 'Registration request submitted (Status: PENDING_APPROVAL)' },
  { time: '2026-09-15 15:20:00', event: 'LOGIN', user: 'farmer@demo.kisankavach.in', role: 'FARMER', details: 'User authenticated successfully from IP 106.51.72.14' },
  { time: '2026-09-15 14:45:12', event: 'KCC_SUBMITTED', user: 'farmer@demo.kisankavach.in', role: 'FARMER', details: 'Application KK-KA-2026-000101 submitted for ₹2,50,000' },
  { time: '2026-09-15 14:40:30', event: 'STATUS_CHANGED', user: 'bank@demo.kisankavach.in', role: 'BANK_OFFICER', details: 'Moved KK-KA-2026-000101 stage to CREDIT_ASSESSMENT' },
  { time: '2026-09-15 14:30:15', event: 'FRAUD_DETECTED', user: 'CyberKavach Engine', role: 'SYSTEM', details: 'High-risk phishing URL flagged: http://kisan-loan-fake...' },
];

export default function AdminConsolePage() {
  const [activeTab, setActiveTab] = useState<'APPROVALS' | 'USERS' | 'SLA' | 'AUDIT'>('APPROVALS');
  const [users, setUsers] = useState(INITIAL_USERS);
  const [slaRules, setSlaRules] = useState(INITIAL_SLA_RULES);
  const [pendingApps, setPendingApps] = useState<any[]>([]);
  const [loadingApprovals, setLoadingApprovals] = useState(true);
  const [showAddUserModal, setShowAddUserModal] = useState(false);
  
  // Form State
  const [newName, setNewName] = useState('');
  const [newEmail, setNewEmail] = useState('');
  const [newRole, setNewRole] = useState('FARMER');
  const [newMobile, setNewMobile] = useState('');
  const [newDistrict, setNewDistrict] = useState('Mysuru');
  const [newBranch, setNewBranch] = useState('');

  useEffect(() => {
    fetch('/api/admin/approvals')
      .then((res) => res.json())
      .then((d) => {
        if (d.success) setPendingApps(d.pendingRegistrations || []);
        setLoadingApprovals(false);
      })
      .catch(() => setLoadingApprovals(false));
  }, []);

  const handleApprovalAction = async (id: string, action: 'APPROVE' | 'REJECT') => {
    try {
      const res = await fetch('/api/admin/approvals', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ registrationId: id, action }),
      });
      const data = await res.json();
      if (data.success) {
        setPendingApps(pendingApps.map(p => p.id === id ? { ...p, status: action === 'APPROVE' ? 'APPROVED' : 'REJECTED' } : p));
        alert(data.message);
      }
    } catch (e) {
      alert('Error updating registration approval status');
    }
  };

  const handleAddUser = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName || !newEmail) return;

    const newUser = {
      id: `usr-${Date.now()}`,
      name: newName,
      email: newEmail,
      role: newRole,
      mobile: newMobile || '9845099999',
      district: newDistrict,
      branch: newBranch || 'N/A',
      status: 'ACTIVE',
    };

    setUsers([newUser, ...users]);
    setShowAddUserModal(false);
    setNewName('');
    setNewEmail('');
    setNewMobile('');
    alert(`Successfully created account for ${newName} (${newRole})!`);
  };

  return (
    <div className="min-h-screen bg-slate-100 font-sans pb-12">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-extrabold text-slate-900">SYSTEM ADMINISTRATOR CONSOLE</h1>
            <p className="text-xs text-slate-500">Approve user registrations, configure SLA rules, and monitor system audit logs</p>
          </div>

          <div className="flex flex-wrap gap-2 bg-white p-1.5 rounded-xl border border-slate-200 shadow-sm">
            <button
              onClick={() => setActiveTab('APPROVALS')}
              className={`px-3.5 py-2 rounded-lg text-xs font-bold transition-all ${
                activeTab === 'APPROVALS' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Pending Registrations ({pendingApps.filter(p => p.status === 'PENDING_APPROVAL').length})
            </button>
            <button
              onClick={() => setActiveTab('USERS')}
              className={`px-3.5 py-2 rounded-lg text-xs font-bold transition-all ${
                activeTab === 'USERS' ? 'bg-slate-900 text-white shadow-md' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              User Directory ({users.length})
            </button>
            <button
              onClick={() => setActiveTab('SLA')}
              className={`px-3.5 py-2 rounded-lg text-xs font-bold transition-all ${
                activeTab === 'SLA' ? 'bg-slate-900 text-white shadow-md' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              SLA Rules Engine
            </button>
            <button
              onClick={() => setActiveTab('AUDIT')}
              className={`px-3.5 py-2 rounded-lg text-xs font-bold transition-all ${
                activeTab === 'AUDIT' ? 'bg-slate-900 text-white shadow-md' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Audit Logs
            </button>
          </div>
        </div>

        {/* Tab: Pending Registrations Approval Queue */}
        {activeTab === 'APPROVALS' && (
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
            <div className="border-b border-slate-100 pb-4">
              <h2 className="font-extrabold text-slate-900 text-lg">Self-Service Registration Approvals Queue</h2>
              <p className="text-xs text-slate-500">Verify registrant identity proof, requested role, and approve account activation</p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 uppercase tracking-wider text-[11px]">
                  <tr>
                    <th className="py-3 px-4">Applicant Name</th>
                    <th className="py-3 px-4">Email Address</th>
                    <th className="py-3 px-4">Requested Role</th>
                    <th className="py-3 px-4">Mobile Number</th>
                    <th className="py-3 px-4">District / Branch Scope</th>
                    <th className="py-3 px-4">ID Proof Reference</th>
                    <th className="py-3 px-4 text-right">Approval Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-medium text-slate-700">
                  {pendingApps.map((p) => (
                    <tr key={p.id} className="hover:bg-slate-50 transition-colors">
                      <td className="py-3.5 px-4 font-bold text-slate-900">{p.name}</td>
                      <td className="py-3.5 px-4 text-slate-600">{p.email}</td>
                      <td className="py-3.5 px-4">
                        <span className="px-2.5 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-900 border border-amber-200">
                          {p.role}
                        </span>
                      </td>
                      <td className="py-3.5 px-4">{p.mobile}</td>
                      <td className="py-3.5 px-4 text-slate-600">{p.district} {p.branch !== 'N/A' && `• ${p.branch}`}</td>
                      <td className="py-3.5 px-4 font-mono text-[11px] text-slate-500">{p.idProof}</td>
                      <td className="py-3.5 px-4 text-right">
                        {p.status === 'PENDING_APPROVAL' ? (
                          <div className="flex items-center justify-end space-x-2">
                            <button
                              onClick={() => handleApprovalAction(p.id, 'REJECT')}
                              className="px-3 py-1.5 bg-red-100 hover:bg-red-200 text-red-800 font-bold text-xs rounded-lg transition-colors inline-flex items-center space-x-1"
                            >
                              <XCircle className="w-3.5 h-3.5" />
                              <span>Reject</span>
                            </button>
                            <button
                              onClick={() => handleApprovalAction(p.id, 'APPROVE')}
                              className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-lg shadow transition-colors inline-flex items-center space-x-1"
                            >
                              <Check className="w-3.5 h-3.5" />
                              <span>Approve & Activate</span>
                            </button>
                          </div>
                        ) : (
                          <span className={`px-2.5 py-0.5 rounded text-[10px] font-bold ${
                            p.status === 'APPROVED' ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'
                          }`}>
                            {p.status}
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Tab 2: User Accounts & Roles */}
        {activeTab === 'USERS' && (
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-4">
              <div>
                <h2 className="font-extrabold text-slate-900 text-lg">System User Directory</h2>
                <p className="text-xs text-slate-500">Manage portal access, assign regional scopes & bank branch roles</p>
              </div>

              <button
                onClick={() => setShowAddUserModal(true)}
                className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow inline-flex items-center space-x-2 transition-all"
              >
                <UserPlus className="w-4 h-4" />
                <span>+ Create New User Account</span>
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 uppercase tracking-wider text-[11px]">
                  <tr>
                    <th className="py-3 px-4">User Profile Name</th>
                    <th className="py-3 px-4">Email Address</th>
                    <th className="py-3 px-4">Role Designation</th>
                    <th className="py-3 px-4">Mobile Number</th>
                    <th className="py-3 px-4">District / Branch Scope</th>
                    <th className="py-3 px-4 text-right">Account Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-medium text-slate-700">
                  {users.map((u) => (
                    <tr key={u.id} className="hover:bg-slate-50 transition-colors">
                      <td className="py-3.5 px-4 font-bold text-slate-900">{u.name}</td>
                      <td className="py-3.5 px-4 text-slate-600">{u.email}</td>
                      <td className="py-3.5 px-4">
                        <span className={`px-2.5 py-0.5 rounded text-[10px] font-bold ${
                          u.role === 'FARMER' ? 'bg-emerald-100 text-emerald-800' :
                          u.role === 'BANK_OFFICER' ? 'bg-blue-100 text-blue-800' :
                          u.role === 'GOVT_OFFICER' ? 'bg-slate-900 text-white' :
                          u.role === 'DISTRICT_OFFICER' ? 'bg-amber-100 text-amber-900' :
                          'bg-purple-100 text-purple-900'
                        }`}>
                          {u.role}
                        </span>
                      </td>
                      <td className="py-3.5 px-4">{u.mobile}</td>
                      <td className="py-3.5 px-4 text-slate-600">{u.district} {u.branch !== 'N/A' && `• ${u.branch}`}</td>
                      <td className="py-3.5 px-4 text-right">
                        <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                          {u.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Tab 3: SLA Rules Engine */}
        {activeTab === 'SLA' && (
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
            <div className="border-b border-slate-100 pb-4">
              <h2 className="font-extrabold text-slate-900 text-lg">Configurable SLA Working Days Rules Engine</h2>
              <p className="text-xs text-slate-500">Define maximum allowable processing timelines per application stage before triggering escalations</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {slaRules.map((rule) => (
                <div key={rule.id} className="p-5 bg-slate-50 rounded-2xl border border-slate-200 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-900 text-sm">{rule.stage}</span>
                    <span className="px-2 py-0.5 rounded bg-blue-100 text-blue-900 text-[10px] font-bold">
                      Warning: {rule.warningPct}%
                    </span>
                  </div>

                  <div className="flex items-center justify-between pt-2">
                    <span className="text-xs text-slate-500">Allowed Working Days:</span>
                    <div className="flex items-center space-x-2">
                      <input
                        type="number"
                        min={1}
                        max={14}
                        value={rule.days}
                        onChange={(e) => setSlaRules(slaRules.map(s => s.id === rule.id ? { ...s, days: parseInt(e.target.value) || 1 } : s))}
                        className="w-16 px-3 py-1.5 rounded-lg border border-slate-300 font-bold text-slate-900 text-xs text-center"
                      />
                      <span className="text-xs text-slate-600 font-semibold">Days</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tab 4: Audit Event Logs */}
        {activeTab === 'AUDIT' && (
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <div className="border-b border-slate-100 pb-4">
              <h2 className="font-extrabold text-slate-900 text-lg">System Audit Event Log Stream</h2>
              <p className="text-xs text-slate-500">Immutable record of security events, authentication attempts, status changes, and fraud flags</p>
            </div>

            <div className="bg-slate-950 text-emerald-400 p-5 rounded-2xl text-xs font-mono space-y-3 overflow-x-auto shadow-inner">
              {AUDIT_LOGS.map((log, idx) => (
                <div key={idx} className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800/80 pb-2.5 gap-2">
                  <div className="space-x-2">
                    <span className="text-slate-500">[{log.time}]</span>
                    <span className="text-emerald-300 font-bold">{log.event}:</span>
                    <span className="text-slate-200">{log.details}</span>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 shrink-0">
                    {log.user} ({log.role})
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Modal: Create New User Account */}
        {showAddUserModal && (
          <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl p-6 max-w-lg w-full shadow-2xl space-y-5">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <h3 className="text-lg font-extrabold text-slate-900">Create New System Account</h3>
                <button onClick={() => setShowAddUserModal(false)} className="text-slate-400 hover:text-slate-600">
                  <X className="w-5 h-5" />
                </button>
              </div>

              <form onSubmit={handleAddUser} className="space-y-4 text-xs">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Full Name</label>
                  <input
                    type="text"
                    required
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                    placeholder="e.g. Anand Gowda"
                    className="w-full px-3.5 py-2 rounded-xl border border-slate-300 font-medium text-slate-900 outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">Email Address</label>
                  <input
                    type="email"
                    required
                    value={newEmail}
                    onChange={(e) => setNewEmail(e.target.value)}
                    placeholder="e.g. anand@demo.kisankavach.in"
                    className="w-full px-3.5 py-2 rounded-xl border border-slate-300 font-medium text-slate-900 outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block font-bold text-slate-700 mb-1">System Role</label>
                    <select
                      value={newRole}
                      onChange={(e) => setNewRole(e.target.value)}
                      className="w-full px-3.5 py-2 rounded-xl border border-slate-300 font-bold text-slate-900 outline-none focus:ring-2 focus:ring-emerald-500"
                    >
                      <option value="FARMER">FARMER (Farmer Portal)</option>
                      <option value="BANK_OFFICER">BANK_OFFICER (Bank Manager)</option>
                      <option value="GOVT_OFFICER">GOVT_OFFICER (State Command)</option>
                      <option value="DISTRICT_OFFICER">DISTRICT_OFFICER (Collector)</option>
                      <option value="ADMIN">ADMIN (System Admin)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block font-bold text-slate-700 mb-1">Mobile Number</label>
                    <input
                      type="text"
                      value={newMobile}
                      onChange={(e) => setNewMobile(e.target.value)}
                      placeholder="98450XXXXX"
                      className="w-full px-3.5 py-2 rounded-xl border border-slate-300 font-medium text-slate-900 outline-none focus:ring-2 focus:ring-emerald-500"
                    />
                  </div>
                </div>

                <div className="flex items-center justify-end space-x-2 pt-3 border-t border-slate-100">
                  <button
                    type="button"
                    onClick={() => setShowAddUserModal(false)}
                    className="px-4 py-2 bg-slate-100 text-slate-700 font-bold text-xs rounded-xl"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow"
                  >
                    Save & Create Account
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
