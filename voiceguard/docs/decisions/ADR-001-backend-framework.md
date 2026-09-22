# ADR-001: Backend Framework

**Status**: Accepted  
**Date**: 2026-09-04  
**Decision**: Python FastAPI

## Context

VoiceGuard requires a backend that:
1. Integrates natively with Python AI libraries (PyTorch, HuggingFace, librosa)
2. Supports WebSocket connections for real-time audio streaming
3. Provides type-safe request/response validation
4. Handles async I/O for concurrent call processing
5. Has mature ecosystem and documentation

## Decision

Use **Python FastAPI** as the backend framework.

## Alternatives Considered

| Alternative | Reason Rejected |
|-------------|----------------|
| Flask | No native async support. No built-in validation. WebSocket requires extensions. |
| Django | Too heavy for API-focused service. ORM less flexible than SQLAlchemy. |
| Node.js + Express | Would require Python subprocess for AI inference, adding latency and complexity. |
| Go + gRPC | Strong performance but poor AI library ecosystem. |

## Rationale

- **Same language as AI stack**: No cross-language overhead for model inference.
- **Pydantic validation**: Request/response schemas are auto-validated and documented.
- **Async WebSocket**: Native support via `fastapi.WebSocket`.
- **OpenAPI docs**: Auto-generated API documentation.
- **Uvicorn**: ASGI server with good performance on CPU-bound tasks.

## Tradeoffs

- **CPU-bound AI inference blocks the event loop**: Must use `asyncio.to_thread()` or process pools for model inference.
- **Single-process prototype**: Uvicorn with 1 worker is sufficient for SIH demo but not production.

## Limitations

- Not suitable for high-concurrency production without multiple workers or a dedicated AI service.
- Python GIL limits true parallelism for CPU-bound work.
