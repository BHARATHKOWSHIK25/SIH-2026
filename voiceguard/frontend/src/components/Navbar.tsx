import React from 'react';
import { ShieldCheck, Cpu, Database, Activity, Mic } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'overview', label: 'Dashboard' },
    { id: 'monitor', label: 'Live Monitor' },
    { id: 'analyzer', label: 'Audio Analyzer' },
    { id: 'speaker', label: 'Voice Registry' },
    { id: 'incidents', label: 'Incident Hub' },
    { id: 'audit', label: 'Blockchain Audit' },
  ];

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50 px-6 py-3.5 shadow-xs">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Brand Logo & Name */}
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('overview')}>
          <div className="flex items-center space-x-1">
            <svg className="w-8 h-8 text-teal-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="M2 12h2l2-5 3 10 3-8 3 6 2-3h3" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-xl font-extrabold tracking-tight text-gray-900 font-sans">
              VOICEGUARD<span className="text-teal-600">.AI</span>
            </span>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-teal-50 text-teal-700 border border-teal-200 uppercase tracking-wider font-mono">
              SIH26104
            </span>
          </div>
        </div>

        {/* Center Navigation Links */}
        <nav className="hidden lg:flex items-center space-x-1 bg-gray-50 p-1 rounded-full border border-gray-200">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`px-4 py-1.5 rounded-full text-xs font-semibold transition-all ${
                activeTab === item.id
                  ? 'bg-gray-900 text-white shadow-xs'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-200/60'
              }`}
            >
              {item.label}
            </button>
          ))}
        </nav>

        {/* Right Status Actions */}
        <div className="flex items-center space-x-3 text-xs">
          <div className="hidden sm:flex items-center space-x-1.5 text-gray-500 bg-gray-100 px-3 py-1.5 rounded-full font-mono text-[11px]">
            <Cpu className="w-3.5 h-3.5 text-teal-600" />
            <span>INT8 Model</span>
          </div>

          <div className="hidden sm:flex items-center space-x-1.5 text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-full font-mono text-[11px]">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>SHA-256 Ledger</span>
          </div>

          <button
            onClick={() => setActiveTab('monitor')}
            className="resemble-pill px-4 py-2 text-xs flex items-center space-x-1.5 shadow-sm"
          >
            <Mic className="w-3.5 h-3.5 text-teal-400" />
            <span>Try Live Monitor</span>
          </button>
        </div>

      </div>
    </header>
  );
};
