from __future__ import annotations

def render_skill(name: str, style: str = "adult", context: dict | None = None) -> str:
    # TODO: implement skills
    return f"[skill:{name}] (style={style})"

def list_skills() -> list[str]:
    return ["grounding_5_4_3_2_1","paced_breathing","cbt_thought_record"]
