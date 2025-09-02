# app/personalization/style.py
from typing import Dict, Any

class StyleSpec(Dict[str, Any]):
    pass

def style_for(profile: Dict[str, Any]) -> StyleSpec:
    defaults = {"tone": "warm", "pacing": "normal", "address": "you", "reading_level": "plain"}
    return StyleSpec({**defaults, **(profile or {})})

def apply_style(reply: Dict[str, Any], stylespec: StyleSpec) -> Dict[str, Any]:
    # Minimal: attach stylespec so UI can render tone/pacing later
    reply["style"] = dict(stylespec)
    return reply
