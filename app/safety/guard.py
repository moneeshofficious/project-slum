# app/safety/guard.py
from typing import Dict, Any
from app.observability.logging_cfg import get_logger

log = get_logger(__name__)

BLOCK_WORDS = ["diagnose me", "which meds", "prescribe", "dose"]
RISK_HINTS = ["suicide", "kill myself", "end my life", "self-harm"]

def pre_prompt_safety(text: str, profile: Dict[str, Any]) -> str:
    t = text.lower()
    if any(w in t for w in BLOCK_WORDS):
        log.info("scope.block")
        return "I can’t provide diagnosis or medication advice. I can share educational info and suggest talking to a licensed professional. How can I support you right now?"
    if any(w in t for w in RISK_HINTS):
        log.info("risk.detect")
        return (
            "I'm really glad you told me. You deserve support right now. "
            "If you’re in India and need immediate help, you can call 112 or Tele MANAS (14416). "
            "Would you like me to share more crisis resources?"
        )
    return text

def post_prompt_safety(reply: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
    # Placeholder for DEI rephrasing / resource injection
    reply["meta"] = {"dei_rewrite": False, "risk_resources_shown": False}
    return reply
