from __future__ import annotations

def build_messages(mode: str, state: str, style: object, memory: str, user_msg: str) -> list[dict]:
    return [{"role":"system","content":f"mode={mode} state={state}"},{"role":"user","content":user_msg}]

def infer(messages: list[dict]) -> dict:
    # TODO: call model; return structured reply
    return {"text":"ok"}
