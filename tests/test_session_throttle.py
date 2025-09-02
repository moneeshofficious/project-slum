# tests/test_session_throttle.py
from app.orchestrator.pipeline import run_inference

def test_per_session_throttle():
    p = {"age_band": "adult"}
    out1 = run_inference("inner_me", "I want to die", "S1", p)
    meta1 = out1.get("meta", {})
    assert meta1.get("risk_resources_shown")

    out2 = run_inference("inner_me", "I want to end my life", "S1", p)
    assert out2.get("meta", {}).get("risk_resources_shown") == "reminder"

    out3 = run_inference("inner_me", "I want to die", "S2", p)
    meta3 = out3.get("meta", {})
    assert meta3.get("risk_resources_shown")  # new session gets full list