import streamlit as st
import requests
from dotenv import load_dotenv
import os
from helper.upload_response import upload_response
from helper.upload_File import uploadFile
from pymongo import MongoClient
import json

class ConversionAnalyst:
    def __init__(self, model_url):
        self.uploaded_files = []
        self.file_dict = {}
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
    
    def request_model(self, payload_txt, headers):
        response = requests.post(self.model_url, json=payload_txt, headers=headers)
        response.raise_for_status()
        print(response)
        output = response.json()
        #st.write(output)
        text = output["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
        #text = json.loads(text)
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
                with st.spinner('Converison Analyst...', show_time=True):
                        st.write('')
                        headers = {"Content-Type": "application/json", "x-api-key": f"{os.getenv('x-api-key')}"}         
                        try:
                                payload_txt = {"input_value": self.payload, "output_type": "text", "input_type": "chat"}
                                payload_txt_model = self.request_model(payload_txt, headers)
                                debug_info = {'data_field' : 'Converison Analyst', 'result': payload_txt_model}
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
                session_lead_generation_mechanism = st.session_state['lead_generation_mechanism']
                if session_lead_generation_mechanism == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Lead Generation Mechanism")
            except Exception as e:
                pass
            try:
                session_client_relations_management_system = st.session_state['client_relations_management_system']
                if session_client_relations_management_system == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Client Relations Management System")
            except Exception as e:
                pass
            try:
                session_pull_through_offers = st.session_state['pull_through_offers']
                if session_pull_through_offers == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Pull through offers")
            except Exception as e:
                pass
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
                name = self.fetch_data("Client Name")
                website = self.fetch_data("Client Website")
                self.payload = name + website + self.payload
                self.process()
                                       

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
