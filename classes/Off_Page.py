from io import StringIO
from urllib.parse import urlparse
import streamlit as st
import requests
from dotenv import load_dotenv
import time
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button, unhide_button
from helper.initialize_analyze_session import initialize_analyze_session
import pandas as pd
import json

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
        if 'off_page_file_uploaded' not in st.session_state:
            st.session_state['off_page_file_uploaded'] = ''
        if 'website_audience' not in st.session_state:
            st.session_state['website_audience'] = ''
        if 'uploaded_files' not in st.session_state:
            st.session_state['uploaded_files'] = ''
    
    def request_model(self, payload_txt, headers):
        response = requests.post(self.model_url, json=payload_txt, headers=headers)
        response.raise_for_status()
        output = response.json()
        text = output["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
        text = json.loads(text)
        
        backlinks = text[0]
        referring_domains = text[1]

        return text
    
    def process(self):
         start_time = time.time()
         session = st.session_state['analyze']
         if self.uploaded_files and session == 'clicked':
                    combined_text = ""
                    website_audience = ""
                    with st.spinner('Uploading Off Page...', show_time=True):
                        st.write('')
                        try:
                            for file_info in st.session_state['uploaded_files'].values():
                                '''
                                if file_info['type'] == 'pdf':
                                    combined_text += file_info['content'] + "\n"
                                '''
                            try:
                                if file_info['type'] == 'csv':                                    
                                    # Load CSV
                                    df = pd.read_csv(StringIO(file_info['content'].to_csv(index=True)))
                                    
                                    # Count total rows
                                    num_rows = len(df)
                                    
                                    # Extract unique domains from 'Source url'
                                    df['Source Domain'] = df['Source url'].apply(lambda x: urlparse(x).netloc)
                                    unique_domains = df['Source Domain'].nunique()
                                        
                                    combined_text += f"Backlinks - SEMRush Report:\nTotal Backlinks Count: {num_rows}\n"
                                    combined_text += f"Referring Domain: {unique_domains}"
                                    #st.info("Backlinks - SEMRush Uploaded Successfuly", icon="ℹ️")
                            except KeyError:
                                st.info("Incorrect CSV format. Please upload a valid CSV file.")
                                pass
                            except UnboundLocalError:
                                 pass
                        except AttributeError:
                                 pass
                        except KeyError:
                             pass
                        '''
                        try:
                            # Check if upload_website_audience exists in session state and is a dictionary
                            if 'upload_website_audience' in st.session_state and isinstance(st.session_state['upload_website_audience'], dict):
                                for file_name, file_info in st.session_state['upload_website_audience'].items():
                                    try:
                                        if file_info['type'] == 'csv':
                                            # Since file_info['content'] is already a DataFrame (from your earlier code)
                                            # No need to convert back from string to DataFrame
                                            df = file_info['content']
                                            
                                            # Process your DataFrame here
                                            # Instead of reading from StringIO, just use the DataFrame directly
                                            website_audience += f"Website Audience Acquisition {df}\n"
                                            
                                            #st.info("Website Audience Acquisition Uploaded Successfully", icon="ℹ️")
                                    except KeyError:
                                        pass
                                        #st.info(f"Incorrect format for {file_name}. Please upload a valid CSV file.")
                        except Exception as e:
                            st.error(f"Error processing data: {str(e)}")
                        
                        '''
                        # OUTPUT FOR SEO ANALYST

                        #result = self.request_model(payload_txt, headers)
                        
                        #end_time = time.time()
                        #time_lapsed = end_time - start_time
                        
                        self.competitor_name = st.session_state.competitor_name
                        self.is_competitor = st.session_state.is_competitor

                        combined_text = self.competitor_name + combined_text if self.is_competitor == True else combined_text

                        if self.is_competitor:
                            debug_info = {'data_field' : 'Backlinks Competitor', 'result': combined_text}
                        else:
                            debug_info = {'data_field' : 'Backlinks', 'result': combined_text}
                        debug_info_website_audience = {'data_field' : 'Website Audience Acquisition', 'result': website_audience}
                        #debug_info = {'url_uuid': self.model_url.split("-")[-1],'time_lapsed' : time_lapsed, 'files': [*st.session_state['uploaded_files']],'payload': payload_txt, 'result': result}

                        if self.uploaded_files:
                            st.session_state['off_page_file_uploaded'] = 'uploaded'
                            collect_telemetry(debug_info)
                        #if self.website_audience:
                        #    st.session_state['website_audience'] = 'uploaded'
                        #    collect_telemetry(debug_info_website_audience)

                        
                        #with st.expander("Debug information", icon="⚙"):
                        #    st.write(debug_info)
                        st.session_state['analyzing'] = False
    
    def row1(self):
            #st.write(self.data_src)
            self.uploaded_files = st.file_uploader('Backlinks - SEMRush', type='csv', accept_multiple_files=True, key="seo_off")
            #self.website_audience = st.file_uploader('Website Audience Acquisition - GA4', type='csv', accept_multiple_files=True, key="website_audiences")
            #self.website_audience = st.text_input("Website Audience Acquisition:", placeholder='Enter Website Audience Acquisition')

            if self.uploaded_files:
                upload.multiple_upload_file(self.uploaded_files)
            #if self.website_audience:
            #     upload.upload_website_audience(self.website_audience)
                
            #st.write("") # FOR THE HIDE BUTTON
            #st.write("") # FOR THE HIDE BUTTON
           
            st.session_state['analyzing'] = False
            
            self.process()
                                       

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
