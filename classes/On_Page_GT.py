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

class SeoOnGT:
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
    
    def request_model(self, payload_txt):
        response = requests.post(self.model_url, json=payload_txt)
        response.raise_for_status()
        output = response.json()
        
        categories = []
        remarks = []

        for key, value in output.items():
            if key == 'json':
                for item in value:
                    categories.append(item.get('elements', 'N/A').replace('_', ' ').title())
                    remarks.append(item.get('remarks', 'N/A'))

        output = ""
        for i in range(len(categories)):
            output += f"\n\n---\n **Category:** {categories[i]}"
            output += f"\n\n **Remarks:** {remarks[i]}\n\n"
        
        data = {
            "Category": [str(category) for category in categories],
            "Remarks": [str(footprint) for footprint in remarks],
        }
        df_output = pd.DataFrame(data)
        '''
        with st.expander("AI Analysis", expanded=True, icon="🤖"):
            st.table(df_output.style.set_table_styles(
                [{'selector': 'th:first-child, td:first-child', 'props': [('width', '20px')]},
                {'selector': 'th, td', 'props': [('width', '150px'), ('text-align', 'center')]}]
            ).set_properties(**{'text-align': 'center'}))
        '''

        return output
    
    def process(self):
                session = st.session_state.analyze
                start_time = time.time()
                if (self.website_responsiveness or self.content_management_system or self.SSL_certificate or self.web_analytics or self.client_relations_management_system or self.lead_generation_mechanism or self.first_meaningful_paint or self.mobile_responsiveness or self.mobile_loading_speed or self.desktop_loading_speed) and session == 'clicked':
                    combined_text = ""
                    website_responsiveness = ""
                    content_management_system = ""
                    SSL_certificate = ""
                    mobile_responsiveness = ""
                    desktop_loading_speed = ""
                    mobile_loading_speed = ""
                    web_analytics = ""
                    client_relations_management_system = ""
                    mobile_loading_speed = ""
                    first_meaningful_paint = ""
                    lead_generation_mechanism = ""
                    with st.spinner('SEO On Page Analyst...', show_time=True):
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
                        '''
                        try: 
                            for f in st.session_state['uploaded_gt'].values():
                                if f['type'] == 'pdf':
                                    combined_text += "GTmetrix: {"+ f['content'] + "}\n"
                                elif f['type'] == 'csv':
                                    combined_text += f['content'].to_csv(index=True) + "\n"
                        except KeyError:
                            pass
                        try:
                            website_responsiveness += f"\nWebsite Responsiveness: {self.website_responsiveness}"
                            content_management_system += f"\nContent Management System: {self.content_management_system}%"
                            SSL_certificate += f"\nSSL Certificate: {self.SSL_certificate}"
                            mobile_responsiveness += f"\nMobile Responsiveness: {self.mobile_responsiveness}"
                            desktop_loading_speed += f"\nDesktop Loading Speed: {self.desktop_loading_speed}"
                            mobile_loading_speed += f"\nMobile Loading Speed: {self.mobile_loading_speed}"
                            first_meaningful_paint += f"\nFirst Meaningful Paint: {self.first_meaningful_paint}"
                            web_analytics += f"\nWeb Analytics: {self.web_analytics}"
                            client_relations_management_system += f"\nClient Relations Management System: {self.client_relations_management_system}"
                            lead_generation_mechanism += f"\nLead Generation Mechanism: {self.lead_generation_mechanism}"
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
                        payload_txt_lead_generation_mechanism = {"question": lead_generation_mechanism}
                        #result_lead_generation_mechanism = self.request_model(lead_generation_mechanism)

                        # OUTPUT FOR SEO ANALYST
                        payload_txt = {"question": combined_text}
                        #result = self.request_model(payload_txt)
                        #end_time = time.time()
                        #time_lapsed = end_time - start_time

                        debug_info = {'data_field' : 'GT Metrix', 'result': combined_text}
                        debug_info_website_responsiveness = {'data_field' : 'Website Responsiveness', 'result': website_responsiveness}
                        debug_info_content_management_system = {'data_field' : 'Content Management System', 'result': content_management_system}
                        debug_info_SSL_certificate = {'data_field' : 'SSL Certificate', 'result': SSL_certificate}
                        debug_info_mobile_responsiveness = {'data_field' : 'Mobile Responsiveness', 'result': mobile_responsiveness}
                        debug_info_desktop_loading_speed = {'data_field' : 'Desktop Loading Speed', 'result': desktop_loading_speed}
                        debug_info_mobile_loading_speed = {'data_field' : 'Mobile Loading Speed', 'result': mobile_loading_speed}
                        debug_info_first_meaningful_paint = {'data_field' : 'First Meaningful Paint', 'result': first_meaningful_paint}
                        debug_info_web_analytics = {'data_field' : 'Web Analytics', 'result': web_analytics}
                        debug_info_client_relations_management_system = {'data_field' : 'Client Relations Management System', 'result': client_relations_management_system}
                        debug_info_lead_generation_mechanism = {'data_field' : 'Lead Generation Mechanism', 'result': lead_generation_mechanism}
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
                            collect_telemetry(debug_info_website_responsiveness)
                        if self.content_management_system:
                            collect_telemetry(debug_info_content_management_system)
                        if self.SSL_certificate:
                            collect_telemetry(debug_info_SSL_certificate)
                        if self.mobile_responsiveness:
                            collect_telemetry(debug_info_mobile_responsiveness)
                        if self.desktop_loading_speed:
                            collect_telemetry(debug_info_desktop_loading_speed)
                        if self.mobile_loading_speed:
                            collect_telemetry(debug_info_mobile_loading_speed)
                        if self.first_meaningful_paint:
                            collect_telemetry(debug_info_first_meaningful_paint)
                        if self.web_analytics:
                            collect_telemetry(debug_info_web_analytics)
                        if self.client_relations_management_system:
                            collect_telemetry(debug_info_client_relations_management_system)
                        if self.lead_generation_mechanism:
                            collect_telemetry(debug_info_lead_generation_mechanism)
                            
                        #with st.expander("Debug information", icon="⚙"):
                        #    st.write(debug_info)


                        st.session_state['analyzing'] = False

                        for df_seo in st.session_state.keys():
                            del st.session_state[df_seo]
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
            self.web_analytics = st.text_input("Web Analytics - BuiltWith:", placeholder='Enter Web Analytics')
            self.client_relations_management_system = st.text_input("Client Relations Management System - BuiltWith:", placeholder='Enter Client Relations Management System')
            self.first_meaningful_paint = st.text_input("First Meaningful Paint - GTMetrix:", placeholder='Enter First Meaningful Paint')
            self.lead_generation_mechanism = st.text_input("Lead Generation Mechanism - Business Context (Lead Generation & Lead Nurturing):", placeholder='Enter Lead Generation Mechanism')

            #st.write("") # FOR THE HIDE BUTTON
            #st.write("") # FOR THE HIDE BUTTON
            #st.write("AI Analyst Output: ")
            st.session_state['analyzing'] = False
            #st.write("") # FOR THE HIDE BUTTON
            self.process()
            
            
      

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()