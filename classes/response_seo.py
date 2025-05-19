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
from pymongo import MongoClient
from helper.data_field import data_field
from helper.upload_response import upload_response
import json

class Seo:
    def __init__(self, model_url):
        self.uploaded_files = []
        self.file_dict = {}
        self.model_url = model_url
        self.run_all = (st.session_state.get('run_all', {}))
        #self.analyst_name = analyst_name
        #self.data_src = data_src
        #self.analyst_description = analyst_description
        self.initialize()
        self.row1()

    def initialize(self):
        # FOR ENV
        load_dotenv()

        # AGENT NAME
        #st.header(self.analyst_name)

        # EVALUATION FORM LINK
        '''url = os.getenv('Link')
        st.write('Evaluation Form: [Link](%s)' % url)

        # RETURN BUTTON
        try:
            if st.button("Return", type='primary'):
                st.switch_page("./pages/home.py")
        except Exception:
            pass'''
    
    def request_model(self, payload_txt, headers):
        response = requests.post(self.model_url, json=payload_txt, headers=headers)
        response.raise_for_status()
        output = response.json()
        #st.write(output)
        text = output["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
        text = json.loads(text)
        return text
    
       
    def fetch_data(self, data_field):
        mongodb_uri = os.getenv("MONGODB_URI")
        myclient = MongoClient(mongodb_uri)
        mydb = myclient.get_database()
        mycol = mydb["df_data"]
        
        # Sort by timestamp field in descending order
        x = mycol.find_one(
            {"data_field": data_field},
            sort=[("timestamp", -1)]  
        )
        
        try:
            if x is None:
                st.session_state[data_field] = ''
                return ''
        except Exception:
            pass
        x = x["result"]
        return x
    
    def process (self):    
        with st.spinner('Seo Analyst...', show_time=True):
                        st.write('')
                        headers = {"Content-Type": "application/json", "x-api-key": f"{os.getenv('x_api_key')}"}         
                        try:
                                payload_txt = {"input_value": self.payload, "output_type": "text", "input_type": "chat"}
                                payload_txt_model = self.request_model(payload_txt, headers)
                                debug_info = {'data_field' : 'SEO Analyst', 'result': payload_txt_model}
                                upload_response(debug_info)

                                st.session_state['bounce_rate'] = ''
                                st.session_state['pages_index'] = ''
                                st.session_state['seo_scope'] = ''
                                st.session_state['others'] = ''
                                st.session_state['df_traffic'] = ''
                                st.session_state['df_seo'] = ''
                                
                        except Exception as e:
                            pass
                        st.session_state['analyzing'] = False    
             
    def row1(self):
            st.session_state['analyzing'] = False
            #st.write("") # FOR THE HIDE BUTTON
            #analyze_button = st.button("Analyze", disabled=initialize_analyze_session())
            self.payload = ""  
            self.payload += self.fetch_data("SEO Keywords")
        
            self.payload += self.fetch_data("Traffic Channels")
    
            self.payload += self.fetch_data("Traffic Acquisition")
    
            self.payload += self.fetch_data("Pages Indexed")            
    
            self.payload += self.fetch_data("Bounce Rate")    
            
            self.payload += self.fetch_data("SEO Scope")   

            self.payload += self.fetch_data("Backlinks") 
            
            summary = self.fetch_data("Client Summary")
            self.payload = summary + self.payload
            self.process()
            

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
