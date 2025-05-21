import streamlit as st
import requests
import json
from helper.upload_response import upload_response

# === CONFIG ===
AGENT_URL = "http://172.17.21.23:7860/api/v1/run/51b63d7f-c30b-4df4-b591-6544d60b2f0c?stream=false"

# === FUNCTIONS ===
def parseable(report_title):
    """
    Check if the report title is parseable.
    """
    parseable_titles = ["Target Market Analyst", "SEM/PPC", "SEO", "Social Media", "Content", "Marketplace"]
    return report_title in parseable_titles

def render_agent_reply(reply):
    def try_parse_json(text):
        try:
            return json.loads(text)
        except Exception:
            return None

    parsed = try_parse_json(reply)
    placeholder = st.empty()
    
    # Handle dictionary response
    if parseable(st.session_state.report_title) and isinstance(parsed, dict):
        with placeholder.container():
            for key, value in parsed.items():
                # Convert key from snake_case to Title Case for display
                display_key = key.replace('_', ' ').title()
                st.markdown(f"### {display_key}")
                st.markdown(value)
                st.markdown("---")
    # Handle list of dictionaries (existing logic)
    elif isinstance(parsed, list) and all(isinstance(item, dict) for item in parsed):
        for idx, item in enumerate(parsed):
            if "elements" in item:
                label = item.get("elements", f"Item {idx + 1}")
                with placeholder.expander(label, expanded=True):
                    for k, v in item.items():
                        if k != "elements":
                            st.markdown(f"**{k}**: {v}")
    # Fallback for non-JSON or other formats
    else:
        placeholder.write(reply)

def save_output(output):
    if parseable(st.session_state.report_title):
        try:
            output = json.loads(output)
        except TypeError:
            st.error("Output is not JSON serializable.")
            return
    ai_response = {'data_field': st.session_state.report_title, 'result': output}
    upload_response(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": "✅ Output saved."})
    st.session_state.latest_reply = output  # Update the session state
    st.session_state.saved_reply = output   # Track the saved state
    # st.rerun()

# === STATE INIT ===
if "messages" not in st.session_state:
    st.session_state.messages = []

st.session_state.latest_reply = st.session_state.chat_text

session_id = st.session_state.session_id

# === LAYOUT ===
    
st.set_page_config(page_title="Langflow Collaborative Chat", page_icon="💬", layout="wide")

if st.button("Back to Output Review"):
    st.session_state.messages = []
    if "saved_reply" in st.session_state:
        del st.session_state.saved_reply
    st.switch_page("pages/output.py")
    
st.title("🤖 Digital Footprint AI Collaborative Workspace")

left_col, right_col = st.columns([1, 1])

# === LEFT PANE: Chat ===
with left_col:
    st.subheader("💬 Chat")
    with st.container(height=500, border=False):
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("Give an instruction..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        try:
            payload = { 
                        "session_id": session_id,
                        "input_type": "chat",
                        "output_type": "chat",
                        "input_value":prompt,
                        "tweaks": {
                            "DataInput-jFbIt": {"input_value": json.dumps(st.session_state.latest_reply)}
                        } 
                    }
            # st.write(f"Payload: {payload}")
            response = requests.post(
                AGENT_URL,
                json=payload,
                timeout=3600
            )
            response.raise_for_status()
            result = response.json()
            reply = result["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
            st.session_state.latest_reply = reply  # Update the session state here
        except Exception as e:
            reply = f"❌ Error: {e}"
            st.session_state.latest_reply = reply  # Ensure session state is updated even on error

        # Immediately show output in right pane after AI responds
        with right_col:
            st.subheader("📄✨ Editing " + st.session_state.report_title)
                
            with st.container(border=True):
                render_agent_reply(reply)  # Render the updated value
                st.button("Save Output", on_click=save_output, args=(reply,))  # Pass the latest reply
            
            with st.expander("Debug Info", expanded=False):
                st.markdown(f"**Session ID**: {session_id}")
                st.markdown(f"**Payload**: {payload}")
                st.markdown(f"**Response**: {reply}")

        # Append assistant's update note after rendering to avoid input field being pushed
        st.session_state.messages.append({"role": "assistant", "content": "✅ Output updated in right panel."})

# === RIGHT PANE: Output (initial or fallback render) ===
if not prompt:
    with right_col:
        st.subheader("📄✨ Editing " + st.session_state.report_title)
        with st.container(border=True):
            # Use saved_reply if available, otherwise use latest_reply
            display_reply = st.session_state.get('saved_reply', st.session_state.latest_reply)
            render_agent_reply(display_reply)