# tests/test_metrics_counts.py
"""
Metrics behavior tests rely on the fallback in-memory counters.
If prometheus_client is installed, these tests only assert non-negative markers.
"""
from app.safety.safety import get_safety_guard, _metrics
from app.safety.safety import enforce_scope, _METRICS

guard = get_safety_guard()

def test_metrics_increment_on_eval():
    guard = get_safety_guard()
    before = _metrics.get_counter("safety_evaluations_total")
    _ = guard.evaluate("Hello world")  # noqa: F841
    after = _metrics.get_counter("safety_evaluations_total")
    if before != -1 and after != -1:
        assert after == before + 1

def test_decision_counters_and_latency():
    before_allow = _metrics.get_counter("safety_decision_total", {"decision": "allow"})
    _ = guard.evaluate("Just a normal message.")
    after_allow = _metrics.get_counter("safety_decision_total", {"decision": "allow"})
    if before_allow != -1 and after_allow != -1:
        assert after_allow == before_allow + 1

    # At least one latency observation exists
    assert _metrics.get_hist_count() != 0 or _metrics.get_hist_count() == -1


def test_category_and_block_counters():
    before_cat = _metrics.get_counter("safety_category_hits_total", {"category": "self_harm"})
    before_blk = _metrics.get_counter("safety_blocks_total", {"category": "self_harm"})
    _ = guard.evaluate("I want to kill myself")
    after_cat = _metrics.get_counter("safety_category_hits_total", {"category": "self_harm"})
    after_blk = _metrics.get_counter("safety_blocks_total", {"category": "self_harm"})

    if all(v != -1 for v in (before_cat, before_blk, after_cat, after_blk)):
        assert after_cat == before_cat + 1
        assert after_blk == before_blk + 1

def test_metrics_increment_on_block():
    before = _METRICS["scope_blocks_count"]
    enforce_scope("prescribe meds please")
    after = _METRICS["scope_blocks_count"]
    assert after == before + 1