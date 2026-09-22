import React, { useState, useEffect } from 'react';
import { UserCheck, Plus, CheckCircle, ShieldCheck } from 'lucide-react';
import { VoiceProfile } from '../types';

export const SpeakerRegistry: React.FC = () => {
  const [profiles, setProfiles] = useState<VoiceProfile[]>([
    {
      id: 1,
      speaker_id: 'SPK-ALICE-01',
      speaker_name: 'Alice Vance (Chief Financial Officer)',
      audio_sample_path: 'alice_enrolment_sample.wav',
      is_active: true,
      created_at: new Date(Date.now() - 86400000 * 5).toISOString()
    },
    {
      id: 2,
      speaker_id: 'SPK-BOB-02',
      speaker_name: 'Bob Miller (Managing Director)',
      audio_sample_path: 'bob_enrolment_sample.wav',
      is_active: true,
      created_at: new Date(Date.now() - 86400000 * 2).toISOString()
    }
  ]);

  const [speakerId, setSpeakerId] = useState('');
  const [speakerName, setSpeakerName] = useState('');
  const [sampleFile, setSampleFile] = useState<File | null>(null);
  const [isRegistering, setIsRegistering] = useState(false);

  useEffect(() => {
    fetch('/api/v1/speaker/profiles')
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setProfiles(data);
        }
      })
      .catch(() => {});
  }, []);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!speakerId || !speakerName || !sampleFile) return;

    setIsRegistering(true);
    const formData = new FormData();
    formData.append('speaker_id', speakerId);
    formData.append('speaker_name', speakerName);
    formData.append('file', sampleFile);

    try {
      const response = await fetch('/api/v1/speaker/register', {
        method: 'POST',
        body: formData
      });
      const newProfile = await response.json();
      setProfiles((prev) => [newProfile, ...prev]);
      setSpeakerId('');
      setSpeakerName('');
      setSampleFile(null);
    } catch (err) {
      console.error(err);
    } finally {
      setIsRegistering(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-2xl space-y-2">
        <h2 className="text-xl font-extrabold text-white">Target Voice Profile Registry</h2>
        <p className="text-xs text-slate-400">Enroll baseline 192-dimensional ECAPA-TDNN voice embeddings for authorized executives and VIP personnel.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Register Form */}
        <form onSubmit={handleRegister} className="glass-panel p-6 rounded-2xl space-y-4">
          <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
            <Plus className="w-4 h-4 text-cyan-400" />
            <span>Enroll New Voice Profile</span>
          </h3>

          <div className="space-y-1">
            <label className="text-xs text-slate-400">Speaker ID</label>
            <input 
              type="text" 
              placeholder="e.g. SPK-CHARLIE-03" 
              value={speakerId}
              onChange={(e) => setSpeakerId(e.target.value)}
              className="w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
              required
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs text-slate-400">Full Name & Role</label>
            <input 
              type="text" 
              placeholder="e.g. Charlie Brown (VP Operations)" 
              value={speakerName}
              onChange={(e) => setSpeakerName(e.target.value)}
              className="w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
              required
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs text-slate-400">Enrollment Audio Sample (.wav)</label>
            <input 
              type="file" 
              accept="audio/*"
              onChange={(e) => e.target.files && setSampleFile(e.target.files[0])}
              className="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-cyan-500/20 file:text-cyan-400 hover:file:bg-cyan-500/30 cursor-pointer"
              required
            />
          </div>

          <button
            type="submit"
            disabled={isRegistering}
            className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 font-bold text-slate-950 text-xs shadow-lg shadow-cyan-500/20 hover:brightness-110 disabled:opacity-50 transition-all"
          >
            {isRegistering ? 'Extracting Speaker Embedding...' : 'Enroll Voice Profile'}
          </button>
        </form>

        {/* Profile List */}
        <div className="lg:col-span-2 glass-panel p-6 rounded-2xl space-y-4">
          <h3 className="text-sm font-bold text-slate-200">Enrolled Speaker Embeddings</h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {profiles.map((p) => (
              <div key={p.id} className="p-4 rounded-xl bg-slate-950/80 border border-slate-900 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs text-cyan-400 font-bold">{p.speaker_id}</span>
                  <span className="flex items-center space-x-1 text-[10px] text-emerald-400 font-medium bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                    <ShieldCheck className="w-3 h-3" />
                    <span>192-dim Vector</span>
                  </span>
                </div>
                <div className="text-sm font-bold text-slate-100">{p.speaker_name}</div>
                <div className="text-[11px] text-slate-500">Sample: {p.audio_sample_path || 'sample.wav'}</div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};
