import streamlit as st
import requests
from dotenv import load_dotenv
import os
import time
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button, unhide_button
from helper.initialize_analyze_session import initialize_analyze_session
import pandas as pd

class LLD_PM_LN:
    def __init__(self, model_url):
        self.uploaded_files = []
        self.file_dict = {}
        self.file_gt = {}
        self.model_url = model_url
        #self.analyst_name = analyst_name
        #self.data_src = data_src
        #self.analyst_description = analyst_description
        self.initialize()
        
        self.row1()

    def initialize(self):
        # FOR ENV
        load_dotenv()

       
        if 'lead_generation_mechanism' not in st.session_state:
            st.session_state['lead_generation_mechanism'] = ''
    
    def process(self):
                session = st.session_state.analyze
                if (self.lead_generation_mechanism) and session == 'clicked':
                    lead_generation_mechanism = ""
                    with st.spinner('Uploading Lead Generation...', show_time=True):
                        st.write('')

                        try:
                            lead_generation_mechanism += f"\nLead Generation Mechanism: {self.lead_generation_mechanism}"
                        except KeyError:
                            pass
                        
                        self.competitor_name = st.session_state.competitor_name
                        self.is_competitor = st.session_state.is_competitor
                        lead_generation_mechanism = self.competitor_name + lead_generation_mechanism if self.is_competitor == True else lead_generation_mechanism

                        if self.is_competitor:
                            debug_info_lead_generation_mechanism = {'data_field' : 'Lead Generation Mechanism Competitor', 'result': lead_generation_mechanism}
                        else:
                            debug_info_lead_generation_mechanism = {'data_field' : 'Lead Generation Mechanism', 'result': lead_generation_mechanism}
             
                        if self.lead_generation_mechanism:
                            st.session_state['lead_generation_mechanism'] = 'uploaded'
                            collect_telemetry(debug_info_lead_generation_mechanism)
                                
                        #with st.expander("Debug information", icon="⚙"):
                        #    st.write(debug_info)


                        st.session_state['analyzing'] = False
                        try:
                            self.file_dict.popitem()
                        except KeyError:
                            pass
                        
    def row1(self):        
            self.lead_generation_mechanism = st.text_input("Lead Generation Mechanism - Business Context (Lead Generation & Lead Nurturing):", placeholder='Enter Lead Generation Mechanism')
            st.session_state['analyzing'] = False
            
            self.process()

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()