# tests/test_specs_exist_and_load.py
import re
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from utils_config_loader import load_policies, load_resources, load_consent_md


def test_policies_yaml_loads_and_has_keys():
    p = load_policies()
    assert p["version"] >= 1
    assert "scope" in p and "dei" in p and "risk" in p and "consent" in p
    assert isinstance(p["scope"]["block_patterns"], list)
    assert "redirect_message" in p["scope"]

def test_resources_json_loads_and_has_entries():
    r = load_resources()
    assert isinstance(r, list) and len(r) >= 3
    assert any("Emergency" in x or "112" in x for x in r)

def test_consent_markdown_has_required_headings():
    md = load_consent_md()
    assert "# Consent & Privacy" in md
    # allow straight or curly apostrophe
    assert re.search(r"won[’']?t provide diagnosis or medication advice", md, re.I)