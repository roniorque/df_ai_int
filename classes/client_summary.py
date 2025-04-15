import streamlit as st
from dotenv import load_dotenv
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button
from helper.initialize_analyze_session import initialize_analyze_session


class CientSummary:
    def __init__(self):
        self.initialize()
        self.row1()

    def initialize(self):
        # FOR ENV
        load_dotenv()
        if 'client_summary' not in st.session_state:
            st.session_state['client_summary'] = ''
        if 'client_name' not in st.session_state:
            st.session_state['client_name'] = ''
        if 'client_website' not in st.session_state:
            st.session_state['client_website'] = ''
        if 'target_market' not in st.session_state:
            st.session_state['target_market'] = ''
    
    def process (self):
            with st.spinner('Seo Analyst...', show_time=True):
                        st.write('')
                        client_summary = ""
                        client_name = ""
                        client_website = ""
                        # 
                        client_summary = f"Client Summary: {self.client_summary}\n"
                        client_name = f"{self.name}\n"
                        client_website = f"{self.website}\n"

                        debug_client_summary = {'data_field' : 'Client Summary', 'result': client_summary}
                        debug_client_name = {'data_field' : 'Client Name', 'result': client_name}
                        debug_client_website = {'data_field' : 'Client Website', 'result': client_website}

                        if self.client_summary:
                            st.session_state['client_summary'] = 'uploaded'
                            st.session_state['target_market'] = 'uploaded'
                            collect_telemetry(debug_client_summary)
                        if self.name:
                            st.session_state['client_name'] = 'uploaded'
                            collect_telemetry(debug_client_website)
                        if self.website:
                            st.session_state['client_website'] = 'uploaded'
                            collect_telemetry(debug_client_name)
             
    def row1(self):
            self.client_summary = st.text_area("Client Summary:", help="Name of business, nature of business, location, products/services")
            session = st.session_state.analyze
            self.name = st.text_input("Client Name:")
            self.website = st.text_input("Client Website:")

            if (self.client_summary or self.name or self.website) and session == 'clicked':
                self.process()


if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
