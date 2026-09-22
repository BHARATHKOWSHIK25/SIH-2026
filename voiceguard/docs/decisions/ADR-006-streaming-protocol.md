# ADR-006: Streaming Protocol

**Status**: Accepted  
**Date**: 2026-09-04  
**Decision**: WebSocket (FastAPI native)

## Context

VoiceGuard requires real-time bidirectional communication between:
1. Browser → Backend: Audio chunk streaming
2. Backend → Browser: Analysis results, risk updates, alerts

## Decision

Use **WebSocket** via FastAPI's native WebSocket support.

## Alternatives Considered

| Alternative | Reason Deferred |
|-------------|----------------|
| WebRTC | More complex setup; designed for peer-to-peer; overkill for prototype |
| Server-Sent Events (SSE) | Unidirectional; cannot receive audio from client |
| gRPC-web | Requires proxy setup; browser support limited |
| HTTP polling | High latency; inefficient for real-time updates |

## Rationale

- **Bidirectional**: Client sends audio, server sends results — both on same connection.
- **FastAPI native**: No additional dependencies.
- **Browser support**: All modern browsers support WebSocket natively.
- **Session-based**: Natural mapping to call sessions.

## Protocol Design

### Connection
```
ws://host:port/api/v1/ws/calls/{call_id}/stream?token={jwt}
```

### Client → Server
- `audio_chunk`: Base64-encoded PCM16 audio data
- `control`: pause/resume/end_call

### Server → Client
- `analysis_update`: Per-chunk analysis results
- `risk_alert`: Threshold crossing alerts
- `system_status`: Module availability
- `error`: Module failures

## Tradeoffs

- **No built-in reconnection**: Must implement client-side reconnection with exponential backoff.
- **No message ordering guarantee after reconnect**: Must use sequence numbers.
- **Single connection per call**: If connection drops, analysis pauses.

## Limitations

- WebSocket does not support binary frames efficiently through JSON messages; audio is base64-encoded (33% overhead). Acceptable for prototype.
- No built-in load balancing. Single-server prototype.
