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
from pymongo import MongoClient
import json
from helper.data_field import data_field
from helper.upload_response import upload_response

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

        # AGENT NAME
        #st.header(self.analyst_name)

        # EVALUATION FORM LINK
        #url = os.getenv('Link')
        #st.write('Evaluation Form: [Link](%s)' % url)

        # RETURN BUTTON
        '''try:
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
        #st.write(text)
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
        
        x = x["result"]
        return x

    def process(self):
                with st.spinner('Content Analyst...', show_time=True):
                        st.write('')       
                        headers = {"Content-Type": "application/json", "x-api-key": f"{os.getenv('x_api_key')}"}                                     
                        try:
                            payload_txt = {"input_value": self.payload, "output_type": "text", "input_type": "chat"}
                            payload_txt_model = self.request_model(payload_txt, headers)
                            debug_info = {'data_field' : 'Content Analyst', 'result': payload_txt_model}
                            upload_response(debug_info)

                            st.session_state['content_in_the_website'] = ''  
                            st.session_state['content_outside_the_website'] = ''  

                            count = 0
                        except Exception as e:
                            pass
                       
                    
                        #end_time = time.time()
                        #time_lapsed = end_time - start_time

                        #debug_info = {'data_field' : 'GT Metrix', 'result': result}
                        
                        
                        '''
                        debug_info = {#'analyst': self.analyst_name,
                                      'url_uuid': self.model_url.split("-")[-1],
                                      'time_lapsed' : time_lapsed, 
                                    'crawl_file': [file.name for file in self.uploaded_files] if self.uploaded_files else ['Not available'],
                                      'gt_metrix': [file.name for file in self.gtmetrix] if self.gtmetrix else ['Not available'],
                                      'payload': payload_txt, 
                                      'result': result}
                        
                        if self.gtmetrix:
                            collect_telemetry(debug_info)
                        '''
 
                            
                        #with st.expander("Debug information", icon="⚙"):
                        #    st.write(debug_info)
                        

                        st.session_state['analyzing'] = False
                        try:
                            self.file_dict.popitem()
                        except KeyError:
                            pass
                        
    def row1(self):
            st.session_state['analyzing'] = False
            self.payload = ""
            count = 0

            try:
                session_content_in_the_website = st.session_state['content_in_the_website']
                if session_content_in_the_website == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Content in the Website")
            except Exception as e:
                pass
            try:
                session_content_outside_the_website = st.session_state['content_outside_the_website']
                if session_content_outside_the_website == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Content outside the Website")
            except Exception as e:
                pass
            
            if count >= 1:
                summary = self.fetch_data("Client Summary")
                self.payload = summary + self.payload
                self.process()
                 
if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()