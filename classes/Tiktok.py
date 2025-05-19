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

class Tiktok:
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
        '''
        # AGENT NAME
        st.header(self.analyst_name)

        # EVALUATION FORM LINK
        url = os.getenv('Link')
        st.write('Evaluation Form: [Link](%s)' % url)

        # RETURN BUTTON
        try:
            if st.button("Return", type='primary'):
                st.switch_page("./pages/home.py")
        except Exception:
            pass
        '''
        if 'tiktok_upload' not in st.session_state:
            st.session_state['tiktok_upload'] = ''

    def request_model(self, payload_txt):
        response = requests.post(self.model_url, json=payload_txt)
        response.raise_for_status()
        output = response.json()
        
        categories = []
        current_footprint = []
        number_of_backlinks = []

        for key, value in output.items():
            if key == 'json':
                for item in value:
                    categories.append(item.get('category', 'N/A').replace('_', ' ').title())
                    current_footprint.append(item.get('current_footprint', 'N/A'))
                    number_of_backlinks.append(item.get('best_of_breed_solution', 'N/A'))    

        output = ""
        for i in range(len(categories)):
            output += f"\n\n---\n **Category:** {categories[i]}"
            output += f"\n\n **Count:** {current_footprint[i]}\n\n"
            output += f"**Best of Breed Solution:** {number_of_backlinks[i]}"

        data = {
            "": [str(category) for category in categories],
            "Current Footprint": [str(footprint) for footprint in current_footprint],
            "Best of Breed Solution": [str(backlink) for backlink in number_of_backlinks]
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
      
    def detect_encoding(self, uploaded_file):
        result = chardet.detect(uploaded_file.read(100000))
        uploaded_file.seek(0)  # Reset file pointer to the beginning
        return result['encoding']

    def terminate_session(self, session):
        try:
            del st.session_state[session]
        except KeyError:
            pass

    def file_upload(self, file_name, file_desc, session):
        st.write("") # FOR THE HIDE BUTTON
        file_name = st.file_uploader(f"{file_desc}", type='csv')
        if file_name:
                try:
                    self.terminate_session(session)
                except UnboundLocalError:
                    pass
                try:
                    encoding = self.detect_encoding(file_name)
                    st.session_state[f'{session}'] = pd.read_csv(file_name, encoding=encoding, low_memory=False)
                except Exception:
                    pass
                return file_name
    
    def process(self):
        session = st.session_state.analyze
        if (self.tiktok_f or self.tiktok_er or self.tiktok_pf) and session == 'clicked':
                    try:
                        combined_text = ""
                        with st.spinner('Uploading Tiktok Files...', show_time=True):
                                st.write('')
                                # INITIALIZING SESSIONS
                                #combined_text += f"Client Summary: {st.session_state.nature}\n"
                                try:
                                    combined_text += f"\nTiktok Followers: {self.tiktok_f}"
                                    combined_text += f"\nTiktok Audience Engagement Rate: {self.tiktok_er}%"
                                    combined_text += f"\nTiktok Post Frequency: {self.tiktok_pf}"
                                except KeyError:
                                    pass
                
                                # OUTPUT FOR SEO ANALYST
                                payload_txt = {"question": combined_text}
                                #result = self.request_model(payload_txt)
                                
                                #end_time = time.time()
                                #time_lapsed = end_time - start_time

                                self.competitor_name = st.session_state.competitor_name
                                self.is_competitor = st.session_state.is_competitor
                                combined_text = self.competitor_name + combined_text if self.is_competitor == True else combined_text
                                
                                debug_info = {'data_field' : 'Tiktok', 'result': combined_text}
                                '''
                                debug_info = {
                                    #'analyst': self.analyst_name,
                                    'url_uuid': self.model_url.split("-")[-1],
                                    'time_lapsed': time_lapsed,
                                    'payload': payload_txt,
                                    'result': result,
                                }
                                '''
                                collect_telemetry(debug_info)
                                st.session_state['tiktok_upload'] = 'uploaded'
                                
                                #with st.expander("Debug information", icon="⚙"):
                                #    st.write(debug_info)

                                st.session_state['analyzing'] = False 
                    except AttributeError:
                        st.info("Please upload CSV or PDF files first.")
                        hide_button() 

    def row1(self):
            self.tiktok_f = st.text_input("Followers:", placeholder='Enter Tiktok Followers')
            self.tiktok_er = st.text_input("Audience Engagement Rate:", placeholder='Enter Tiktok Audience Engagement Rate')
            self.tiktok_pf = st.text_input("Post Frequency:", placeholder='Enter Tiktok Post Frequency')

            followers = {
                'Tiktok Followers': self.tiktok_f if self.tiktok_f else 'N/A'
            }
            #tiktok_post = self.file_upload("Tiktok", "Tiktok Content post", "Tiktok")
            
            #tiktok_post
           
            '''
            st.write("") # FOR THE HIDE BUTTON
            st.write("") # FOR THE HIDE BUTTON
            st.write("AI Analyst Output: ")
            st.session_state['analyzing'] = False
            st.write("") # FOR THE HIDE BUTTON'
            '''
            #analyze_button = st.button("Analyze", disabled=initialize_analyze_session())
            self.process()
            
if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
