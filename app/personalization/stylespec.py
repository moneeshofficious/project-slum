from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

Tone = Literal["warm", "neutral", "direct"]
Pacing = Literal["slow", "normal", "fast"]

@dataclass
class StyleSpec:
    reading_level: Literal["simple","standard"] = "standard"
    tone: Tone = "warm"
    pacing: Pacing = "normal"
    pronouns: str = "they/them"
    language: str = "en"
    culture_notes: str = ""
    accessibility: dict[str, bool] = None  # e.g., {"large_text": True}

def style_for(profile: dict) -> StyleSpec:
    # TODO: map real profile data; safe defaults for now
    return StyleSpec()

def apply_style(reply: str, stylespec: StyleSpec) -> str:
    # TODO: real transformations (length/tone/pronouns)
    return reply
