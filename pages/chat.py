import streamlit as st
import requests
import json

# === CONFIG ===
AGENT_URL = "http://172.17.21.23:7860/api/v1/run/51b63d7f-c30b-4df4-b591-6544d60b2f0c?stream=false"

# === FUNCTIONS ===
def render_agent_reply(reply):
    def try_parse_json(text):
        try:
            return json.loads(text)
        except Exception:
            return None

    parsed = try_parse_json(reply)

    if isinstance(parsed, list) and all(isinstance(item, dict) for item in parsed):
        for idx, item in enumerate(parsed):
            label = item.get("elements", f"Item {idx + 1}")
            with st.expander(label, expanded=True):
                for k, v in item.items():
                    if k != "elements":
                        st.markdown(f"**{k}**: {v}")
    else:
        st.write(reply)

def save_output(output):
    st.session_state.latest_reply = output
    st.session_state.messages.append({"role": "assistant", "content": output})
    st.session_state.report_title = st.session_state.latest_reply
    st.session_state.messages.append({"role": "assistant", "content": "✅ Output saved."})

# === STATE INIT ===
if "messages" not in st.session_state:
    st.session_state.messages = []

st.session_state.latest_reply = st.session_state.chat_text

session_id = st.session_state.session_id

# === LAYOUT ===
    
st.set_page_config(page_title="Langflow Collaborative Chat", page_icon="💬", layout="wide")

if st.button("Back to Output Review"):
    st.session_state.messages = []
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
                        "input_value": prompt,
                        "tweaks": {
                            "DataInput-jFbIt": {"input_value": st.session_state.latest_reply},
                            "TextInput-pR8UG": {"input_value": st.session_state.report_title}
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
        except Exception as e:
            reply = f"❌ Error: {e}"

        st.session_state.latest_reply = reply

        # Immediately show output in right pane after AI responds
        with right_col:
            st.subheader("📄 AI Output")
            render_agent_reply(st.session_state.latest_reply)
            st.button("Save Output", on_click=save_output, args=(st.session_state.latest_reply,))

        # Append assistant's update note after rendering to avoid input field being pushed
        st.session_state.messages.append({"role": "assistant", "content": "✅ Output updated in right panel."})

# === RIGHT PANE: Output (initial or fallback render) ===
if not prompt:
    with right_col:
        st.subheader("📄 AI Output")
        render_agent_reply(st.session_state.latest_reply)
        st.button("Save Output", on_click=save_output, args=(st.session_state.latest_reply,))
