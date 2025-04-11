import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import pandas._libs.tslibs.parsing
import time
import chardet
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
    
    def process (self):
            with st.spinner('Seo Analyst...', show_time=True):
                        st.write('')
                        client_summary = ""
                        # INITIALIZING SESSIONS
                        client_summary += f"Client Summary: {self.client_summary}\n"

                        debug_client_summary = {'data_field' : 'Client Summary', 'result': client_summary}
                        
                        if self.client_summary:
                            st.session_state['client_summary'] = 'uploaded'
                            collect_telemetry(debug_client_summary)
             
    def row1(self):
            self.client_summary = st.text_area("Client Summary:", help="Name of business, nature of business, location, products/services")
            session = st.session_state.analyze
            if self.client_summary and session == 'clicked':
                self.process()

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
