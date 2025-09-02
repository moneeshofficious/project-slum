from __future__ import annotations
from enum import Enum

class ConvState(str, Enum):
    WARM_IN="warm_in"; ASSESS="assess"; FORMULATE="formulate"
    INTERVENE="intervene"; PLAN="plan"; SAFETY="safety"; CLOSE="close"

def advance_state(state: ConvState, signal: dict) -> ConvState:
    # TODO: add real rules; keep identity for now
    return state

def current_state(session_id: str) -> ConvState:
    # TODO: wire to session store
    return ConvState.WARM_IN
