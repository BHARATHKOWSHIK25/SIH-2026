import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { DashboardOverviewComponent } from './components/DashboardOverview';
import { LiveCallMonitor } from './components/LiveCallMonitor';
import { VoiceAnalyzer } from './components/VoiceAnalyzer';
import { SpeakerRegistry } from './components/SpeakerRegistry';
import { IncidentHub } from './components/IncidentHub';
import { AuditInspector } from './components/AuditInspector';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');

  const renderActiveView = () => {
    switch (activeTab) {
      case 'overview':
        return <DashboardOverviewComponent onNavigate={setActiveTab} />;
      case 'monitor':
        return <LiveCallMonitor />;
      case 'analyzer':
        return <VoiceAnalyzer />;
      case 'speaker':
        return <SpeakerRegistry />;
      case 'incidents':
        return <IncidentHub />;
      case 'audit':
        return <AuditInspector />;
      default:
        return <DashboardOverviewComponent onNavigate={setActiveTab} />;
    }
  };

  return (
    <div className="min-h-screen bg-[#FAFAFA] text-gray-900 flex flex-col font-sans">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <div className="flex-1 flex max-w-7xl mx-auto w-full px-4 sm:px-6 py-6 gap-8">
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
        
        <main className="flex-1 min-w-0">
          {renderActiveView()}
        </main>
      </div>
    </div>
  );
};
