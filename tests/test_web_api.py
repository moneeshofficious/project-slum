# tests/test_web_api.py
from fastapi.testclient import TestClient
from app.web.main import app

def test_health():
    c = TestClient(app)
    r = c.get("/health")
    assert r.status_code == 200
    assert r.json().get("ok") is True

def test_chat_basic():
    c = TestClient(app)
    r = c.post("/chat", json={"user_msg":"hello","profile":{"tone":"Warm"}})
    assert r.status_code == 200
    data = r.json()
    assert "reply" in data and "mode" in data
