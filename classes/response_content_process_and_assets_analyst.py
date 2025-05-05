import streamlit as st
import requests
from dotenv import load_dotenv
import os
from helper.upload_response import upload_response
from helper.upload_File import uploadFile
from pymongo import MongoClient
import json
class Content_Process_and_Assets_Analyst:
    def __init__(self, model_url):
        self.uploaded_files = []
        self.file_dict = {}
        self.model_url = model_url
        self.run_all = (st.session_state.get('run_all', {}))
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
                with st.spinner('Content - Process and Assets Analyst...', show_time=True):
                        st.write('')
                        headers = {"Content-Type": "application/json", "x-api-key": f"{os.getenv('x_api_key')}"}         
                        try:
                                payload_txt = {"input_value": self.payload, "output_type": "text", "input_type": "chat"}
                                payload_txt_model = self.request_model(payload_txt, headers)
                                debug_info = {'data_field' : 'Content - Process and Assets Analyst', 'result': payload_txt_model}
                                upload_response(debug_info)

                                count = 0
                        except Exception as e:
                            pass
                        st.session_state['analyzing'] = False    
                      
    def row1(self):
            st.session_state['analyzing'] = False
            self.payload = ""  
            count = 0
            try:
                session_client_summary = st.session_state['client_summary']
                if session_client_summary == 'uploaded' or self.run_all == True:
                    count += 1
                    self.payload += self.fetch_data("Client Summary")
            except Exception as e:
                pass
            try:
                session_content_in_the_website = st.session_state['content_in_the_website']
                if session_content_in_the_website == 'uploaded' or self.run_all == True:
                    count += 1
                    self.payload += self.fetch_data("Content in the Website")
            except Exception as e:
                pass
            try:
                session_content_outside_the_website = st.session_state['content_outside_the_website']
                if session_content_outside_the_website == 'uploaded' or self.run_all == True:
                    count += 1
                    self.payload += self.fetch_data("Content outside the Website")
            except Exception as e:
                pass
            
            if count >= 3:
                self.process()
                                       

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
