import streamlit as st
import requests
from dotenv import load_dotenv
import os
import time
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button
from helper.initialize_analyze_session import initialize_analyze_session
import json

class LeadListAnalyst:
    def __init__(self, model_url, analyst_name, data_src, analyst_description):
        self.model_url = model_url
        self.analyst_name = analyst_name
        self.data_src = data_src
        self.analyst_description = analyst_description
        self.initialize()
        self.row1()

    def initialize(self):
        # FOR ENV
        load_dotenv()

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
    
    def request_model(self, payload_txt):
        response = requests.post(self.model_url, json=payload_txt)
        response.raise_for_status()
        output = response.json()
        text = output["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
        text = json.loads(text)
   
        lead_list_dev = text["lead_list_development"]
        prospecting_mech = text["prospecting_mechanism"]
        lead_nurt = text["lead_nurturing"]
        
        with st.expander("AI Analyst", expanded=True, icon="🤖"):
            st.write(f"**Lead List Development**:\n {lead_list_dev}\n")
            st.write(f"\n**Prospecting Mechanism**: {prospecting_mech}")
            st.write(f"\n**Lead Nurturing**: {lead_nurt}")
        
        return output
 
    def row1(self):
        col1, col2 = st.columns(gap="medium", spec=[0.33, 0.66])
        with col1:
            lead_list = st.checkbox("Lead List Development", key='lead_list')
            pros_mech = st.checkbox("Prospecting Mechanism", key='pros_mech')
            lead_nur = st.checkbox("Lead Nurturing", key='lead_nur')
            self.lead_gen = st.text_area("What are the Lead Generation/s?", height=200 , placeholder='Enter Lead Generation/s', key='lead_gen')
            self.crm = st.text_input("What CRM are they using? N/A if None", placeholder='Enter CRM', key='crm')
        with col2:
            st.write("") # FOR THE HIDE BUTTON
            st.write("") # FOR THE HIDE BUTTON
            st.write("AI Analyst Output: ")
            st.session_state['analyzing'] = False
            st.write("") # FOR THE HIDE BUTTON
            analyze_button = st.button("Analyze", disabled=initialize_analyze_session())
            start_time = time.time()
            if analyze_button:
                hide_button()
                if lead_list or pros_mech or lead_nur:
                    combined_text = ""
                    with st.spinner('Analyzing...', show_time=True):
                        st.write('')
                        # INITIALIZING SESSIONS
                        
                        combined_text += f"Lead List Development: {lead_list}\n"
                        combined_text += f"Prospecting Mechanism: {pros_mech}\n"
                        combined_text += f"Lead Nurturing: {lead_nur}\n"
                            
                        combined_text += f"\nWhat are the Lead Generation/s they are using?: {self.lead_gen}\n"
                        if not self.crm:
                            self.crm = "None"
                        combined_text += f"\nWhat CRM are they using?: {self.crm}"

                        # OUTPUT FOR SEO ANALYST
                        payload_txt = {"input_value": combined_text,
                                       "output_type": "text",
                                       "input_type": "chat"
                                       }
                        result = self.request_model(payload_txt)

                        end_time = time.time()
                        time_lapsed = end_time - start_time
                        debug_info = {
                            'analyst': self.analyst_name,
                            'url_uuid': self.model_url.split("-")[-1],
                            'time_lapsed': time_lapsed,
                            'payload': payload_txt,
                            'result': result,
                        }

                        collect_telemetry(debug_info)

                        with st.expander("Debug information", icon="⚙"):
                            st.write(debug_info)

                        st.session_state['analyzing'] = False 
                else:
                    st.info("Please upload CSV or PDF files first.")
                    hide_button()
            
if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
