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

class SeoOn:
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
        if 'crawl_file' not in st.session_state:
            st.session_state['crawl_file'] = ''
        if 'first_meaningful_paint' not in st.session_state:
            st.session_state['first_meaningful_paint'] = ''

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
                if (self.first_meaningful_paint or self.uploaded_files) and session == 'clicked':
                    first_meaningful_paint = ""
                    crawl_file = ""
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
                            for file_info in st.session_state['uploaded_files'].values():
                                if file_info['type'] == 'pdf':
                                    crawl_file += file_info['content'] + "\n"
                                elif file_info['type'] == 'csv':
                                    try:
                                        crawl_file += "CrawlFile CSV: {"+ file_info['content'].to_csv(index=True) + "\n"
                                    except AttributeError:
                                        pass
                        except KeyError:
                            pass
                        try:
                            first_meaningful_paint += f"\nFirst Meaningful Paint: {self.first_meaningful_paint}"
                        except KeyError:
                            pass
                        
                        debug_info_first_meaningful_paint = {'data_field' : 'First Meaningful Paint', 'result': first_meaningful_paint}
                        debug_info_crawl_file = {'data_field' : 'Crawl File', 'result': crawl_file}

                        if self.first_meaningful_paint:
                            st.session_state['first_meaningful_paint'] = 'uploaded'
                            collect_telemetry(debug_info_first_meaningful_paint)
                        if self.uploaded_files:
                            st.session_state['crawl_file'] = 'uploaded'
                            collect_telemetry(debug_info_crawl_file)
                            
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
            self.uploaded_files = st.file_uploader("Crawl File - ScreamingFrog:", type=['pdf', 'csv'], accept_multiple_files=True)
            #self.gtmetrix = st.file_uploader("GTmetrix", type=['pdf', 'csv'], accept_multiple_files=True, key="seo_on_gt")
            if self.uploaded_files:
                upload.multiple_upload_file(self.uploaded_files)
                self.file_dict = upload.file_dict

            self.first_meaningful_paint = st.text_input("First Meaningful Paint - GTMetrix:", placeholder='Enter First Meaningful Paint')
           

            #st.write("") # FOR THE HIDE BUTTON
            #st.write("") # FOR THE HIDE BUTTON
            #st.write("AI Analyst Output: ")
            st.session_state['analyzing'] = False
            #st.write("") # FOR THE HIDE BUTTON
            self.process()
            
            
      

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()