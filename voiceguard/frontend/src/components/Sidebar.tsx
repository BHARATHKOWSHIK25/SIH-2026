import React from 'react';
import { 
  LayoutDashboard, 
  Mic, 
  FileAudio, 
  UserCheck, 
  ShieldAlert, 
  Link as LinkIcon 
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'overview', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'monitor', label: 'Live Call Monitor', icon: Mic, badge: 'LIVE' },
    { id: 'analyzer', label: 'Audio Analyzer', icon: FileAudio },
    { id: 'speaker', label: 'Voice Registry', icon: UserCheck },
    { id: 'incidents', label: 'Incident Hub', icon: ShieldAlert },
    { id: 'audit', label: 'Blockchain Audit', icon: LinkIcon }
  ];

  return (
    <aside className="w-56 shrink-0 hidden md:block">
      <div className="resemble-card p-3 space-y-1 sticky top-20">
        <div className="px-3 py-2 text-[11px] font-extrabold text-gray-400 uppercase tracking-wider">
          Platform Menu
        </div>

        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                isActive
                  ? 'bg-gray-900 text-white shadow-xs'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <div className="flex items-center space-x-2.5">
                <Icon className={`w-4 h-4 ${isActive ? 'text-teal-400' : 'text-gray-400'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className="px-1.5 py-0.5 text-[9px] font-bold rounded-full bg-red-100 text-red-600 border border-red-200">
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}

        <div className="pt-4 mt-4 border-t border-gray-100">
          <div className="p-3 rounded-xl bg-gray-50 border border-gray-200 text-[11px] space-y-1 text-gray-500 font-sans">
            <div className="font-bold text-gray-800">AICTE Cybersecurity</div>
            <div className="text-[10px] text-teal-700 font-mono">SIH26104 Real-Time Protection</div>
          </div>
        </div>
      </div>
    </aside>
  );
};
