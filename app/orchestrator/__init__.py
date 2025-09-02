# app/orchestrator/__init__.py
"""
Orchestrator package
Exports run_inference for tests and app entry points.
"""
from .pipeline import run_inference  # re-export for convenience

__all__ = ["run_inference"]
