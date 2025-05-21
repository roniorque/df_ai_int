import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import time
import chardet
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button
from helper.initialize_analyze_session import initialize_analyze_session
from pymongo import MongoClient
import json
from helper.data_field import data_field
from helper.upload_response import upload_response

class SocialMedia:
    def __init__(self, model_url):
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

        # EVALUATION FORM LINK
        '''
        url = os.getenv('Link')
        st.write('Evaluation Form: [Link](%s)' % url)

        # RETURN BUTTON
        try:
            if st.button("Return", type='primary'):
                st.switch_page("./pages/home.py")
        except Exception:
            pass
        '''
        if 'fb_upload' not in st.session_state:
            st.session_state['fb_upload'] = ''
    
    def request_model(self, payload_txt, headers):
        response = requests.post(self.model_url, json=payload_txt, headers=headers)
        response.raise_for_status()
        output = response.json()
        #st.write(output)
        text = output["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
        text = json.loads(text)
        #st.write(text)
        return text
    
    def terminate_session(self, session):
        try:
            del st.session_state[session]
        except KeyError:
            pass

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
        with st.spinner('Social Media Analyst...', show_time=True):
                    st.write('')
                    headers = {"Content-Type": "application/json", "x-api-key": f"{os.getenv('x_api_key')}"}              
                    try:
                        payload_txt = {"input_value": self.payload, "output_type": "text", "input_type": "chat"}
                        payload_txt_model = self.request_model(payload_txt, headers)
                        debug_info = {'data_field' : 'Social Media Analyst', 'result': payload_txt_model}
                        upload_response(debug_info)

                        st.session_state['fb_upload'] = ''
                        st.session_state['ig_upload'] = ''
                        st.session_state['twitter_upload'] = ''
                        st.session_state['youtube_upload'] = ''
                        st.session_state['linkedin_upload'] = ''
                        st.session_state['tiktok_upload'] = ''
                        count = 0
                                                
                    except Exception as e:
                        pass
                    st.session_state['analyzing'] = False

    def row1(self):
            st.session_state['analyzing'] = False
            self.payload = ""                   
            
            self.payload += self.fetch_data("Facebook") + "\n" 
            self.payload += self.fetch_data("Instagram") + "\n"
            self.payload += self.fetch_data("Twitter") + "\n"
            self.payload += self.fetch_data("YouTube") + "\n"
            self.payload += self.fetch_data("Linkedin") + "\n"     
            self.payload += self.fetch_data("Tiktok") + "\n"
            summary = self.fetch_data("Client Summary") + "\n"
            
            self.payload = summary + self.payload

            self.competitor = ""
            self.competitor += self.fetch_competitor_data("Facebook Competitor") + "\n"
            self.competitor += self.fetch_competitor_data("Instagram Competitor") + "\n"
            self.competitor += self.fetch_competitor_data("Twitter Competitor") + "\n"
            self.competitor += self.fetch_competitor_data("YouTube Competitor") + "\n"           
            self.competitor += self.fetch_competitor_data("Linkedin Competitor") + "\n"    
            self.competitor += self.fetch_competitor_data("Tiktok Competitor") + "\n"   
            competitor_summary = self.fetch_competitor_data("Competitor Summary") + "\n"

            self.payload = "\n=== CLIENT DATA ===\n\n" + self.payload
            self.competitor = "\n\n=== COMPETITOR DATA ===\n\n" + competitor_summary + self.competitor
            self.payload = self.payload + "\n" + "=" * 50 + "\n" + self.competitor

            self.process()
            

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
