from io import StringIO
from urllib.parse import urlparse
import streamlit as st
import requests
from dotenv import load_dotenv
import os
import time
from helper.upload_response import upload_response
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button, unhide_button
from helper.initialize_analyze_session import initialize_analyze_session
import json
from pymongo import MongoClient
from helper.data_field import data_field

class SeoOffPageAnalyst:
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
    
    def request_model(self, payload_txt, headers):
        response = requests.post(self.model_url, json=payload_txt, headers=headers)
        response.raise_for_status()
        output = response.json()
        #st.write(output)
        text = output["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
        text = json.loads(text)
        #st.write(text)
        #backlinks = text[0]
        #referring_domains = text[1]

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
                with st.spinner('SEO Off Page Analyst...', show_time=True):
                        st.write('')
                        headers = {"Content-Type": "application/json", "x-api-key": f"{os.getenv('x_api_key')}"}         
                        try:
                                payload_txt = {"input_value": self.payload, "output_type": "text", "input_type": "chat"}
                                payload_txt_model = self.request_model(payload_txt, headers)
                                debug_info = {'data_field' : 'SEO Off Page Analyst', 'result': payload_txt_model}
                                upload_response(debug_info)

                                st.session_state['off_page_file_uploaded'] = ''
                                
                        except Exception as e:
                            pass
                        st.session_state['analyzing'] = False    
                      
    def row1(self):
            st.session_state['analyzing'] = False
            self.payload = ""  
            count = 0
            try:
                session_off_page_file_uploaded = st.session_state['off_page_file_uploaded']
                if session_off_page_file_uploaded == 'uploaded' or self.run_all:
                    count += 1
                    self.payload += self.fetch_data("Backlinks")
                
            except Exception as e:
                pass
            if count >= 1:
                summary = self.fetch_data("Client Summary")
                self.payload = summary + self.payload
                self.process()
                                       

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
