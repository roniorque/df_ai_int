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

class WebsiteAndTools:
    def __init__(self, model_url,):
        self.uploaded_files = []
        self.file_dict = {}
        self.file_gt = {}
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

       
    def request_model(self, payload_txt, headers):
        response = requests.post(self.model_url, json=payload_txt, headers=headers)
        response.raise_for_status()
        
        output = response.json()
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

    def fetch_competitor_data(self, data_field):
        mongodb_uri = os.getenv("MONGODB_URI")
        myclient = MongoClient(mongodb_uri)
        mydb = myclient.get_database()
        mycol = mydb["df_data"]
        
        # Get all documents matching the data_field
        results = mycol.find(
            {"data_field": data_field},
            sort=[("timestamp", -1)]  # Still sorting by timestamp in descending order
        )
        
        try:
            # Convert cursor to list
            results_list = list(results)
            if not results_list:
                st.session_state[data_field] = ''
                return ''
            
            # Extract "result" field from each document into a list
            data = [doc["result"] for doc in results_list]
            
            # Join the list into a single string with newlines between items
            return "\n".join(str(item) for item in data)
        except Exception as e:
            st.session_state[data_field] = ''
            return ''
        
    def process(self):
                with st.spinner('Website and Tools...', show_time=True):
                        st.write('')       
                        headers = {"Content-Type": "application/json", "x-api-key": f"{os.getenv('x_api_key')}"}                                     
                        try:
                                payload_txt = {"input_value": self.payload, "output_type": "text", "input_type": "chat"}
                                payload_txt_model = self.request_model(payload_txt, headers)
                                debug_info = {'data_field' : 'Website and Tools Analyst', 'result': payload_txt_model}
                                upload_response(debug_info)
                                st.session_state['website_responsiveness'] = ''
                                st.session_state['content_management_system'] = ''
                                st.session_state['SSL_certificate'] = ''
                                st.session_state['mobile_responsiveness'] = ''
                                st.session_state['desktop_loading_speed'] = ''
                                st.session_state['mobile_loading_speed'] = ''
                                st.session_state['first_meaningful_paint'] = ''
                                st.session_state['web_analytics'] = ''
                                st.session_state['client_relations_management_system'] = ''
                                #st.session_state['lead_generation_mechanism'] = ''
                                count = 0
                        except Exception as e:
                             pass


                      
                        st.session_state['analyzing'] = False
                        try:
                            self.file_dict.popitem()
                        except KeyError:
                            pass
                        
    def row1(self):
            st.session_state['analyzing'] = False
            self.payload = ""
            self.competitor = ""
            count = 0
            try:
                session_website_responsiveness = st.session_state['website_responsiveness']
                if session_website_responsiveness == 'uploaded'  or self.run_all == True:
                    count += 1
                    self.payload += self.fetch_data("Website Responsiveness") + "\n"
                    self.competitor += self.fetch_competitor_data("Website Responsiveness Competitor") + "\n"
            except Exception as e:
                pass
            try:
                session_content_management_system = st.session_state['content_management_system']
                if session_content_management_system == 'uploaded'  or self.run_all == True:
                    count += 1
                    self.payload += self.fetch_data("Content Management System") + "\n"
                    self.competitor += self.fetch_competitor_data("Content Management System Competitor") + "\n"
            except Exception as e:
                pass
            try:
                session_SSL_certificate = st.session_state['SSL_certificate']
                if session_SSL_certificate == 'uploaded'  or self.run_all == True:
                    count += 1
                    self.payload += self.fetch_data("SSL Certificate") + "\n"
                    self.competitor += self.fetch_competitor_data("SSL Certificate Competitor") + "\n"
            except Exception as e:
                pass
            try:
                session_mobile_responsiveness = st.session_state['mobile_responsiveness']
                if session_mobile_responsiveness == 'uploaded'  or self.run_all == True:
                    count += 1
                    self.payload += self.fetch_data("Mobile Responsiveness") + "\n"
                    self.competitor += self.fetch_competitor_data("Mobile Responsiveness Competitor") + "\n"
            except Exception as e:
                pass
            try:
                session_desktop_loading_speed = st.session_state['desktop_loading_speed']
                if session_desktop_loading_speed == 'uploaded'  or self.run_all == True:
                    count += 1
                    self.payload += self.fetch_data("Desktop Loading Speed") + "\n"
                    self.competitor += self.fetch_competitor_data("Desktop Loading Speed Competitor") + "\n"
            except Exception as e:
                pass
            try:
                session_mobile_loading_speed = st.session_state['mobile_loading_speed']
                if session_mobile_loading_speed == 'uploaded'  or self.run_all == True:
                    count += 1
                    self.payload += self.fetch_data("Mobile Loading Speed") + "\n"
                    self.competitor += self.fetch_competitor_data("Mobile Loading Speed Competitor") + "\n"
            except Exception as e:
                pass
            try:
                session_first_meaningful_paint = st.session_state['first_meaningful_paint']
                if session_first_meaningful_paint == 'uploaded'  or self.run_all == True:
                    count += 1
                    self.payload += self.fetch_data("First Meaningful Paint") + "\n"
                    self.competitor += self.fetch_competitor_data("First Meaningful Paint Competitor") + "\n"
            except Exception as e:
                pass
            try:
                session_web_analytics = st.session_state['web_analytics']
                if session_web_analytics == 'uploaded'  or self.run_all == True:
                    count += 1
                    self.payload += self.fetch_data("Web Analytics") + "\n"
                    self.competitor += self.fetch_competitor_data("Web Analytics Competitor") + "\n"
            except Exception as e:
                pass
            try:
                session_client_relations_management_system = st.session_state['client_relations_management_system']
                if session_client_relations_management_system == 'uploaded'  or self.run_all == True:
                    count += 1
                    self.payload += self.fetch_data("Client Relations Management System") + "\n"
                    self.competitor += self.fetch_competitor_data("Client Relations Management System Competitor") + "\n"
            except Exception as e:
                pass
            
            
            if count >= 1:
                client_summary = self.fetch_data("Client Summary")
                competitor_summary = self.fetch_competitor_data("Competitor Summary") + "\n"
                
                self.payload = "\n=== CLIENT DATA ===\n\n" + client_summary + self.payload
                self.competitor = "\n\n=== COMPETITOR DATA ===\n\n" + competitor_summary + self.competitor
                self.payload = self.payload + "\n" + "=" * 50 + "\n" + self.competitor

                self.process()
                 
if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()