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

class TargetMarketAnalyst:
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
        text = text[0]

        target_market = text["target_market"]
        demographics = text["demographics"]
        summary = text["summary"]
        
        with st.expander("AI Analyst", expanded=True, icon="🤖"):
            st.write(f"**Target Market**:\n {target_market}\n")
            st.write(f"\n**Product / Service Demographics**: {demographics}")
            st.write(f"\n**Marketing Message Summary**: {summary}")
        
        return output
 
    def row1(self):
        col1, col2 = st.columns(gap="medium", spec=[0.33, 0.66])
        with col1:
            self.business_name = st.text_input("Business Name: ", placeholder='Enter Business Name', key='business_name')
            self.products = st.text_area("Product/s: ", placeholder='Enter Product/s', key='product')
            self.area = st.text_input("Area of Business: ", placeholder='Enter Area of Business', key='area')
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
                if self.business_name and self.products and self.area:
                    combined_text = ""
                    with st.spinner('Analyzing...', show_time=True):
                        st.write('')
                        # INITIALIZING SESSIONS
                        
                        combined_text += f"Business Name: {self.business_name}\n"
                        combined_text += f"Product/s: {self.products}\n"
                        combined_text += f"Area of Business: {self.area}\n"
                            

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
