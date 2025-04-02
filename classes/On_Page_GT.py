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
        with st.expander("AI Analysis", expanded=True, icon="🤖"):
            st.table(df_output.style.set_table_styles(
                [{'selector': 'th:first-child, td:first-child', 'props': [('width', '20px')]},
                {'selector': 'th, td', 'props': [('width', '150px'), ('text-align', 'center')]}]
            ).set_properties(**{'text-align': 'center'}))


        return output
    
    def row1(self):
            #st.write(self.data_src)
            #self.uploaded_files = st.file_uploader("Upload Backlink List (PDF)", type=['pdf', 'csv'], accept_multiple_files=True, key="seo_on")
            self.gtmetrix = st.file_uploader("GTmetrix:", type=['pdf', 'csv'], accept_multiple_files=True, key="seo_on_gt")
            '''
            if self.uploaded_files:
                upload.multiple_upload_file(self.uploaded_files)
                self.file_dict = upload.file_dict
            '''
            if self.gtmetrix:
                upload.upload_gt(self.gtmetrix)

            self.website_responsiveness = st.text_input("Website Responsiveness - Google PageSpeed Insight:", placeholder='Enter Website Responsiveness')
            self.content_management_system = st.text_input("Content Management System - BuiltWith:", placeholder='Enter Content Management System')
            self.SSL_certificate = st.text_input("SSL Certificate - BuiltWith:", placeholder='Enter SSL Certificate')
            self.web_analytics = st.text_input("Web Analytics - BuiltWith:", placeholder='Enter Web Analytics')
            self.client_relations_management_system = st.text_input("Client Relations Management System - BuiltWith:", placeholder='Enter Client Relations Management System')
            self.lead_generation_mechanism = st.text_input("Lead Generation Mechanism - Business Context (Lead Generation & Lead Nurturing):", placeholder='Enter Lead Generation Mechanism')

            #st.write("") # FOR THE HIDE BUTTON
            #st.write("") # FOR THE HIDE BUTTON
            #st.write("AI Analyst Output: ")
            st.session_state['analyzing'] = False
            #st.write("") # FOR THE HIDE BUTTON
            
            if st.session_state['analyze'] == 'clicked':
                start_time = time.time()
                if self.gtmetrix:
                    combined_text = ""
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
                            combined_text += f"\nWebsite Responsiveness: {self.website_responsiveness}"
                            combined_text += f"\nContent Management System: {self.content_management_system}%"
                            combined_text += f"\nSSL Certificate: {self.SSL_certificate}"
                            combined_text += f"\nWeb Analytics: {self.web_analytics}"
                            combined_text += f"\nClient Relations Management System: {self.client_relations_management_system}"
                            combined_text += f"\nLead Generation Mechanism: {self.lead_generation_mechanism}"
                        except KeyError:
                            pass
                        # OUTPUT FOR SEO ANALYST
                        payload_txt = {"question": combined_text}
                        result = self.request_model(payload_txt)
                        end_time = time.time()
                        time_lapsed = end_time - start_time
                        debug_info = {#'analyst': self.analyst_name,
                                      'url_uuid': self.model_url.split("-")[-1],
                                      'time_lapsed' : time_lapsed, 
                                    'crawl_file': [file.name for file in self.uploaded_files] if self.uploaded_files else ['Not available'],
                                      'gt_metrix': [file.name for file in self.gtmetrix] if self.gtmetrix else ['Not available'],
                                      'payload': payload_txt, 
                                      'result': result}
                        
                        collect_telemetry(debug_info)
                        
                            
                        with st.expander("Debug information", icon="⚙"):
                            st.write(debug_info)


                        st.session_state['analyzing'] = False

                        for df_seo in st.session_state.keys():
                            del st.session_state[df_seo]
                        try:
                            self.file_dict.popitem()
                        except KeyError:
                            pass
                        if 'analyze' not in st.session_state:
                            st.session_state['analyze'] = ''
                        st.session_state['analyze'] == ''
      

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()