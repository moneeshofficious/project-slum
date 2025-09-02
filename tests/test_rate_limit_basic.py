# tests/test_rate_limit_basic.py
def test_rate_limit_sample_exists():
    import pathlib, yaml
    p = pathlib.Path("ops/rate_limit.sample.yaml")
    assert p.exists(), "Missing ops/rate_limit.sample.yaml"
    cfg = yaml.safe_load(p.read_text(encoding="utf-8"))
    assert "limits" in cfg and "default" in cfg["limits"], "rate limit keys not found"
