# app/orchestrator/core.py
"""
Thin bridge that forwards to your existing orchestrator implementation.
Prefers app.orchestrator.pipeline.{run|run_pipeline}, falls back safely.
"""
from __future__ import annotations
from typing import Any, Dict
from importlib import import_module

def _safe_enforce(text: str) -> tuple[str, bool]:
    s = import_module("app.safety.safety")
    out = s.enforce_scope(text)  # type: ignore[attr-defined]
    if isinstance(out, tuple) and len(out) == 2:
        a, b = out
        if isinstance(a, bool):
            return (str(b), bool(a))
        if isinstance(b, bool):
            return (str(a), bool(b))
    return (str(out), False)

def run_pipeline(user_msg: str, profile: Dict[str, Any] | None = None) -> Dict[str, Any]:
    profile = profile or {}
    try:
        pipe = import_module("app.orchestrator.pipeline")
        if hasattr(pipe, "run"):
            return pipe.run(user_msg=user_msg, profile=profile)  # type: ignore[call-arg]
        if hasattr(pipe, "run_pipeline"):
            return pipe.run_pipeline(user_msg, profile)  # type: ignore[misc]
    except Exception:
        pass
    msg, blocked = _safe_enforce(user_msg)
    if blocked:
        return {"mode": "blocked", "reply": msg}
    return {"mode": "inner_me", "reply": f"(fallback) You said: {msg}", "style": {"tone":"Warm"}}
