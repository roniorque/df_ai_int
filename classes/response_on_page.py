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

class SeoOn:
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
        x = mycol.find_one({"data_field": data_field})
        x = x["result"]
        return x

    def process(self):
                with st.spinner('SEO On Page...', show_time=True):
                        st.write('')
                        # OUTPUT FOR SEO ANALYST
                        headers = {"Content-Type": "application/json", "x-api-key": f"{os.getenv('x-api-key')}"}
                        payload = ""
                        try:
                             payload += self.fetch_data("First Meaningful Paint")
                        except Exception as e:
                            pass
                        try:
                             payload += self.fetch_data("Crawl File")
                        except Exception as e:
                            pass

                        try:
                            session_first_meaningful_paint = st.session_state['first_meaningful_paint']
                            session_crawl_file = st.session_state['crawl_file']
                            if session_first_meaningful_paint or session_crawl_file == 'uploaded':
                                payload_txt = {"input_value": payload, "output_type": "text", "input_type": "chat"}
                                payload_txt_model = self.request_model(payload_txt, headers)
                                debug_info = {'data_field' : 'On Page Analyst', 'result': payload_txt_model}
                                upload_response(debug_info)

                                st.session_state['first_meaningful_paint'] = ''
                                st.session_state['crawl_file'] = ''
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
           
            #st.write("") # FOR THE HIDE BUTTON
            #st.write("") # FOR THE HIDE BUTTON
            #st.write("AI Analyst Output: ")
            st.session_state['analyzing'] = False
            #st.write("") # FOR THE HIDE BUTTON
            self.process()
                 

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()