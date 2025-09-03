# app/state/machine.py
"""
Bridge shim so imports like `from app.state.machine import ...`
work even if your project already uses app.state.state_machine.
"""
from __future__ import annotations
from enum import Enum

try:
    # Prefer your existing implementation if present
    from app.state.state_machine import (  # type: ignore[assignment]
        ConversationState as _ConversationState,  # if you use this name
        advance_state as _advance_state,
    )
    ConversationState = _ConversationState  # type: ignore[reportGeneralTypeIssues]
    advance_state = _advance_state  # type: ignore[reportGeneralTypeIssues]
except Exception:
    class ConversationState(str, Enum):
        warm_in = "warm_in"
        assess = "assess"
        plan = "plan"
        close = "close"
    def advance_state(current: ConversationState, signal: str) -> ConversationState:  # type: ignore[override]
        if current == ConversationState.warm_in:
            return ConversationState.assess
        return current
