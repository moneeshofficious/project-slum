# app/safety/config.py
# -*- coding: utf-8 -*-
from __future__ import annotations

"""
Runtime policy loader for Module 1 (Safety).
- Loads policies.yaml (scope + DEI + risk + consent).
- Exposes helpers used by the safety guard and by tests.
- Provides safe defaults if the YAML is missing or malformed.
"""

import io
import json
import logging
import os
from typing import Dict, List, Any

try:
    import yaml  # type: ignore
except Exception as e:  # pragma: no cover
    raise RuntimeError("PyYAML is required for app.safety.config") from e

logger = logging.getLogger(__name__)

# -----------------------------
# Defaults used if YAML is missing
# -----------------------------
DEFAULT_SCOPE_PATTERNS: List[str] = [
    r"\b(diagnos(e|is)|prescrib(e|ing)|dose|dosage|medication advice|what meds|which meds)\b",
]
DEFAULT_REDIRECT_MESSAGE: str = (
    "I can't help with diagnosis or medications. I can’t provide diagnosis or medication advice. "
    "I can share general education and suggest speaking with a licensed clinician. If you’d like, "
    "I can help you prepare questions for your appointment."
)
DEFAULT_DEI_LEXICON: Dict[str, str] = {
    r"\bcrazy|insane\b": "feeling overwhelmed",
    r"\bmentally ill\b": "person living with a mental health condition",
    r"\bcommitted suicide\b": "died by suicide",
}

_DEFAULT_POLICIES: Dict[str, Any] = {
    "version": 1,
    "scope": {
        "block_patterns": DEFAULT_SCOPE_PATTERNS,
        "redirect_message": DEFAULT_REDIRECT_MESSAGE,
    },
    "dei": {
        "lexicon": DEFAULT_DEI_LEXICON,
    },
    "risk": {
        "throttle": {"repeat_risk_seconds": 180},
    },
    "consent": {
        "text": "We store only what you allow. You can pause, export, or delete memory anytime.",
    },
}

# -----------------------------
# Policy cache and file lookup
# -----------------------------
_POLICIES: Dict[str, Any] | None = None

def _candidate_policy_paths() -> List[str]:
    """Return candidate paths where policies.yaml might live."""
    here = os.path.dirname(__file__)
    repo_root = os.getcwd()
    return [
        os.path.join(here, "policies.yaml"),                 # app/safety/policies.yaml
        os.path.join(repo_root, "app", "safety", "policies.yaml"),
        os.path.join(repo_root, "policies.yaml"),
    ]

def _load_yaml_file(path: str) -> Dict[str, Any] | None:
    try:
        with io.open(path, "r", encoding="utf-8-sig") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            logger.warning("policies.yaml at %s is not a mapping; got %s", path, type(data).__name__)
            return None
        return data
    except FileNotFoundError:
        return None
    except Exception as e:
        logger.warning("Failed to load policies.yaml at %s: %s", path, e)
        return None

def load_policies() -> Dict[str, Any]:
    """Load policies.yaml once and cache. Falls back to safe defaults."""
    global _POLICIES
    if _POLICIES is not None:
        return _POLICIES

    for p in _candidate_policy_paths():
        data = _load_yaml_file(p)
        if data:
            _POLICIES = _normalize(data)
            logger.debug("Loaded policies from %s", p)
            return _POLICIES

    logger.warning("Using default policies; could not find a valid policies.yaml in candidates")
    _POLICIES = dict(_DEFAULT_POLICIES)
    return _POLICIES

def refresh_policies() -> Dict[str, Any]:
    """Force reload of policies.yaml (used by tests)."""
    global _POLICIES
    _POLICIES = None
    return load_policies()

# -----------------------------
# Normalization and getters
# -----------------------------
def _normalize(data: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure required keys exist and types match what tests expect."""
    out: Dict[str, Any] = dict(_DEFAULT_POLICIES)

    # version
    if isinstance(data.get("version"), int):
        out["version"] = data["version"]

    # scope
    scope_in = data.get("scope") or {}
    if isinstance(scope_in, dict):
        bp = scope_in.get("block_patterns")
        rm = scope_in.get("redirect_message")
        if isinstance(bp, list) and all(isinstance(x, str) for x in bp):
            out["scope"]["block_patterns"] = bp
        if isinstance(rm, str) and rm.strip():
            out["scope"]["redirect_message"] = rm

    # dei
    dei_in = data.get("dei") or {}
    if isinstance(dei_in, dict):
        lex = dei_in.get("lexicon")
        if isinstance(lex, dict):
            # keep keys & values as strings
            cleaned = {str(k): str(v) for (k, v) in lex.items()}
            out["dei"]["lexicon"] = cleaned

    # risk & consent (optional)
    if isinstance(data.get("risk"), dict):
        out["risk"].update(data["risk"])
    if isinstance(data.get("consent"), dict):
        out["consent"].update(data["consent"])

    return out

def get_scope_patterns() -> List[str]:
    return list(load_policies()["scope"]["block_patterns"])

def get_redirect_message() -> str:
    return str(load_policies()["scope"]["redirect_message"])

def get_dei_lexicon() -> Dict[str, str]:
    # return a copy so callers can't mutate our cache
    return dict(load_policies()["dei"]["lexicon"])

__all__ = [
    "DEFAULT_SCOPE_PATTERNS",
    "DEFAULT_DEI_LEXICON",
    "load_policies",
    "refresh_policies",
    "get_scope_patterns",
    "get_redirect_message",
    "get_dei_lexicon",
]
