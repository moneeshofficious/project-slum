# tests/utils_config_loader.py
import json, os, yaml

BASE = os.path.join(os.path.dirname(__file__), "..", "app", "safety")

def load_policies():
    path = os.path.abspath(os.path.join(BASE, "policies.yaml"))
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_resources():
    path = os.path.abspath(os.path.join(BASE, "resources_in.json"))
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_consent_md():
    path = os.path.abspath(os.path.join(BASE, "consent.md"))
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
