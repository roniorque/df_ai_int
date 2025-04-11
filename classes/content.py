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

class Content:
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

        if 'content_in_the_website' not in st.session_state:
            st.session_state['content_in_the_website'] = ''
        if 'content_outside_the_website' not in st.session_state:
            st.session_state['content_outside_the_website'] = ''
    
    def process(self):
                session = st.session_state.analyze

                if (self.content_in_the_website or self.content_outside_the_website) and session == 'clicked':
                    with st.spinner('SEO On Page Analyst...', show_time=True):
                        st.write('')
                        content_in_the_website = ""
                        content_outside_the_website = ""
                        try:
                            content_in_the_website += f"\nContent in the Website: {self.content_in_the_website}"
                        except KeyError:
                            pass
                        try:
                            content_outside_the_website += f"\nContent outside the Website: {self.content_outside_the_website}"
                        except KeyError:
                            pass

                        debug_info_content_in_the_website = {'data_field' : 'Content in the Website', 'result': content_in_the_website}
                        debug_info_content_outside_the_website = {'data_field' : 'Content outside the Website', 'result': content_outside_the_website}

                        if self.content_in_the_website:
                            st.session_state['content_in_the_website'] = 'uploaded'
                            collect_telemetry(debug_info_content_in_the_website)
                        if self.content_outside_the_website:
                            st.session_state['content_outside_the_website'] = 'uploaded'
                            collect_telemetry(debug_info_content_outside_the_website)
                        
                            
                        #with st.expander("Debug information", icon="⚙"):
                        #    st.write(debug_info)


                        st.session_state['analyzing'] = False
                        try:
                            self.file_dict.popitem()
                        except KeyError:
                            pass
                        
    def row1(self):
            self.content_in_the_website = st.text_input("Content in the Website (Website Content)", placeholder='Enter Content in the Website')
            self.content_outside_the_website = st.text_input("Content outside the Website (Website Content)", placeholder='Enter Content outside the Website')

            self.process()

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()