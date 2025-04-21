import streamlit as st
import threading
from dotenv import load_dotenv
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button
from helper.initialize_analyze_session import initialize_analyze_session


class ClientSummary:
    def __init__(self):
        self.initialize()
        self.row1()

    def initialize(self):
        load_dotenv()
        for key in ['client_summary', 'client_name', 'client_website', 'target_market']:
            if key not in st.session_state:
                st.session_state[key] = ''

    def run_in_background(self):
        try:
            client_summary = f"Client Summary: {self.client_summary}\n" if self.client_summary else ""
            client_name = f"{self.name}\n" if self.name else ""
            client_website = f"{self.website}\n" if self.website else ""

            debug_client_summary = {'data_field': 'Client Summary', 'result': client_summary}
            debug_client_name = {'data_field': 'Client Name', 'result': client_name}
            debug_client_website = {'data_field': 'Client Website', 'result': client_website}

            if self.client_summary:
                st.session_state['client_summary'] = 'uploaded'
                st.session_state['target_market'] = 'uploaded'
                collect_telemetry(debug_client_summary)
            if self.name:
                st.session_state['client_name'] = 'uploaded'
                collect_telemetry(debug_client_name)
            if self.website:
                st.session_state['client_website'] = 'uploaded'
                collect_telemetry(debug_client_website)

        except Exception as e:
            st.error(f"Error during Client Summary processing: {e}")

        st.session_state['analyzing'] = False

    def process(self):
        with st.spinner('Uploading Client Details...'):
            thread = threading.Thread(target=self.run_in_background)
            thread.start()

    def row1(self):
        self.client_summary = st.text_area("Client Summary:", help="Name of business, nature of business, location, products/services")
        self.name = st.text_input("Client Name:")
        self.website = st.text_input("Client Website:")

        session = st.session_state.get('analyze')
        if (self.client_summary or self.name or self.website) and session == 'clicked':
            self.process()


if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
