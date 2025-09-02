# app/data/database.py
from typing import Any, Dict, Optional
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///app.db", future=True)

def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS profiles(
            id INTEGER PRIMARY KEY,
            user_id TEXT UNIQUE,
            data TEXT
        );
        """))
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS consents(
            user_id TEXT PRIMARY KEY,
            accepted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """))

def get_profile(user_id: str) -> Optional[Dict[str, Any]]:
    return None
