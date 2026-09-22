import React, { useState, useEffect } from 'react';
import { ShieldAlert, CheckCircle, Clock, AlertTriangle, Eye, ShieldCheck } from 'lucide-react';
import { Incident } from '../types';

export const IncidentHub: React.FC = () => {
  const [incidents, setIncidents] = useState<Incident[]>([
    {
      id: 'INC-7F89B2',
      session_id: 'CALL-8921A',
      risk_score: 88.5,
      risk_level: 'CRITICAL',
      status: 'OPEN',
      title: 'CRITICAL Risk Voice Impersonation Alert',
      description: 'Detected synthetic voice deepfake combined with executive impersonation and high-value wire transfer request.',
      action_taken: 'BLOCK_SESSION_IMMEDIATELY',
      created_at: new Date(Date.now() - 15 * 60000).toISOString()
    },
    {
      id: 'INC-4A21D9',
      session_id: 'CALL-5412B',
      risk_score: 78.0,
      risk_level: 'HIGH',
      status: 'UNDER_INVESTIGATION',
      title: 'High Risk Speaker Mismatch',
      description: 'Voice profile similarity dropped to 35% during high-privilege administrative request.',
      action_taken: 'HOLD_TRANSACTION_AND_VERIFY',
      created_at: new Date(Date.now() - 120 * 60000).toISOString()
    }
  ]);

  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(incidents[0]);

  useEffect(() => {
    fetch('/api/v1/incidents')
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setIncidents(data);
          setSelectedIncident(data[0]);
        }
      })
      .catch(() => {});
  }, []);

  const updateStatus = async (id: string, newStatus: string) => {
    try {
      await fetch(`/api/v1/incidents/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      });
      setIncidents((prev) =>
        prev.map((i) => (i.id === id ? { ...i, status: newStatus as any } : i))
      );
      if (selectedIncident && selectedIncident.id === id) {
        setSelectedIncident({ ...selectedIncident, status: newStatus as any });
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-2xl space-y-2">
        <h2 className="text-xl font-extrabold text-white">Security Incident Triage & Forensics</h2>
        <p className="text-xs text-slate-400">Review flagged impersonation alerts, inspect signal score breakdowns, and update incident resolution status.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Incident List */}
        <div className="space-y-3">
          {incidents.map((inc) => (
            <div
              key={inc.id}
              onClick={() => setSelectedIncident(inc)}
              className={`glass-panel p-4 rounded-xl cursor-pointer transition-all ${
                selectedIncident?.id === inc.id
                  ? 'border-cyan-500/50 bg-slate-900/90 shadow-lg shadow-cyan-500/10'
                  : 'hover:bg-slate-900/50'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs text-cyan-400 font-bold">{inc.id}</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                  inc.risk_level === 'CRITICAL' ? 'bg-red-500/20 text-red-400' : 'bg-amber-500/20 text-amber-400'
                }`}>
                  {inc.risk_level} ({inc.risk_score})
                </span>
              </div>
              <div className="text-xs font-bold text-slate-200 mt-2">{inc.title}</div>
              <div className="text-[11px] text-slate-500 mt-1">Status: {inc.status}</div>
            </div>
          ))}
        </div>

        {/* Detailed Forensic Inspector */}
        <div className="lg:col-span-2 glass-panel p-6 rounded-2xl space-y-6">
          {selectedIncident ? (
            <div className="space-y-6">
              
              <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                <div>
                  <span className="font-mono text-xs text-cyan-400">{selectedIncident.id}</span>
                  <h3 className="text-lg font-bold text-white">{selectedIncident.title}</h3>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => updateStatus(selectedIncident.id, 'RESOLVED')}
                    className="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition-all"
                  >
                    Mark Resolved
                  </button>
                  <button
                    onClick={() => updateStatus(selectedIncident.id, 'FALSE_POSITIVE')}
                    className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs transition-all"
                  >
                    False Positive
                  </button>
                </div>
              </div>

              <div className="space-y-3">
                <div className="text-xs font-semibold text-slate-300">Description & Summary</div>
                <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-900 text-xs text-slate-300">
                  {selectedIncident.description}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 text-xs">
                <div className="p-3 bg-slate-950 rounded-xl border border-slate-900">
                  <div className="text-slate-500">Action Enforced:</div>
                  <div className="font-mono text-cyan-400 font-bold mt-1">{selectedIncident.action_taken}</div>
                </div>
                <div className="p-3 bg-slate-950 rounded-xl border border-slate-900">
                  <div className="text-slate-500">Call Session ID:</div>
                  <div className="font-mono text-slate-300 font-bold mt-1">{selectedIncident.session_id}</div>
                </div>
              </div>

            </div>
          ) : (
            <div className="text-center py-12 text-slate-500 text-xs">Select an incident to view forensic details.</div>
          )}
        </div>

      </div>
    </div>
  );
};
