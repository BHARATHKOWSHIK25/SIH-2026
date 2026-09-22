import React, { useState, useEffect, useRef } from 'react';
import { 
  Mic, 
  MicOff, 
  Square, 
  ShieldAlert, 
  ShieldCheck, 
  Lock, 
  Radio, 
  Activity, 
  User,
  MessageSquare
} from 'lucide-react';
import { DynamicRiskResponse } from '../types';

export const LiveCallMonitor: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [sessionId, setSessionId] = useState(`CALL-${Math.random().toString(36).substring(2, 9).toUpperCase()}`);
  const [expectedSpeaker, setExpectedSpeaker] = useState('SPK-ALICE-01');
  const [riskData, setRiskData] = useState<DynamicRiskResponse>({
    risk_score: 12.5,
    risk_level: 'LOW',
    confidence: 0.92,
    signals: {
      deepfake_prob: 0.05,
      speaker_similarity: 0.94,
      acoustic_anomaly: 0.08,
      prosody_anomaly: 0.04,
      social_engineering_score: 0,
      transaction_risk: 0,
      context_risk: 10
    },
    detected_intents: [],
    risk_indicators: [],
    reasons: ['Authentic voice characteristics verified.'],
    recommended_action: 'CONTINUE_MONITORING',
    timestamp: new Date().toISOString()
  });

  const [transcript, setTranscript] = useState("Hello, this is Alice from the accounts team calling to verify the quarterly audit timeline.");
  const wsRef = useRef<WebSocket | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Audio Waveform Visualizer
  useEffect(() => {
    let animationFrameId: number;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const renderWaveform = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.lineWidth = 2;
      ctx.strokeStyle = riskData.risk_level === 'CRITICAL' ? '#EF4444' : riskData.risk_level === 'HIGH' ? '#F97316' : '#0D9488';
      ctx.beginPath();

      const sliceWidth = canvas.width / 50;
      let x = 0;

      for (let i = 0; i < 50; i++) {
        const amplitude = isRecording ? Math.random() * (canvas.height / 2.5) : 4;
        const y = canvas.height / 2 + (i % 2 === 0 ? amplitude : -amplitude);

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
        x += sliceWidth;
      }
      ctx.stroke();
      animationFrameId = requestAnimationFrame(renderWaveform);
    };

    renderWaveform();
    return () => cancelAnimationFrame(animationFrameId);
  }, [isRecording, riskData.risk_level]);

  const startStreaming = () => {
    setIsRecording(true);
    const newSessionId = `CALL-${Math.random().toString(36).substring(2, 9).toUpperCase()}`;
    setSessionId(newSessionId);

    const wsUrl = `ws://${window.location.host}/ws/calls/${newSessionId}/stream`;
    try {
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onmessage = (event) => {
        try {
          const update = JSON.parse(event.data);
          if (update.event === 'risk_update') {
            setRiskData({
              risk_score: update.risk_score,
              risk_level: update.risk_level,
              confidence: update.confidence,
              signals: update.signals,
              detected_intents: [],
              risk_indicators: [],
              reasons: update.recommended_action === 'BLOCK_SESSION_IMMEDIATELY' 
                ? ['CRITICAL: Impersonation attack detected by multi-signal fusion.'] 
                : ['Continuous audio stream analyzed.'],
              recommended_action: update.recommended_action,
              timestamp: update.timestamp
            });
            if (update.transcript) {
              setTranscript(update.transcript);
            }
          }
        } catch (e) {}
      };
    } catch (e) {}

    const interval = setInterval(() => {
      simulateAudioChunk();
    }, 2500);

    (window as any).streamInterval = interval;
  };

  const stopStreaming = () => {
    setIsRecording(false);
    if (wsRef.current) {
      wsRef.current.send(JSON.stringify({ event: 'end_call' }));
      wsRef.current.close();
    }
    if ((window as any).streamInterval) {
      clearInterval((window as any).streamInterval);
    }
  };

  const simulateAudioChunk = () => {
    const scenarios = [
      {
        text: "Hi, I am calling regarding the vendor invoice approval.",
        score: 18.0,
        level: 'LOW' as const,
        deepfake: 0.08,
        speaker: 0.92,
        anomaly: 0.05
      },
      {
        text: "URGENT: Requesting immediate wire transfer of $50,000 to offshore account.",
        score: 88.5,
        level: 'CRITICAL' as const,
        deepfake: 0.89,
        speaker: 0.22,
        anomaly: 0.85
      }
    ];
    const pick = scenarios[Math.floor(Math.random() * scenarios.length)];
    setTranscript(pick.text);
    setRiskData({
      risk_score: pick.score,
      risk_level: pick.level,
      confidence: 0.89,
      signals: {
        deepfake_prob: pick.deepfake,
        speaker_similarity: pick.speaker,
        acoustic_anomaly: pick.anomaly,
        prosody_anomaly: pick.anomaly,
        social_engineering_score: pick.score > 50 ? 75 : 0,
        transaction_risk: pick.score > 50 ? 80 : 0,
        context_risk: 10
      },
      detected_intents: pick.score > 50 ? ['FINANCIAL_TRANSFER', 'URGENCY'] : [],
      risk_indicators: [],
      reasons: pick.score > 50 
        ? ['High deepfake probability detected.', 'Speaker voiceprint mismatch.', 'Urgent financial request keyword flagged.']
        : ['Continuous real-time spectral monitoring active.'],
      recommended_action: pick.score >= 85 ? 'BLOCK_SESSION_IMMEDIATELY' : 'CONTINUE_MONITORING',
      timestamp: new Date().toISOString()
    });
  };

  return (
    <div className="space-y-6">
      
      {/* Top Banner Alert if Critical */}
      {riskData.risk_level === 'CRITICAL' && (
        <div className="p-4 rounded-2xl bg-red-600 text-white flex items-center justify-between shadow-lg animate-pulse">
          <div className="flex items-center space-x-3">
            <ShieldAlert className="w-6 h-6 stroke-[2.5]" />
            <div>
              <div className="text-sm font-extrabold">CRITICAL IMPERSONATION RISK DETECTED</div>
              <div className="text-xs text-red-100">Synthetic voice + Executive impersonation + Financial transfer request isolated.</div>
            </div>
          </div>
          <button 
            onClick={stopStreaming}
            className="px-4 py-2 bg-gray-900 hover:bg-black text-white font-bold text-xs rounded-xl transition-all shadow-md"
          >
            BLOCK SESSION IMMEDIATELY
          </button>
        </div>
      )}

      {/* Control Header */}
      <div className="resemble-card p-6 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${isRecording ? 'bg-red-100 text-red-600 pulse-mic' : 'bg-gray-100 text-gray-600'}`}>
            <Radio className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-mono text-gray-500">{sessionId}</span>
              <span className={`px-2.5 py-0.5 text-[10px] font-bold rounded-full ${
                riskData.risk_level === 'CRITICAL' ? 'bg-red-100 text-red-700' : 'bg-emerald-100 text-emerald-800'
              }`}>
                {riskData.risk_level} RISK ({riskData.risk_score})
              </span>
            </div>
            <h2 className="text-xl font-extrabold text-gray-900">Live Call Analysis Stream</h2>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 bg-gray-100 rounded-xl px-3 py-2 text-xs text-gray-700 font-medium">
            <User className="w-3.5 h-3.5 text-gray-500" />
            <span>Profile:</span>
            <span className="font-mono text-teal-700 font-bold">{expectedSpeaker}</span>
          </div>

          {!isRecording ? (
            <button
              onClick={startStreaming}
              className="resemble-pill px-5 py-2.5 text-xs flex items-center space-x-2 shadow-sm"
            >
              <Mic className="w-4 h-4 text-teal-400" />
              <span>Start Live Monitor</span>
            </button>
          ) : (
            <button
              onClick={stopStreaming}
              className="px-5 py-2.5 rounded-full bg-red-600 hover:bg-red-700 text-white font-bold text-xs flex items-center space-x-2 shadow-sm"
            >
              <Square className="w-4 h-4 fill-current" />
              <span>Stop Stream</span>
            </button>
          )}
        </div>
      </div>

      {/* Main Grid: Visualizer & Waveform */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <div className="lg:col-span-2 space-y-6">
          
          {/* Waveform Panel */}
          <div className="resemble-card p-6 space-y-3">
            <div className="flex items-center justify-between text-xs text-gray-500 font-medium">
              <span className="flex items-center space-x-2">
                <Activity className="w-4 h-4 text-teal-600" />
                <span>Live Audio PCM Waveform (16kHz Mono)</span>
              </span>
              <span className="font-mono text-teal-700 font-bold">SNR: 42.5 dB</span>
            </div>
            <div className="h-28 bg-gray-900 rounded-xl p-2 flex items-center justify-center overflow-hidden">
              <canvas ref={canvasRef} width={600} height={80} className="w-full h-full"></canvas>
            </div>
          </div>

          {/* Metric Cards Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            
            <div className="resemble-card p-4 space-y-1">
              <div className="text-xs text-gray-500 font-semibold">Deepfake Prob</div>
              <div className="text-2xl font-extrabold font-mono text-gray-900">
                {Math.round(riskData.signals.deepfake_prob * 100)}%
              </div>
              <div className="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden mt-2">
                <div 
                  className="bg-teal-600 h-full transition-all duration-500" 
                  style={{ width: `${riskData.signals.deepfake_prob * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="resemble-card p-4 space-y-1">
              <div className="text-xs text-gray-500 font-semibold">Speaker Match</div>
              <div className={`text-2xl font-extrabold font-mono ${riskData.signals.speaker_similarity < 0.5 ? 'text-red-600' : 'text-emerald-600'}`}>
                {Math.round(riskData.signals.speaker_similarity * 100)}%
              </div>
              <div className="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden mt-2">
                <div 
                  className={`h-full transition-all duration-500 ${riskData.signals.speaker_similarity < 0.5 ? 'bg-red-600' : 'bg-emerald-600'}`}
                  style={{ width: `${riskData.signals.speaker_similarity * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="resemble-card p-4 space-y-1">
              <div className="text-xs text-gray-500 font-semibold">Acoustic Anomaly</div>
              <div className="text-2xl font-extrabold font-mono text-amber-600">
                {Math.round(riskData.signals.acoustic_anomaly * 100)}%
              </div>
              <div className="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden mt-2">
                <div 
                  className="bg-amber-500 h-full transition-all duration-500"
                  style={{ width: `${riskData.signals.acoustic_anomaly * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="resemble-card p-4 space-y-1">
              <div className="text-xs text-gray-500 font-semibold">Social Eng Score</div>
              <div className={`text-2xl font-extrabold font-mono ${riskData.signals.social_engineering_score > 50 ? 'text-red-600' : 'text-gray-900'}`}>
                {riskData.signals.social_engineering_score} <span className="text-xs font-normal">pts</span>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden mt-2">
                <div 
                  className="bg-red-500 h-full transition-all duration-500"
                  style={{ width: `${riskData.signals.social_engineering_score}%` }}
                ></div>
              </div>
            </div>

          </div>

          {/* Transcript Panel */}
          <div className="resemble-card p-6 space-y-3">
            <div className="flex items-center justify-between text-xs text-gray-500 font-semibold">
              <span className="flex items-center space-x-2">
                <MessageSquare className="w-4 h-4 text-teal-600" />
                <span>Live Speech Transcript</span>
              </span>
              <span className="font-mono text-gray-400">Whisper Engine</span>
            </div>
            <div className="p-4 bg-gray-50 rounded-xl border border-gray-200 text-sm leading-relaxed text-gray-800 font-medium min-h-[100px]">
              {transcript}
            </div>
          </div>

        </div>

        {/* Risk Fusion Gauge Column */}
        <div className="space-y-6">
          <div className="resemble-card p-6 space-y-4 text-center">
            <div className="text-xs font-extrabold uppercase tracking-wider text-gray-400">
              Impersonation Risk Score
            </div>

            <div className="relative inline-flex items-center justify-center">
              <div className="w-36 h-36 rounded-full border-4 border-gray-100 flex flex-col items-center justify-center shadow-inner">
                <span className={`text-4xl font-extrabold font-mono ${riskData.risk_score >= 75 ? 'text-red-600' : 'text-emerald-600'}`}>
                  {riskData.risk_score}
                </span>
                <span className="text-[10px] text-gray-400">out of 100</span>
              </div>
            </div>

            <div>
              <div className="inline-block px-3 py-1 rounded-full text-xs font-extrabold bg-teal-50 text-teal-800 border border-teal-200">
                POLICY TIER: {riskData.risk_level}
              </div>
              <div className="text-xs text-gray-500 mt-2 font-medium">
                Action: <span className="font-bold text-gray-900">{riskData.recommended_action}</span>
              </div>
            </div>
          </div>

          <div className="resemble-card p-6 space-y-3">
            <div className="flex items-center space-x-2 text-xs font-extrabold text-gray-900">
              <ShieldCheck className="w-4 h-4 text-teal-600" />
              <span>Multi-Signal Fusion Rule</span>
            </div>
            <div className="text-xs text-gray-500 leading-normal">
              No single weak signal produces a CRITICAL score. CRITICAL requires ≥ 2 independent high-confidence indicators.
            </div>

            <div className="space-y-2 pt-2 border-t border-gray-100">
              {riskData.reasons.map((reason, idx) => (
                <div key={idx} className="flex items-start space-x-2 text-xs text-gray-700">
                  <span className="text-teal-600 mt-0.5">•</span>
                  <span>{reason}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <button className="w-full py-3 px-4 rounded-full bg-gray-900 hover:bg-black text-white text-xs font-extrabold flex items-center justify-center space-x-2 shadow-sm transition-all">
              <Lock className="w-3.5 h-3.5 text-teal-400" />
              <span>Issue Secondary MFA Challenge</span>
            </button>
          </div>

        </div>

      </div>
    </div>
  );
};
