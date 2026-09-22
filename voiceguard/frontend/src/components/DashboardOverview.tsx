import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, 
  PhoneCall, 
  Activity, 
  Cpu, 
  TrendingUp, 
  ArrowRight, 
  CheckCircle2, 
  Lock, 
  Sliders,
  FileAudio,
  Radio,
  Workflow
} from 'lucide-react';
import { DashboardOverview as DashboardOverviewType } from '../types';

interface DashboardProps {
  onNavigate?: (tab: string) => void;
}

export const DashboardOverviewComponent: React.FC<DashboardProps> = ({ onNavigate }) => {
  const [data, setData] = useState<DashboardOverviewType>({
    total_calls_analyzed: 124,
    total_incidents_flagged: 14,
    active_calls_count: 3,
    synthetic_voices_detected: 8,
    avg_risk_score: 24.8,
    recent_incidents: [
      {
        id: 'INC-7F89B2',
        session_id: 'CALL-8921A',
        risk_score: 88.5,
        risk_level: 'CRITICAL',
        status: 'OPEN',
        title: 'CRITICAL Risk Voice Impersonation Alert',
        action_taken: 'BLOCK_SESSION_IMMEDIATELY',
        created_at: new Date(Date.now() - 15 * 60000).toISOString()
      },
      {
        id: 'INC-4A21D9',
        session_id: 'CALL-5412B',
        risk_score: 78.0,
        risk_level: 'HIGH',
        status: 'UNDER_INVESTIGATION',
        title: 'High Risk Executive Impersonation Attempt',
        action_taken: 'HOLD_TRANSACTION_AND_VERIFY',
        created_at: new Date(Date.now() - 120 * 60000).toISOString()
      }
    ],
    blockchain_hash_head: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
  });

  const [activeWorkflowTab, setActiveWorkflowTab] = useState('workflows');

  useEffect(() => {
    fetch('/api/v1/dashboard/overview')
      .then((res) => res.json())
      .then((resData) => {
        if (resData && resData.total_calls_analyzed !== undefined) {
          setData(resData);
        }
      })
      .catch(() => {});
  }, []);

  return (
    <div className="space-y-10 pb-12">
      
      {/* 1. RESEMBLE.AI HERO SECTION */}
      <section className="pt-6 pb-4">
        {/* Intro Tag */}
        <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-teal-50 border border-teal-200 text-teal-800 text-xs font-semibold font-mono mb-6">
          <span className="w-2 h-2 rounded-full bg-teal-500 animate-pulse"></span>
          <span>INTRODUCING REAL-TIME VOICE IMPERSONATION PREVENTION</span>
        </div>

        {/* Hero Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          <div className="lg:col-span-7">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-gray-900 tracking-tight leading-[1.1]">
              Deepfakes are everywhere. <br className="hidden sm:block"/>
              <span className="text-gray-900">VoiceGuard protects you.</span>
            </h1>
          </div>

          <div className="lg:col-span-5 space-y-6">
            <p className="text-gray-600 text-base leading-relaxed">
              Detect AI-generated synthetic voice clones, verify speaker identities, analyze conversation intent, and calculate dynamic risk in real-time. Make confident security decisions before sensitive actions occur.
            </p>

            <div className="flex flex-wrap items-center gap-3">
              <button 
                onClick={() => onNavigate && onNavigate('monitor')}
                className="resemble-pill px-6 py-3 text-sm flex items-center space-x-2 shadow-md hover:bg-gray-800"
              >
                <span>Try Live Detection</span>
                <ArrowRight className="w-4 h-4 text-teal-400" />
              </button>

              <button 
                onClick={() => onNavigate && onNavigate('analyzer')}
                className="px-6 py-3 rounded-full border border-gray-300 text-gray-700 hover:bg-gray-100 text-sm font-semibold transition-all"
              >
                Upload Audio File
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* 2. RESEMBLE.AI FEATURE TABS BANNER */}
      <section className="rounded-3xl bg-gradient-to-r from-slate-900 via-teal-950 to-slate-900 p-8 sm:p-10 text-white shadow-xl">
        <h2 className="text-2xl sm:text-3xl font-extrabold text-center tracking-tight mb-8">
          Detection models usable anywhere deepfakes happen.
        </h2>

        {/* Tab Buttons */}
        <div className="flex justify-center mb-8">
          <div className="inline-flex p-1.5 rounded-2xl bg-slate-800/80 border border-slate-700/80 backdrop-blur-md">
            <button
              onClick={() => setActiveWorkflowTab('workflows')}
              className={`flex items-center space-x-2 px-5 py-2.5 rounded-xl text-xs font-bold transition-all ${
                activeWorkflowTab === 'workflows'
                  ? 'bg-white text-gray-900 shadow-md'
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              <Workflow className="w-4 h-4" />
              <span>In existing workflows</span>
            </button>

            <button
              onClick={() => setActiveWorkflowTab('integrations')}
              className={`flex items-center space-x-2 px-5 py-2.5 rounded-xl text-xs font-bold transition-all ${
                activeWorkflowTab === 'integrations'
                  ? 'bg-white text-gray-900 shadow-md'
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              <Radio className="w-4 h-4" />
              <span>Via streaming WebSocket</span>
            </button>

            <button
              onClick={() => setActiveWorkflowTab('api')}
              className={`flex items-center space-x-2 px-5 py-2.5 rounded-xl text-xs font-bold transition-all ${
                activeWorkflowTab === 'api'
                  ? 'bg-white text-gray-900 shadow-md'
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              <Cpu className="w-4 h-4" />
              <span>&lt;/&gt; Via REST API</span>
            </button>
          </div>
        </div>

        {/* Tab Content Display */}
        <div className="bg-slate-950/80 rounded-2xl p-6 border border-slate-800 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="space-y-3 max-w-xl">
            <div className="inline-block px-2.5 py-1 rounded bg-teal-500/20 text-teal-300 text-xs font-mono font-semibold">
              {activeWorkflowTab === 'workflows' && 'Contact Center Fraud Prevention'}
              {activeWorkflowTab === 'integrations' && 'Live Inbound Call Gateway'}
              {activeWorkflowTab === 'api' && 'Developer & Enterprise REST API'}
            </div>
            <h3 className="text-xl font-bold text-white">
              {activeWorkflowTab === 'workflows' && 'Integrate directly into carrier & call infrastructure'}
              {activeWorkflowTab === 'integrations' && 'Process 16kHz audio chunks with <10ms latency'}
              {activeWorkflowTab === 'api' && 'Submit WAV/WebM audio payloads and receive multi-signal risk JSON'}
            </h3>
            <p className="text-slate-300 text-xs leading-relaxed">
              VoiceGuard monitors inbound audio streams, evaluates acoustic spectral anomalies, verifies speaker voiceprints against registered profiles, and triggers security isolation before sensitive transactions complete.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 font-mono text-xs text-teal-400 space-y-2 shrink-0 w-full md:w-auto">
            <div className="flex items-center justify-between space-x-4 text-[11px] text-slate-400">
              <span>SECURITY POSTURE</span>
              <span className="text-emerald-400">ONLINE</span>
            </div>
            <div className="text-white font-bold">Multi-Signal Evidence Fusion</div>
            <div className="text-[11px] text-slate-400">Hash Head: {data.blockchain_hash_head.substring(0, 16)}...</div>
          </div>
        </div>
      </section>

      {/* 3. EXECUTIVE TELEMETRY KPI CARDS */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-gray-900">Real-Time Threat Intelligence</h3>
          <span className="text-xs font-mono text-gray-500">Updated Live</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          
          <div className="resemble-card p-6 space-y-3">
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span className="font-semibold">Calls Analyzed</span>
              <div className="w-8 h-8 rounded-full bg-teal-50 flex items-center justify-center text-teal-700">
                <PhoneCall className="w-4 h-4" />
              </div>
            </div>
            <div className="text-4xl font-extrabold font-mono text-gray-900">
              {data.total_calls_analyzed}
            </div>
            <div className="text-xs text-teal-700 font-medium flex items-center space-x-1">
              <TrendingUp className="w-3.5 h-3.5" />
              <span>100% audio streams verified</span>
            </div>
          </div>

          <div className="resemble-card p-6 space-y-3">
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span className="font-semibold">Synthetic Voices Isolated</span>
              <div className="w-8 h-8 rounded-full bg-amber-50 flex items-center justify-center text-amber-600">
                <Activity className="w-4 h-4" />
              </div>
            </div>
            <div className="text-4xl font-extrabold font-mono text-amber-600">
              {data.synthetic_voices_detected}
            </div>
            <div className="text-xs text-gray-500">Deepfake probability ≥ 65%</div>
          </div>

          <div className="resemble-card p-6 space-y-3">
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span className="font-semibold">Incidents Flagged</span>
              <div className="w-8 h-8 rounded-full bg-red-50 flex items-center justify-center text-red-600">
                <ShieldAlert className="w-4 h-4" />
              </div>
            </div>
            <div className="text-4xl font-extrabold font-mono text-red-600">
              {data.total_incidents_flagged}
            </div>
            <div className="text-xs text-red-600/80 font-medium">HIGH / CRITICAL risk events</div>
          </div>

          <div className="resemble-card p-6 space-y-3">
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span className="font-semibold">Avg System Risk Score</span>
              <div className="w-8 h-8 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-600">
                <Cpu className="w-4 h-4" />
              </div>
            </div>
            <div className="text-4xl font-extrabold font-mono text-emerald-600">
              {data.avg_risk_score} <span className="text-xs text-gray-400 font-sans">/ 100</span>
            </div>
            <div className="text-xs text-gray-500">Baseline threat posture</div>
          </div>

        </div>
      </div>

      {/* 4. RECENT IMPERSONATION ATTACK ALERTS TABLE */}
      <div className="resemble-card p-6 sm:p-8 space-y-5">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-extrabold text-gray-900">Recent Security Intervention Ledger</h3>
            <p className="text-xs text-gray-500 mt-0.5">Automated prevention responses recorded on hash-chain ledger</p>
          </div>
          <span className="text-xs font-mono bg-gray-100 text-gray-700 px-3 py-1 rounded-full font-semibold">
            SIH26104 Audit Trail
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-gray-50 text-gray-500 uppercase font-mono text-[10px] border-b border-gray-200">
              <tr>
                <th className="px-4 py-3 font-semibold">Incident ID</th>
                <th className="px-4 py-3 font-semibold">Session</th>
                <th className="px-4 py-3 font-semibold">Risk Level</th>
                <th className="px-4 py-3 font-semibold">Risk Score</th>
                <th className="px-4 py-3 font-semibold">Action Taken</th>
                <th className="px-4 py-3 font-semibold">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 font-sans">
              {data.recent_incidents.map((inc) => (
                <tr key={inc.id} className="hover:bg-gray-50/80 transition-colors">
                  <td className="px-4 py-3.5 font-mono text-teal-700 font-bold">{inc.id}</td>
                  <td className="px-4 py-3.5 font-mono text-gray-600">{inc.session_id}</td>
                  <td className="px-4 py-3.5">
                    <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                      inc.risk_level === 'CRITICAL' 
                        ? 'bg-red-100 text-red-700 border border-red-200' 
                        : 'bg-amber-100 text-amber-800 border border-amber-200'
                    }`}>
                      {inc.risk_level}
                    </span>
                  </td>
                  <td className="px-4 py-3.5 font-mono font-bold text-gray-900">{inc.risk_score}</td>
                  <td className="px-4 py-3.5 font-mono text-gray-600">{inc.action_taken}</td>
                  <td className="px-4 py-3.5">
                    <span className="px-2.5 py-1 rounded-full bg-gray-100 text-gray-700 font-medium">
                      {inc.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
