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
        if 'website_responsiveness' not in st.session_state:
            st.session_state['website_responsiveness'] = ''
        if 'content_management_system' not in st.session_state:
            st.session_state['content_management_system'] = ''
        if 'SSL_certificate' not in st.session_state:
            st.session_state['SSL_certificate'] = ''
        if 'mobile_responsiveness' not in st.session_state:
            st.session_state['mobile_responsiveness'] = ''
        if 'desktop_loading_speed' not in st.session_state:
            st.session_state['desktop_loading_speed'] = ''
        if 'mobile_loading_speed' not in st.session_state:
            st.session_state['mobile_loading_speed'] = ''
        if 'web_analytics' not in st.session_state:
            st.session_state['web_analytics'] = ''
        if 'client_relations_management_system' not in st.session_state:
            st.session_state['client_relations_management_system'] = ''
    
    def process(self):
                session = st.session_state.analyze
                start_time = time.time()
                if (self.website_responsiveness or self.content_management_system or self.SSL_certificate or self.web_analytics or self.client_relations_management_system or self.mobile_responsiveness or self.mobile_loading_speed or self.desktop_loading_speed) and session == 'clicked':
                    website_responsiveness = ""
                    content_management_system = ""
                    SSL_certificate = ""
                    mobile_responsiveness = ""
                    desktop_loading_speed = ""
                    mobile_loading_speed = ""
                    web_analytics = ""
                    client_relations_management_system = ""
                    mobile_loading_speed = ""
        
                    with st.spinner('Uploading Website and Tools...', show_time=True):
                        st.write('')
                        '''
                        try:
                            for file_info in st.session_state['uploaded_files'].values():
                                if file_info['type'] == 'pdf':
                                    combined_text += file_info['content'] + "\n"
                                elif file_info['type'] == 'csv':
                                    try:
                                        combined_text += "CrawlFile CSV: {"+ file_info['content'].to_csv(index=True) + "\n"
                                    except AttributeError:
                                        pass
                        except KeyError:
                            pass
                            
                        try: 
                            for f in st.session_state['uploaded_gt'].values():
                                if f['type'] == 'pdf':
                                    crawl_file += "GTmetrix: {"+ f['content'] + "}\n"
                                elif f['type'] == 'csv':
                                    crawl_file += f['content'].to_csv(index=True) + "\n"
                        except KeyError:
                            pass
                        '''
                        try:
                            website_responsiveness += f"\nGTMetrix Report:\nWebsite Responsiveness: {self.website_responsiveness}"
                        except KeyError:
                            pass
                        try:
                            content_management_system += f"\nBuiltWith Report:\nContent Management System: {self.content_management_system}"
                        except KeyError:
                            pass
                        try:
                            SSL_certificate += f"\nBuiltWith Report:\nSSL Certificate: {self.SSL_certificate}"
                        except KeyError:
                            pass
                        try:
                            mobile_responsiveness += f"\nGTMetrix Report:\nMobile Responsiveness: {self.mobile_responsiveness}"
                        except KeyError:
                            pass
                        try:
                            desktop_loading_speed += f"\nGTMetrix Report:\nDesktop Loading Speed: {self.desktop_loading_speed}"
                        except KeyError:
                            pass
                        try:
                            mobile_loading_speed += f"\nGTMetrix Report:\nMobile Loading Speed: {self.mobile_loading_speed}"
                        except KeyError:
                            pass
                        try:
                            web_analytics += f"\nBuiltWith (GA4) Report:\nWeb Analytics: {self.web_analytics}"

                        except KeyError:
                            pass
                        try:
                            client_relations_management_system += f"\nBuiltWith Report:\nClient Relations Management System: {self.client_relations_management_system}"
                        except KeyError:
                            pass
                        
                        # OUTPUT FOR WEBSITE RESPONSIVENESS
                        payload_txt_website_responsiveness = {"question": website_responsiveness}
                        #result_website_responsiveness = self.request_model(website_responsiveness)

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

                        # OUTPUT FOR SEO ANALYST
                        #payload_txt = {"question": combined_text}
                        #result = self.request_model(payload_txt)
                        #end_time = time.time()
                        #time_lapsed = end_time - start_time
                        
                        self.competitor_name = st.session_state.competitor_name
                        self.is_competitor = st.session_state.is_competitor

                        website_responsiveness = self.competitor_name + website_responsiveness if self.is_competitor == True else website_responsiveness
                        content_management_system = self.competitor_name + content_management_system if self.is_competitor == True else content_management_system
                        SSL_certificate = self.competitor_name + SSL_certificate if self.is_competitor == True else SSL_certificate
                        mobile_responsiveness = self.competitor_name + mobile_responsiveness if self.is_competitor == True else mobile_responsiveness
                        desktop_loading_speed = self.competitor_name + desktop_loading_speed if self.is_competitor == True else desktop_loading_speed
                        mobile_loading_speed = self.competitor_name + mobile_loading_speed if self.is_competitor == True else mobile_loading_speed
                        web_analytics = self.competitor_name + web_analytics if self.is_competitor == True else web_analytics
                        client_relations_management_system = self.competitor_name + client_relations_management_system if self.is_competitor == True else client_relations_management_system
                        
                        if self.is_competitor:
                            debug_info_website_responsiveness = {'data_field' : 'Website Responsiveness Competitor', 'result': website_responsiveness}
                            debug_info_content_management_system = {'data_field' : 'Content Management System Competitor', 'result': content_management_system}
                            debug_info_SSL_certificate = {'data_field' : 'SSL Certificate Competitor', 'result': SSL_certificate}
                            debug_info_mobile_responsiveness = {'data_field' : 'Mobile Responsiveness Competitor', 'result': mobile_responsiveness}
                            debug_info_desktop_loading_speed = {'data_field' : 'Desktop Loading Speed Competitor', 'result': desktop_loading_speed}
                            debug_info_mobile_loading_speed = {'data_field' : 'Mobile Loading Speed Competitor', 'result': mobile_loading_speed}
                            debug_info_web_analytics = {'data_field' : 'Web Analytics Competitor', 'result': web_analytics}
                            debug_info_client_relations_management_system = {'data_field' : 'Client Relations Management System Competitor', 'result': client_relations_management_system}
                        else:
                            debug_info_website_responsiveness = {'data_field' : 'Website Responsiveness', 'result': website_responsiveness}
                            debug_info_content_management_system = {'data_field' : 'Content Management System', 'result': content_management_system}
                            debug_info_SSL_certificate = {'data_field' : 'SSL Certificate', 'result': SSL_certificate}
                            debug_info_mobile_responsiveness = {'data_field' : 'Mobile Responsiveness', 'result': mobile_responsiveness}
                            debug_info_desktop_loading_speed = {'data_field' : 'Desktop Loading Speed', 'result': desktop_loading_speed}
                            debug_info_mobile_loading_speed = {'data_field' : 'Mobile Loading Speed', 'result': mobile_loading_speed}
                            debug_info_web_analytics = {'data_field' : 'Web Analytics', 'result': web_analytics}
                            debug_info_client_relations_management_system = {'data_field' : 'Client Relations Management System', 'result': client_relations_management_system}

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
                        if self.website_responsiveness:
                            st.session_state['website_responsiveness'] = 'uploaded'
                            collect_telemetry(debug_info_website_responsiveness)
                        if self.content_management_system:
                            st.session_state['content_management_system'] = 'uploaded'
                            collect_telemetry(debug_info_content_management_system)
                        if self.SSL_certificate:
                            st.session_state['SSL_certificate'] = 'uploaded'
                            collect_telemetry(debug_info_SSL_certificate)
                        if self.mobile_responsiveness:
                            st.session_state['mobile_responsiveness'] = 'uploaded'
                            collect_telemetry(debug_info_mobile_responsiveness)
                        if self.desktop_loading_speed:
                            st.session_state['desktop_loading_speed'] = 'uploaded'
                            collect_telemetry(debug_info_desktop_loading_speed)
                        if self.mobile_loading_speed:
                            st.session_state['mobile_loading_speed'] = 'uploaded'
                            collect_telemetry(debug_info_mobile_loading_speed)
                        if self.web_analytics:
                            st.session_state['web_analytics'] = 'uploaded'
                            collect_telemetry(debug_info_web_analytics)
                        if self.client_relations_management_system:
                            st.session_state['client_relations_management_system'] = 'uploaded'
                            collect_telemetry(debug_info_client_relations_management_system)

                            
                        #with st.expander("Debug information", icon="⚙"):
                        #    st.write(debug_info)


                        st.session_state['analyzing'] = False
                        try:
                            self.file_dict.popitem()
                        except KeyError:
                            pass
                        
    def row1(self):
            #st.write(self.data_src)
            #self.uploaded_files = st.file_uploader("Upload Backlink List (PDF)", type=['pdf', 'csv'], accept_multiple_files=True, key="seo_on")
            #self.gtmetrix = st.file_uploader("GTmetrix:", type=['pdf', 'csv'], accept_multiple_files=True, key="seo_on_gt")
            '''
            if self.uploaded_files:
                upload.multiple_upload_file(self.uploaded_files)
                self.file_dict = upload.file_dict
            
            if self.gtmetrix:
                upload.upload_gt(self.gtmetrix)
            '''
            self.website_responsiveness = st.text_input("Website Overall Health Scores - GTMetrix:", placeholder='Enter Website Overall Health Scores')
            self.content_management_system = st.text_input("Content Management System - BuiltWith:", placeholder='Enter Content Management System')
            self.SSL_certificate = st.text_input("SSL Certificate - BuiltWith:", placeholder='Enter SSL Certificate')
            self.mobile_responsiveness = st.text_input("Mobile Responsiveness - GTMetrix:", placeholder='Enter Mobile Responsiveness')
            self.desktop_loading_speed = st.text_input("Desktop Loading Speed - GTMetrix:", placeholder='Enter Desktop Loading Speed')
            self.mobile_loading_speed = st.text_input("Mobile Loading Speed - GTMetrix:", placeholder='Enter Mobile Loading Speed')
            self.web_analytics = st.text_input("Web Analytics - BuiltWith (GA4):", placeholder='Enter Web Analytics')
            self.client_relations_management_system = st.text_input("Client Relations Management System - BuiltWith:", placeholder='Enter Client Relations Management System')
            
            #st.write("") # FOR THE HIDE BUTTON
            #st.write("") # FOR THE HIDE BUTTON
            #st.write("AI Analyst Output: ")
            st.session_state['analyzing'] = False
            #st.write("") # FOR THE HIDE BUTTON
            self.process()

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()