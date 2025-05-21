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

class PullThroughOffers:
    def __init__(self, model_url):
        self.model_url = model_url
        #self.analyst_name = analyst_name
        #self.data_src = data_src
        #self.analyst_description = analyst_description
        self.initialize()
        
        self.row1()

    def initialize(self):
        # FOR ENV
        load_dotenv()

        if 'pull_through_offers' not in st.session_state:
            st.session_state['pull_through_offers'] = ''
    
    def process(self):
                session = st.session_state.analyze
                if (self.pull_through_offers) and session == 'clicked':
                    pull_through_offers = ""
                    with st.spinner('Uploading Pull Through Offers...', show_time=True):
                        st.write('')
                        
                        try:
                            pull_through_offers += f"\nPull Through Offers: {self.pull_through_offers}"
                        except KeyError:
                            pass
                        
                        self.competitor_name = st.session_state.competitor_name
                        self.is_competitor = st.session_state.is_competitor
                        pull_through_offers = self.competitor_name + pull_through_offers if self.is_competitor == True else pull_through_offers
                        
                        if self.is_competitor:
                            debug_info_pull_through_offers = {'data_field' : 'Pull through offers Competitor', 'result': pull_through_offers}
                        else:
                            debug_info_pull_through_offers = {'data_field' : 'Pull through offers', 'result': pull_through_offers}

                        if self.pull_through_offers:
                            st.session_state['pull_through_offers'] = 'uploaded'
                            collect_telemetry(debug_info_pull_through_offers)
                       
                        
                            
                        #with st.expander("Debug information", icon="⚙"):
                        #    st.write(debug_info)


                        st.session_state['analyzing'] = False
                                             
    def row1(self):
            
            self.pull_through_offers = st.text_input("Pull through offers (Business Context):", placeholder='Enter Pull through offers')
            
            st.session_state['analyzing'] = False

            self.process()

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()