# app/data/models.py
"""
Minimal SQLAlchemy models that won't conflict with existing code.
If you already use raw SQL migrations (app/db/migrations/0001_init.sql), keep them.
These models are *additive*; nothing else imports them by default.
"""
from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.data.database import Base  # your existing Base/engine

class AuditLog(Base):
    __tablename__ = "audit_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event: Mapped[str] = mapped_column(String(64))
    details: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
