# tests/test_adversarial_basic.py
from __future__ import annotations

def test_adversarial_placeholders():
    # This ensures eval files are loadable and contain basic structure
    import json, pathlib
    base = pathlib.Path("tests/conversations")
    files = list(base.glob("*.json"))
    assert files, "No golden dialogs found in tests/conversations/"
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        assert isinstance(data, (list, dict)), f"{f} is not JSON list/dict"
