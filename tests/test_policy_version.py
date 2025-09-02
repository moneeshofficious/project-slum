# tests/test_policy_version.py
from app.orchestrator.pipeline import run_inference

def test_policy_version_in_meta():
    out = run_inference("inner_me", "hello", "PV1", {"age_band": "adult"})
    assert "policy_version" in out.get("meta", {})
