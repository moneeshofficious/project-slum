# app/safety/config.py
"""
Runtime loader for safety policies (YAML).
- Reads app/safety/policies.yaml by default.
- Can be overridden with env SAFETY_POLICY_PATH.
- Provides safe fallbacks if file is missing or malformed.
"""
from __future__ import annotations
import os, json, re, logging
from functools import lru_cache
from typing import Dict, List, Tuple, Pattern, Any

logger = logging.getLogger(__name__)
DEFAULT_REDIRECT = (
    "I can’t help with diagnosis or medications. "
    "I can’t provide diagnosis or medication advice. "
    "I can share general education and suggest speaking with a licensed clinician. "
    "If you’d like, I can help you prepare questions for your appointment."
)
DEFAULT_SCOPE_PATTERNS = [
    r"(?i)\bdiagnos(e|is)\b",
    r"(?i)\bprescrib(e|ption)\b",
    r"(?i)\bwhich\s+meds?\b",
    r"(?i)\bwhat\s+(medicine|medication)s?\b",
    r"(?i)\bwhat\s+dose\b",
    r"(?i)\bdose\s+of\b",
]
DEFAULT_DEI_LEXICON: Dict[str, str] = {
    r"(?i)\baddict|junkie\b": "person with a substance use problem",
    r"(?i)\bmentally\s+ill\b": "person living with a mental health condition",
    r"(?i)\bcrippled\b": "person with a disability",
    r"(?i)\bcrazy|insane\b": "feeling overwhelmed",
}

@lru_cache(maxsize=1)
def load_policies() -> Dict[str, Any]:
    path = os.environ.get("SAFETY_POLICY_PATH")
    if not path:
        path = os.path.join(os.path.dirname(__file__), "policies.yaml")
    data: Dict[str, Any] = {}
    try:
        import yaml  # type: ignore
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except FileNotFoundError:
        logger.warning("policies.yaml not found at %s; using defaults", path)
    except Exception as e:
        logger.warning("Failed to load policies.yaml (%s): %s; using defaults", path, e)
    return data

def get_scope_patterns() -> List[str]:
    p = load_policies()
    patterns = (((p.get("scope") or {}).get("block_patterns")) or []) if isinstance(p, dict) else []
    if not patterns:
        return list(DEFAULT_SCOPE_PATTERNS)
    return [str(s) for s in patterns]

def get_redirect_message() -> str:
    p = load_policies()
    msg = ((p.get("scope") or {}).get("redirect_message")) if isinstance(p, dict) else None
    msg = str(msg).strip() if msg else ""
    return msg or DEFAULT_REDIRECT

def get_dei_lexicon() -> Dict[str, str]:
    p = load_policies()
    lex = ((p.get("dei") or {}).get("lexicon")) if isinstance(p, dict) else None
    if isinstance(lex, dict) and lex:
        # YAML may carry regex as keys; ensure string mapping
        return {str(k): str(v) for k, v in lex.items()}
    return dict(DEFAULT_DEI_LEXICON)
