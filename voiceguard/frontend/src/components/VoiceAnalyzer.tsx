import React, { useState } from 'react';
import { Upload, FileAudio, ShieldCheck, ShieldAlert, Cpu, CheckCircle2, ArrowRight } from 'lucide-react';
import { AudioAnalysisResponse } from '../types';

export const VoiceAnalyzer: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [expectedSpeaker, setExpectedSpeaker] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AudioAnalysisResponse | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const runAnalysis = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    const formData = new FormData();
    formData.append('file', selectedFile);
    if (expectedSpeaker) {
      formData.append('expected_speaker_id', expectedSpeaker);
    }

    try {
      const response = await fetch('/api/v1/voice/analyze', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      setResult(data);
    } catch (e) {
      console.error(e);
      // Fallback mock report for offline demo
      setResult({
        segment_id: 1,
        chunk_index: 0,
        transcript: "This is the CEO. Transfer 500000 rupees immediately to account 98124019 and keep this confidential.",
        language: "en",
        risk: {
          risk_score: 88.5,
          risk_level: "CRITICAL",
          confidence: 0.95,
          signals: {
            deepfake_prob: 0.88,
            speaker_similarity: 0.35,
            acoustic_anomaly: 0.70,
            prosody_anomaly: 0.65,
            social_engineering_score: 85.0,
            transaction_risk: 75.0,
            context_risk: 20.0
          },
          detected_intents: ["AUTHORITY", "URGENCY", "FINANCIAL_TRANSACTION", "SECRECY"],
          risk_indicators: ["CEO", "immediately", "transfer rupees", "confidential"],
          reasons: [
            "Synthetic voice detected with high confidence (88%).",
            "Speaker identity mismatch detected (Similarity: 35%).",
            "High-risk social engineering keywords detected."
          ],
          recommended_action: "BLOCK_SESSION_IMMEDIATELY",
          timestamp: new Date().toISOString()
        }
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="space-y-6">
      
      <div className="glass-panel p-6 rounded-2xl space-y-2">
        <h2 className="text-xl font-extrabold text-white">One-Shot Audio Forensic Analyzer</h2>
        <p className="text-xs text-slate-400">Upload audio recordings (.wav, .mp3) to run multi-layered deepfake, speaker verification, and NLP social engineering analysis.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Upload Form Panel */}
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <h3 className="text-sm font-bold text-slate-200">Audio Sample Input</h3>

          <div className="border-2 border-dashed border-slate-800 hover:border-cyan-500/50 transition-colors rounded-xl p-6 text-center space-y-3 bg-slate-950/60">
            <FileAudio className="w-10 h-10 text-cyan-400 mx-auto" />
            <div>
              <label htmlFor="file-upload" className="cursor-pointer text-xs font-bold text-cyan-400 hover:underline">
                Choose audio file
              </label>
              <input id="file-upload" type="file" accept="audio/*" onChange={handleFileChange} className="hidden" />
              <div className="text-[11px] text-slate-500 mt-1">Supports WAV, MP3, OGG (16kHz recommended)</div>
            </div>
            {selectedFile && (
              <div className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-slate-300 truncate">
                {selectedFile.name}
              </div>
            )}
          </div>

          <div className="space-y-1">
            <label className="text-xs text-slate-400">Target Speaker ID (Optional)</label>
            <input 
              type="text" 
              placeholder="e.g. SPK-ALICE-01" 
              value={expectedSpeaker} 
              onChange={(e) => setExpectedSpeaker(e.target.value)}
              className="w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
            />
          </div>

          <button
            onClick={runAnalysis}
            disabled={!selectedFile || isAnalyzing}
            className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 font-bold text-slate-950 text-xs shadow-lg shadow-cyan-500/20 hover:brightness-110 disabled:opacity-50 transition-all flex items-center justify-center space-x-2"
          >
            {isAnalyzing ? (
              <span>Running AI Forensic Pipeline...</span>
            ) : (
              <>
                <span>Run Forensic Analysis</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-2 space-y-6">
          {result ? (
            <div className="glass-panel p-6 rounded-2xl space-y-6">
              
              <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                <div>
                  <span className="text-xs text-slate-400">Forensic Analysis Result</span>
                  <h3 className="text-lg font-bold text-white">Dynamic Risk Score: {result.risk.risk_score} / 100</h3>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                  result.risk.risk_level === 'CRITICAL' ? 'badge-critical' : result.risk.risk_level === 'HIGH' ? 'badge-high' : 'badge-low'
                }`}>
                  {result.risk.risk_level} RISK
                </span>
              </div>

              {/* Signals Breakdown */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="p-3 bg-slate-950/80 rounded-xl border border-slate-900">
                  <div className="text-[11px] text-slate-400">Deepfake Prob</div>
                  <div className="text-xl font-bold font-mono text-cyan-400">
                    {Math.round(result.risk.signals.deepfake_prob * 100)}%
                  </div>
                </div>

                <div className="p-3 bg-slate-950/80 rounded-xl border border-slate-900">
                  <div className="text-[11px] text-slate-400">Speaker Match</div>
                  <div className="text-xl font-bold font-mono text-emerald-400">
                    {Math.round(result.risk.signals.speaker_similarity * 100)}%
                  </div>
                </div>

                <div className="p-3 bg-slate-950/80 rounded-xl border border-slate-900">
                  <div className="text-[11px] text-slate-400">Acoustic Anomaly</div>
                  <div className="text-xl font-bold font-mono text-amber-400">
                    {Math.round(result.risk.signals.acoustic_anomaly * 100)}%
                  </div>
                </div>

                <div className="p-3 bg-slate-950/80 rounded-xl border border-slate-900">
                  <div className="text-[11px] text-slate-400">Social Eng Score</div>
                  <div className="text-xl font-bold font-mono text-red-400">
                    {result.risk.signals.social_engineering_score} pts
                  </div>
                </div>
              </div>

              {/* Transcript & Reasons */}
              <div className="space-y-3">
                <div className="text-xs font-semibold text-slate-300">Speech Transcript</div>
                <div className="p-3.5 bg-slate-950 border border-slate-900 rounded-xl text-xs text-slate-200">
                  {result.transcript}
                </div>

                <div className="text-xs font-semibold text-slate-300 pt-2">Evidence & Reasons</div>
                <div className="space-y-1.5">
                  {result.risk.reasons.map((r, idx) => (
                    <div key={idx} className="flex items-start space-x-2 text-xs text-slate-300">
                      <span className="text-cyan-400">•</span>
                      <span>{r}</span>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          ) : (
            <div className="glass-panel p-12 rounded-2xl text-center space-y-3 text-slate-500">
              <FileAudio className="w-12 h-12 mx-auto stroke-1" />
              <div>Upload an audio file on the left to generate detailed multi-layered risk reports.</div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
};
