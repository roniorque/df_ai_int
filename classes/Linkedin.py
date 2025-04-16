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

class Linkedin:
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
        if 'linkedin_upload' not in st.session_state:
            st.session_state['linkedin_upload'] = ''

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

    def linkedin_content_metrics(self, linkedin_content_metrics):
        # Avg. engagement rate
        try:
            linkedin_engagement_rate = linkedin_content_metrics['Engagement rate (organic)'].mean().round(2)
        except Exception:
            new_header = linkedin_content_metrics.iloc[0] #grab the first row for the header
            linkedin_content_metrics = linkedin_content_metrics[1:] #take the data less the header row
            linkedin_content_metrics.columns = new_header #set the header row as the df header
            linkedin_content_metrics['Engagement rate (organic)'] = pd.to_numeric(linkedin_content_metrics['Engagement rate (organic)'], errors='coerce')
            linkedin_engagement_rate = linkedin_content_metrics['Engagement rate (organic)'].mean().round(2)
        # Post Frequency
        
        st.session_state['linkedin_engagement_rate'] = linkedin_engagement_rate
        
        return linkedin_engagement_rate
    
    def linkedin_content_post(self, linkedin_content_post):
        try:
            linkedin_post_frequency = linkedin_content_post[~linkedin_content_post['Post title'].isna()].shape[0]
        except Exception:
            new_header = linkedin_content_post.iloc[0]
            linkedin_content_post = linkedin_content_post[1:]
            linkedin_content_post.columns = new_header
            linkedin_post_frequency = linkedin_content_post[~linkedin_content_post['Post title'].isna()].shape[0]
            st.write(linkedin_content_post)
            
        st.session_state['linkedin_post_frequency'] = linkedin_post_frequency
        return linkedin_post_frequency

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
        if  (self.linkedin_f or (self.linkedin_metrics and self.linkedin_metrics.name) or (self.linkedin_post and self.linkedin_post.name)) and session == "clicked":
                try:
                        combined_text = ""
                        with st.spinner('Uploading Linkedin Files...', show_time=True):
                            st.write('')
                            # INITIALIZING SESSIONS
                            #combined_text += f"Client Summary: {st.session_state.nature}\n"

                            try: # LINKEDIN
                                try: # LINKEDIN CONTENT POST
                                    combined_text += f"\nLinkedin Followers: {self.linkedin_f}"
                                    linkedin_content_post = st.session_state['linkedin_content_post'] 
                                    self.linkedin_content_post(linkedin_content_post)
                                    linkedin_post_frequency = st.session_state['linkedin_post_frequency']
                                    combined_text += f"\nLinkedin Post Frequency: {linkedin_post_frequency}"
                                except KeyError:
                                    pass
                                try: # LINKEDIN CONTENT METRICS
                                    linkedin_content_metrics = st.session_state['linkedin_content_metrics']  
                                    self.linkedin_content_metrics(linkedin_content_metrics)
                                    linkedin_engagement_rate = st.session_state['linkedin_engagement_rate'] 
                                    combined_text += f"\nLinkedin Engagement Rate: {linkedin_engagement_rate}%"
                                except KeyError:
                                    pass
                                try: # LINKEDIN CONTENT METRICS CSV
                                    combined_text += f"\nLinkedin Content Metrics: {linkedin_content_metrics.to_csv(index=True)}"
                                except UnboundLocalError:
                                    pass
                                try: # LINKEDIN CONTENT POST CSV
                                    combined_text += f"\nLinkedin Content Post: {linkedin_content_post.to_csv(index=True)}"
                                except UnboundLocalError:
                                    pass
                            except KeyError:
                                pass
            
                            # OUTPUT FOR SEO ANALYST
                            payload_txt = {"question": combined_text}
                            #result = self.request_model(payload_txt)
                            
                            #end_time = time.time()
                            #time_lapsed = end_time - start_time
                            debug_info = {'data_field' : 'Linkedin', 'result': combined_text}
                            '''
                            debug_info = {
                                #'analyst': self.analyst_name,
                                'url_uuid': self.model_url.split("-")[-1],
                                'time_lapsed': time_lapsed,
                                'linkedin_content_metrics': [linkedin_metrics.name] if linkedin_metrics else ['Not available'],
                                'linkedin_content_post': [linkedin_post.name] if linkedin_post else ['Not available'],
                                'payload': payload_txt,
                                'result': result,
                            }
                            '''
                            collect_telemetry(debug_info)
                            st.session_state['linkedin_upload'] = 'uploaded'
                            
                            #with st.expander("Debug information", icon="⚙"):
                            #    st.write(debug_info)

                            st.session_state['analyzing'] = False 
                            #for key in st.session_state.keys():
                            #    del st.session_state[session]  
                except AttributeError:
                    st.info("Please upload CSV or PDF files first.")
                    hide_button() 
    
    def row1(self):
            self.linkedin_f = st.text_input("Followers:", placeholder='Enter Linkedin Followers')
            
            followers = {
                'Linkedin Followers': self.linkedin_f if self.linkedin_f else 'N/A'
            }

            self.linkedin_metrics = self.file_upload("linkedin_content_metrics", "Content Metrics CSV", "linkedin_content_metrics")
            self.linkedin_post = self.file_upload("linkedin_content_post", "Content Post CSV", "linkedin_content_post")   
           
            self.linkedin_metrics
            self.linkedin_post
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
