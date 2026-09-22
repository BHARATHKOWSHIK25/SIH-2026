export interface SignalScores {
  deepfake_prob: number;
  speaker_similarity: number;
  acoustic_anomaly: number;
  prosody_anomaly: number;
  social_engineering_score: number;
  transaction_risk: number;
  context_risk: number;
}

export interface DynamicRiskResponse {
  risk_score: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  confidence: number;
  signals: SignalScores;
  detected_intents: string[];
  risk_indicators: string[];
  reasons: string[];
  recommended_action: string;
  timestamp: string;
}

export interface AudioAnalysisResponse {
  segment_id: number;
  chunk_index: number;
  transcript: string;
  language: string;
  risk: DynamicRiskResponse;
}

export interface CallSession {
  id: string;
  caller_id: string;
  callee_id: string;
  expected_speaker_id?: string;
  status: 'ACTIVE' | 'ENDED' | 'BLOCKED' | 'ON_HOLD';
  current_risk_score: number;
  current_risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  peak_risk_score: number;
  start_time: string;
  end_time?: string;
}

export interface Incident {
  id: string;
  session_id: string;
  risk_score: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  status: 'OPEN' | 'UNDER_INVESTIGATION' | 'RESOLVED' | 'FALSE_POSITIVE';
  title: string;
  description?: string;
  evidence_json?: any;
  action_taken: string;
  created_at: string;
  resolved_at?: string;
}

export interface VoiceProfile {
  id: number;
  speaker_id: string;
  speaker_name: string;
  audio_sample_path?: string;
  is_active: boolean;
  created_at: string;
}

export interface AuditEvent {
  event_index: number;
  previous_hash: string;
  event_hash: string;
  event_type: string;
  session_id?: string;
  payload_json: any;
  timestamp: string;
}

export interface AuditVerifyResponse {
  total_events: number;
  is_valid: boolean;
  broken_at_index?: number;
  message: string;
}

export interface DashboardOverview {
  total_calls_analyzed: number;
  total_incidents_flagged: number;
  active_calls_count: number;
  synthetic_voices_detected: number;
  avg_risk_score: number;
  recent_incidents: Incident[];
  blockchain_hash_head: string;
}
