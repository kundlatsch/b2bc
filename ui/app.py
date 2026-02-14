# Run the simulation interface with
# streamlit run ui/app.py

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

import streamlit as st
from peer import Peer
from protocol.message import B2BCMessage
from ui.presets import MENTAL_STATE_PRESETS
from ui.autocomplete import OPKEYS, OPTYPES, COMMON_KEYS

st.set_page_config(
    page_title="BTB/C Interactive Client",
    layout="wide",
)

st.title("🧠 BTB/C Interactive Protocol Client")
st.caption("Educational, meme-based protocol • Mascot: Carcule 🥕")

# -------------------------
# Session state
# -------------------------
if "peers" not in st.session_state:
    st.session_state.peers = {
        "Alice": Peer("Alice"),
        "Bob": Peer("Bob"),
    }

if "log" not in st.session_state:
    st.session_state.log = []

# -------------------------
# Sidebar — Peer Management
# -------------------------
with st.sidebar:
    st.header("🤖 Peers")

    for name in list(st.session_state.peers.keys()):
        st.write(f"• {name}")

    new_peer = st.text_input("Add peer")
    if st.button("Create peer") and new_peer:
        st.session_state.peers[new_peer] = Peer(new_peer)

    st.divider()
    st.header("🧠 Mental State Presets")

    preset = st.selectbox("Preset", MENTAL_STATE_PRESETS.keys())
    target_peer = st.selectbox("Apply to", st.session_state.peers.keys())

    if st.button("Apply preset"):
        peer = st.session_state.peers[target_peer]
        peer.state.data.clear()
        for k, v in MENTAL_STATE_PRESETS[preset].items():
            peer.state.set(k, v)

# -------------------------
# Protocol Console
# -------------------------
col1, col2, col3 = st.columns([2, 3, 3])

with col1:
    st.subheader("📨 Send Message")

    sender = st.selectbox("From", st.session_state.peers.keys())
    receiver = st.selectbox("To", st.session_state.peers.keys())

    opkey = st.selectbox("Operation", OPKEYS)
    optype = st.selectbox("Type", OPTYPES.get(opkey, [""]))
    key = st.selectbox("Key", COMMON_KEYS + ["<custom>"])

    if key == "<custom>":
        key = st.text_input("Custom key")

    value = st.text_input("Value")

    if st.button("Send"):
        msg = B2BCMessage.create(
            opkey=opkey,
            optype=optype,
            key=key,
            value=value,
        )

        responses = st.session_state.peers[sender].send(
            st.session_state.peers[receiver],
            msg
        )

        st.session_state.log.append(
            f"{sender} → {receiver}: {msg.serialize()}"
        )

        if responses:
            if isinstance(responses, list):
                for r in responses:
                    st.session_state.log.append(f"↳ {r.serialize()}")
            else:
                st.session_state.log.append(f"↳ {responses.serialize()}")

# -------------------------
# State Viewer
# -------------------------
with col2:
    st.subheader("🧩 Mental State")

    selected = st.selectbox("Inspect peer", st.session_state.peers.keys())
    state = st.session_state.peers[selected].state.data

    if state:
        st.json(state)
    else:
        st.info("Empty mental state")

# -------------------------
# Event Log / EMIT
# -------------------------
with col3:
    st.subheader("📡 Protocol Log")

    log_box = st.container()
    for entry in reversed(st.session_state.log[-20:]):
        log_box.markdown(f"`{entry}`")

    if st.button("Clear log"):
        st.session_state.log.clear()
