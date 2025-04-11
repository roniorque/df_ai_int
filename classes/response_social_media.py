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
        
        x = x["result"]
        return x
    
    def process(self):  
        with st.spinner('Social Media Analyst...', show_time=True):
                    st.write('')
                    headers = {"Content-Type": "application/json", "x-api-key": f"{os.getenv('x-api-key')}"}              
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
            count = 0                           
            try:
                session_fb = st.session_state['fb_upload']
                if session_fb == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Facebook")        
            except Exception as e:
                pass
            try:
                session_ig = st.session_state['ig_upload']
                if session_ig == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Instagram")
            except Exception as e:
                pass
            try:
                session_twitter = st.session_state['twitter_upload']
                if session_twitter == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Twitter")
            except Exception as e:
                pass
            try:
                session_yt = st.session_state['youtube_upload']
                if session_yt == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("YouTube")
            except Exception as e:
                pass
            try:
                session_linkedin = st.session_state['linkedin_upload']
                if session_linkedin == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Linkedin")           
            except Exception as e:
                pass
            try:
                session_tiktok = st.session_state['tiktok_upload']
                if session_tiktok == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Tiktok")
            except Exception as e:
                pass
            if count >= 1:
                self.process()
            

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
