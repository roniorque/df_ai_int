import streamlit as st
import requests
import json
from helper.upload_response import upload_response
from dotenv import load_dotenv
import os

# === LOGIN CHECK ===
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.switch_page('app.py')
    st.stop()

# === CONFIG ===
load_dotenv()
AGENT_URL = os.getenv("AGENT_URL")
PARSEABLE_TITLES = [
    "Target Market Analyst", "Conversion Analyst", "Content - Process and Assets Analyst",
    "LLD/PM/LN Analyst", "Content", "Marketplace"
]

# === UTILS ===
def is_parseable(title):
    return title in PARSEABLE_TITLES 

def try_parse_json(text):
    try:
        return json.loads(text)
    except Exception:
        return None

def render_agent_reply(reply):
    parsed = try_parse_json(reply)
    placeholder = st.empty()

    if is_parseable(st.session_state.report_title) and isinstance(parsed, dict):
        with placeholder.container():
            for key, value in parsed.items():
                st.markdown(f"### {key.replace('_', ' ').title()}")
                st.markdown(value)
                st.markdown("---")
    elif isinstance(parsed, list) and all(isinstance(item, dict) for item in parsed):
        for idx, item in enumerate(parsed):
            label = item.get("elements", f"Item {idx + 1}")
            with placeholder.expander(label, expanded=True):
                for k, v in item.items():
                    if k != "elements":
                        st.markdown(f"**{k}**: {v}")
    else:
        placeholder.write(reply)

def save_output(output):
    if is_parseable(st.session_state.report_title):
        try:
            output = json.loads(output)
        except TypeError:
            st.error("Output is not JSON serializable.")
            return

    ai_response = {
        'data_field': st.session_state.report_title,
        'result': output
    }
    # IF TABULAR DATA, GET THE RESULT FIRST, INJECT THE OTHER FINDINGS AND SAVE DOCUMENTS
    
    upload_response(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": "✅ Output saved."})
    st.session_state.latest_reply = output
    st.session_state.saved_reply = output

def post_prompt(prompt):
    inital_analysis = st.session_state.latest_reply
    if is_parseable(st.session_state.report_title):
        inital_analysis = json.dumps(st.session_state.latest_reply)
    payload = {
        "session_id": st.session_state.session_id,
        "input_type": "chat",
        "output_type": "chat",
        "input_value": prompt,
        "tweaks": {
            "TextInput-U9c9a": {"input_value": st.session_state.client_context},
            "DataInput-jFbIt": {"input_value": inital_analysis}
        }
    }

    try:
        response = requests.post(AGENT_URL, json=payload, timeout=3600)
        response.raise_for_status()
        return response.json()["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"], payload
    except Exception as e:
        return f"❌ Error: {e}", payload

# === STATE INIT ===
st.set_page_config(page_title="Langflow Collaborative Chat", page_icon="💬", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.session_state.latest_reply = st.session_state.chat_text
report_title = st.session_state.report_title
session_id = st.session_state.session_id

# === NAVIGATION ===
if st.button("Back to Output Review"):
    st.session_state.messages.clear()
    st.session_state.pop("saved_reply", None)
    st.switch_page("pages/output.py")

# === UI HEADER ===
st.title("🤖 Digital Footprint AI Collaborative Workspace")
left_col, right_col = st.columns([1, 1])

# === LEFT PANE: CHAT ===
with left_col:
    st.subheader("💬 Chat")
    with st.container(height=500, border=False):
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("Give an instruction..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        reply, payload = post_prompt(prompt)
        st.session_state.latest_reply = reply

        with right_col:
            st.subheader("📄✨ Editing " + report_title)
            with st.container(border=True):
                render_agent_reply(reply)
                st.button("Save Output", on_click=save_output, args=(reply,))

            with st.expander("Debug Info", expanded=False):
                st.markdown(f"**Session ID**: {session_id}")
                st.markdown(f"**Payload**: {payload}")
                st.markdown(f"**Response**: {reply}")

        st.session_state.messages.append({"role": "assistant", "content": "✅ Output updated in right panel."})

# === RIGHT PANE: DEFAULT RENDER ===
if not prompt:
    with right_col:
        st.subheader("📄✨ Editing " + report_title)
        with st.container(border=True):
            display_reply = st.session_state.get('saved_reply', st.session_state.latest_reply)
            if is_parseable(report_title):
                display_reply = json.dumps(display_reply)
            render_agent_reply(display_reply)
