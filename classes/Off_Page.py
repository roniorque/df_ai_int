from io import StringIO
from urllib.parse import urlparse
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
import asyncio

class SeoOffPageAnalyst:
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
    
    def request_model(self, payload_txt):
        response = requests.post(self.model_url, json=payload_txt)
        response.raise_for_status()
        output = response.json()
        
        categories = []
        remarks = []
        count = []

        for key, value in output.items():
            if key == 'json':
                for item in value:
                    categories.append(item.get('elements', 'N/A').replace('_', ' ').title())
                    remarks.append(item.get('remarks', 'N/A'))
                    count.append(item.get('count', 'N/A'))

        output = ""
        for i in range(len(categories)):
            output += f"\n\n---\n **Category:** {categories[i]}"
            output += f"\n\n **Remarks:** {remarks[i]}\n\n"
            output += f"**Count:** {count[i]}"
        
        data = {
            "": [str(category) for category in categories],
            "Count": [str(count) for count in count],
            "Remarks": [str(remark) for remark in remarks]
            
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
         print("init off page")
         start_time = time.time()
         session = st.session_state['analyze']
         if self.uploaded_files and session == 'clicked':
                    combined_text = ""
                    with st.spinner('SEO Off Page Analyst...', show_time=True):
                        st.write('')
                        for file_info in st.session_state['uploaded_files'].values():
                            '''
                            if file_info['type'] == 'pdf':
                                combined_text += file_info['content'] + "\n"
                            '''
                            if file_info['type'] == 'csv':                                    
                                # Load CSV
                                df = pd.read_csv(StringIO(file_info['content'].to_csv(index=True)))
                                
                                # Count total rows
                                num_rows = len(df)
                                
                                # Extract unique domains from 'Source url'
                                df['Source Domain'] = df['Source url'].apply(lambda x: urlparse(x).netloc)
                                unique_domains = df['Source Domain'].nunique()
                                    
                                combined_text += f"Total Backlinks Count: {num_rows}\n"
                                combined_text += f"Referring Domain: {unique_domains}"
                        
                        # OUTPUT FOR SEO ANALYST
                        payload_txt = {"question": combined_text}
                        #result = self.request_model(payload_txt)
                        
                        #end_time = time.time()
                        #time_lapsed = end_time - start_time
                        
                        debug_info = {'data_field' : 'Backlinks', 'result': combined_text}
                        #debug_info = {'url_uuid': self.model_url.split("-")[-1],'time_lapsed' : time_lapsed, 'files': [*st.session_state['uploaded_files']],'payload': payload_txt, 'result': result}
                        collect_telemetry(debug_info)
                        
                        #with st.expander("Debug information", icon="⚙"):
                        #    st.write(debug_info)
                        print("done2")
                        st.session_state['analyzing'] = False
                      
    def row1(self):
            #st.write(self.data_src)
            self.uploaded_files = st.file_uploader('Backlinks - SEMRush', type='csv', accept_multiple_files=True, key="seo_off")
            if self.uploaded_files:
                upload.multiple_upload_file(self.uploaded_files)
                
            #st.write("") # FOR THE HIDE BUTTON
            #st.write("") # FOR THE HIDE BUTTON
           
            st.session_state['analyzing'] = False
            
            self.process()
                                       

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
