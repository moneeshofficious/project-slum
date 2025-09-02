# ui/Home.py
# --- robust project-root on sys.path (handles "ui/" working dir) ---
import sys
from pathlib import Path
from app.safety.safety import needs_consent, get_consent_text, record_consent
from app.observability import metrics

USER_ID = "local_user"  # later we’ll store real IDs
THIS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = THIS_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
# -------------------------------------------------------------------


from app.orchestrator.pipeline import run_inference
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

st.set_page_config(page_title="SLUM Counseling AI", layout="centered")

st.title("SLUM — Counseling AI (Local)")

# --- Consent banner ---
if needs_consent(user_id=USER_ID):
    with st.expander("Consent & Privacy — please read", expanded=True):
        st.markdown(get_consent_text())
        ack = st.checkbox("I understand and agree to continue using this supportive tool.", value=False)
        if not ack:
            st.info("Please tick the box above to continue.")
            st.stop()
        else:
            record_consent(USER_ID)      
            metrics.inc(metrics.CONSENT_ACCEPT)

# --- Input controls ---
mode = st.radio("Mode", ["inner_me", "mate"], index=0, horizontal=True)
user_msg = st.text_area("Say something…", height=120)
profile = {
    "age_band": st.selectbox("Age band", ["teen", "adult", "older_adult"], index=1),
    "pronouns": st.text_input("Pronouns", value="they/them"),
    "tone": st.selectbox("Tone", ["warm", "neutral"], index=0),
    "pacing": st.selectbox("Pacing", ["slow", "normal", "fast"], index=1),
    "culture_notes": st.text_input("Culture notes", value="IN"),
}

# --- Action ---
if st.button("Send"):
    out = run_inference(mode, user_msg, "local_session", profile)

    # Sections
    st.subheader("Response")
    if "sections" in out:
        for k, v in out["sections"].items():
            if isinstance(v, str):
                st.write(f"**{k.capitalize()}**: {v}")
            elif isinstance(v, list):
                st.write(f"**{k.capitalize()}**:")
                for item in v:
                    st.write(f"- {item}")

    # Risk resources (if any)
    resources = out.get("resources")
    if resources:
        st.subheader("Crisis Resources (India)")
        # Render as a simple table
        rows = []
        for r in resources:
            rows.append({
                "Name": r.get("name", ""),
                "Type": r.get("type", ""),
                "Phone": r.get("phone", ""),
                "URL": r.get("url", ""),
                "Notes": r.get("notes", ""),
            })
        # lightweight table rendering without pandas dependency in UI
        st.table(rows)

        # Copyable helplines text
        helplines_text = []
        for r in resources:
            line = f"{r.get('name','')} — {r.get('phone','').strip()} {r.get('url','')}".strip()
            helplines_text.append(line)
        helplines_blob = "\n".join(helplines_text).strip()

        st.text_area("Copy helplines", value=helplines_blob, height=120)

    # Debug / meta
    with st.expander("Details"):
        st.json(out)
