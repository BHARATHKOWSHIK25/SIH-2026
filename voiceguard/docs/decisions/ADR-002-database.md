# ADR-002: Database

**Status**: Accepted  
**Date**: 2026-09-04  
**Decision**: SQLite (prototype) with SQLAlchemy ORM for PostgreSQL migration

## Context

VoiceGuard needs persistent storage for users, calls, incidents, audit events, and speaker profiles. The development environment lacks PostgreSQL and Docker.

## Decision

Use **SQLite** for the prototype via **SQLAlchemy ORM**. Schema designed for PostgreSQL migration (config change only).

## Alternatives Considered

| Alternative | Reason Rejected |
|-------------|----------------|
| PostgreSQL directly | Not available locally; would require Docker (also unavailable) |
| MongoDB | Document store less suited for relational security data with audit requirements |
| In-memory only | Data loss on restart; insufficient for incident management |

## Rationale

- **Zero configuration**: SQLite is a file; no server needed.
- **SQLAlchemy abstraction**: Switching to PostgreSQL requires changing only the connection string.
- **Sufficient for SIH demo**: Single-user prototype; SQLite handles this well.

## Tradeoffs

- **No concurrent writes**: SQLite uses file-level locking. Multiple simultaneous write operations may queue.
- **No JSON operators**: Some advanced queries available in PostgreSQL are unavailable.
- **No full-text search**: PostgreSQL `tsvector` not available.

## Migration Path

```python
# Development (SQLite)
DATABASE_URL=sqlite:///./voiceguard.db

# Production (PostgreSQL)
DATABASE_URL=postgresql://user:pass@host:5432/voiceguard
```

No code changes required. Only environment variable change.

## Limitations

- Not suitable for production with concurrent users.
- No native vector storage for embeddings (use BLOB or separate file storage).
