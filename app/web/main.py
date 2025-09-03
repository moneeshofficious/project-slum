# app/web/main.py
"""
Optional FastAPI entrypoint that *wraps your existing pipeline*.
Only used if you choose to run an HTTP API (doesn't affect existing tests).
If FastAPI/uvicorn are not installed, skip running this file.
"""
from __future__ import annotations
from typing import Any, Dict

try:
    from fastapi import FastAPI
    from pydantic import BaseModel
except Exception as _e:  # pragma: no cover
    # Allow the file to exist without forcing dependencies at import time.
    FastAPI = None  # type: ignore
    BaseModel = object  # type: ignore

from importlib import import_module

def _call_enforce_scope(user_msg: str) -> tuple[str, bool]:
    """Compat wrapper: supports both (msg, blocked) and (blocked, msg)."""
    s = import_module("app.safety.safety")
    out = s.enforce_scope(user_msg)  # type: ignore[attr-defined]
    if isinstance(out, tuple) and len(out) == 2:
        a, b = out
        if isinstance(a, bool):
            return (str(b), bool(a))  # (msg, blocked) from (blocked, msg)
        if isinstance(b, bool):
            return (str(a), bool(b))  # (msg, blocked)
    return (str(out), False)

def run_pipeline(user_msg: str, profile: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Wrapper that prefers your existing orchestrator pipeline."""
    profile = profile or {}
    # Try your real pipeline first
    try:
        pipe = import_module("app.orchestrator.pipeline")
        if hasattr(pipe, "run"):
            return pipe.run(user_msg=user_msg, profile=profile)  # type: ignore[call-arg]
        if hasattr(pipe, "run_pipeline"):
            return pipe.run_pipeline(user_msg, profile)  # type: ignore[misc]
    except Exception:
        pass

    # Fallback: minimal safe response + echo
    msg, blocked = _call_enforce_scope(user_msg)
    if blocked:
        return {"mode": "blocked", "reply": msg}
    return {"mode": "inner_me", "reply": f"Validate → Reflect → Tiny step → Why\n\nYou said: {msg}", "style": {"tone":"Warm"}}

# If FastAPI is available, expose an API
if FastAPI:
    app = FastAPI(title="SLUM API (Bridge)")
    class ChatIn(BaseModel):  # type: ignore[misc]
        user_msg: str
        profile: dict | None = None

    @app.get("/health")
    def health():  # type: ignore[reportGeneralTypeIssues]
        return {"ok": True}

    @app.post("/chat")
    def chat(body: ChatIn):  # type: ignore[reportGeneralTypeIssues]
        return run_pipeline(body.user_msg, body.profile or {})
