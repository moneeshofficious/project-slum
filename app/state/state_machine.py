# app/state/state_machine.py
from typing import Literal

State = Literal["WarmIn", "Assess", "Formulate", "Intervene", "Plan", "Safety", "Close"]

def current_state(session_id: str) -> State:
    # Placeholder: later persist in DB
    return "Assess"
