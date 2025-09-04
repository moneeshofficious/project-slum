# Project SLUM — Master Tracker (24 Modules)

> Status keys: ☐ not started | ◐ in progress | ✅ done | ❓ not verified

| # | Module | Spec aligned to 24? | Code present | Tests passing | Deployed | Owner | Notes |
|---|--------|---------------------|--------------|---------------|---------|-------|-------|
| 1 | Foundational Security & Hardening | ◐ | ◐ | ◐ | ☐ | | PII redaction + scope limiter in repo; expand threat model, headers, auth tests. |
| 2 | Core Data Layer | ☐ | ☐ | ☐ | ☐ | | Alembic migration not verified; ERD/index/backups pending. |
| 3 | Web App Service | ◐ | ◐ | ☐ | ☐ | | App boots; auth/CSP/HSTS and CI/CD not verified. |
| 4 | Safety & Scope Guard | ◐ | ◐ | ◐ | ☐ | | Risk/Scope/DEI present; crisp <50ms perf + crisis trigger checks pending. |
| 5 | Orchestrator Engine | ☐ | ☐ | ☐ | ☐ | | |
| 6 | Frontend UI & Experience | ☐ | ☐ | ☐ | ☐ | | |
| 7 | Knowledge & Retrieval Packs | ☐ | ☐ | ☐ | ☐ | | |
| 8 | Core Skills Library | ☐ | ☐ | ☐ | ☐ | | |
| 9 | Science Notes Engine | ☐ | ☐ | ☐ | ☐ | | |
| 10 | Conversation State Machine | ☐ | ☐ | ☐ | ☐ | | |
| 11 | “Inner Me” Companion Engine | ☐ | ☐ | ☐ | ☐ | | |
| 12 | Memory Layer | ☐ | ☐ | ☐ | ☐ | | |
| 13 | Personalization Engine | ☐ | ☐ | ☐ | ☐ | | |
| 14 | “Mate Mode” Coach Engine | ☐ | ☐ | ☐ | ☐ | | |
| 15 | Interactive Skill Modules | ☐ | ☐ | ☐ | ☐ | | |
| 16 | Crisis Hand-off Protocols | ☐ | ☐ | ☐ | ☐ | | |
| 17 | User Journey & Progress Engine | ☐ | ☐ | ☐ | ☐ | | |
| 18 | Observability & Reliability | ◐ | ◐ | ☐ | ☐ | | Metrics up; logs/alerts/retries/cache to verify. |
| 19 | Proactive Engagement Engine | ☐ | ☐ | ☐ | ☐ | | |
| 20 | Voice & Tonality Engine | ☐ | ☐ | ☐ | ☐ | | |
| 21 | Evaluation & Red-Teaming | ☐ | ☐ | ☐ | ☐ | | |
| 22 | AI-Powered Volunteer Simulation | ☐ | ☐ | ☐ | ☐ | | |
| 23 | Updates & Learning Loop | ☐ | ☐ | ☐ | ☐ | | |
| 24 | Accessibility & Localization | ☐ | ☐ | ☐ | ☐ | | |

## How we verify each checkbox
- **Spec aligned**: module’s Goals/Inputs/Checklist/Run/Verify sections updated to the 24-module doc.
- **Code present**: module folder + service/API stubs exist with type hints + docstrings.
- **Tests passing**: pytest coverage for the module features; no red tests for this module.
- **Deployed**: module reachable in the running app (or enabled feature flag) with logs/metrics.

## Evidence log (quick pointers)
- App boot + metrics exporter observed (M3, M18).
- PII redaction & scope tests executed (M1, M4).
- Alembic migration attempt error seen (M2) — not confirmed successful.

- 2025-09-04: pytest 66 passed, 19 skipped.
- 2025-09-04: app boot ok; metrics on :9108.
- 2025-09-04: alembic upgrade head ?
- 2025-09-04: metrics exporter ? on :9108 (ENABLE_METRICS=true).
