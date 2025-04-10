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
                with st.spinner('Website and Tools...', show_time=True):
                        st.write('')
                        '''
                        # OUTPUT FOR WEBSITE RESPONSIVENESS
                        payload_txt_website_responsiveness = {"result": website_responsiveness}
                        result_website_responsiveness = self.request_model(payload_txt_website_responsiveness)

                        # OUTPUT FOR CONTENT MANAGEMENT SYSTEM
                        payload_txt_content_management_system = {"question": content_management_system}
                        #result_content_management_system = self.request_model(content_management_system)

                        # OUTPUT FOR SSL CERTIFICATE
                        payload_txt_SSL_certificate = {"question": SSL_certificate}
                        #result_SSL_certificate = self.request_model(SSL_certificate)

                        # OUTPUT FOR WEB ANALYTICS
                        payload_txt_web_analytics = {"question": web_analytics}
                        #result_web_analytics = self.request_model(web_analytics)

                        # OUTPUT FOR CLIENT RELATIONS MANAGEMENT SYSTEM
                        payload_txt_client_relations_management_system = {"question": client_relations_management_system}
                        #result_client_relations_management_system = self.request_model(client_relations_management_system)
                        
                        # OUTPUT FOR LEAD GENERATION MECHANISM
                        payload_txt_lead_generation_mechanism = {"question": lead_generation_mechanism}
                        #result_lead_generation_mechanism = self.request_model(lead_generation_mechanism)
                        '''
                        # OUTPUT FOR SEO ANALYST
                      
                        #print(x)
                        headers = {"Content-Type": "application/json", "x-api-key": f"{os.getenv('x-api-key')}"}
                        try:
                            payload = ""
                            session_website_responsiveness = st.session_state['website_responsiveness']
                            if session_website_responsiveness == 'uploaded':
                                payload += self.fetch_data("Website Responsiveness")
                        except Exception as e:
                             pass
                        try:
                            session_content_management_system = st.session_state['content_management_system']
                            if session_content_management_system == 'uploaded':
                                payload += self.fetch_data("Content Management System")
                        except Exception as e:
                             pass
                        try:
                            session_SSL_certificate = st.session_state['SSL_certificate']
                            if session_SSL_certificate == 'uploaded':
                                payload += self.fetch_data("SSL Certificate")
                                
                        except Exception as e:
                             pass
                        try:
                            session_mobile_responsiveness = st.session_state['mobile_responsiveness']
                            if session_mobile_responsiveness == 'uploaded':
                                payload += self.fetch_data("Mobile Responsiveness")
                        except Exception as e:
                             pass
                        try:
                            session_desktop_loading_speed = st.session_state['desktop_loading_speed']
                            if session_desktop_loading_speed == 'uploaded':
                                payload += self.fetch_data("Desktop Loading Speed")
                        except Exception as e:
                             pass
                        try:
                            session_mobile_loading_speed = st.session_state['mobile_loading_speed']
                            if session_mobile_loading_speed == 'uploaded':
                                payload += self.fetch_data("Mobile Loading Speed")
                        except Exception as e:
                             pass
                        try:
                            session_first_meaningful_paint = st.session_state['first_meaningful_paint']
                            if session_first_meaningful_paint == 'uploaded':
                                payload += self.fetch_data("First Meaningful Paint")
                        except Exception as e:
                             pass
                        try:
                            session_web_analytics = st.session_state['web_analytics']
                            if session_web_analytics == 'uploaded':
                                payload += self.fetch_data("Web Analytics")
                        except Exception as e:
                             pass
                        try:
                            session_client_relations_management_system = st.session_state['client_relations_management_system']
                            if session_client_relations_management_system == 'uploaded':
                                payload += self.fetch_data("Client Relations Management System")
                        except Exception as e:
                             pass
                        try:
                            session_lead_generation_mechanism = st.session_state['lead_generation_mechanism']
                            if session_lead_generation_mechanism == 'uploaded':
                                payload += self.fetch_data("Lead Generation Mechanism")
                        except Exception as e:
                             pass
                        
                        try:
                            session_website_responsiveness = st.session_state['website_responsiveness']
                            session_client_relations_management_system = st.session_state['client_relations_management_system']
                            session_lead_generation_mechanism = st.session_state['lead_generation_mechanism']
                            session_web_analytics = st.session_state['web_analytics']
                            session_mobile_responsiveness = st.session_state['mobile_responsiveness']
                            session_desktop_loading_speed = st.session_state['desktop_loading_speed']
                            session_mobile_loading_speed = st.session_state['mobile_loading_speed']
                            session_SSL_certificate = st.session_state['SSL_certificate']
                            session_content_management_system = st.session_state['content_management_system']

                            if session_website_responsiveness or session_client_relations_management_system or session_lead_generation_mechanism or session_web_analytics or session_mobile_responsiveness or session_desktop_loading_speed or session_mobile_loading_speed or session_content_management_system or session_SSL_certificate == 'uploaded':
                                payload_txt = {"input_value": payload, "output_type": "text", "input_type": "chat"}
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
                                st.session_state['lead_generation_mechanism'] = ''
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