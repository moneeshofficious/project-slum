# tests/test_module1_safety.py
import json
from app.safety import safety, pre_prompt_guard, post_prompt_guard, refresh_policies

def _post(reply, pre):
    return post_prompt_guard(reply, pre.get("risk_info", {}))["reply"]

def test_golden_dialogs_module1():
    refresh_policies()  # ensure latest YAML loaded
    data = json.load(open("tests/conversations/golden_module1.json", "r", encoding="utf-8"))
    for case in data:
        pre = pre_prompt_guard(case["user"], {"session_id": "golden-1", "age_band": "adult"})
        exp = case["expect"]

        if "pre.risk" in exp:
            assert pre["risk"] == exp["pre.risk"]

        if "pre.action" in exp:
            assert pre["action"] == exp["pre.action"]

        if "pre.categories" in exp:
            for c in exp["pre.categories"]:
                assert c in pre["categories"]

        if "pre.text_contains" in exp:
            assert exp["pre.text_contains"].lower() in pre["text"].lower()

        post = _post({"sections": {"body": case["user"]}}, pre)

        if "post.contains" in exp:
            text = post if isinstance(post, str) else json.dumps(post)
            assert exp["post.contains"].lower() in text.lower()
