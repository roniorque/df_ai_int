from urllib.parse import urlparse
import streamlit as st
import requests
from dotenv import load_dotenv
import os
from helper.upload_response import upload_response
from helper.upload_File import uploadFile
import json
from pymongo import MongoClient
from helper.data_field import get_analyst_response


class ExecutiveSummary:
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
    
    def request_model(self, payload_txt, headers):
        response = requests.post(self.model_url, json=payload_txt, headers=headers)
        response.raise_for_status()
        output = response.json()
        #st.write(output)
        text = output["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
        #text = json.loads(text)
        #st.write(text)
        return text
    
    def fetch_data(self, data_field):
        mongodb_uri = os.getenv("MONGODB_URI")
        myclient = MongoClient(mongodb_uri)
        mydb = myclient.get_database()
        mycol = mydb["df_data"]
        
        # Sort by timestamp field in descending order
        x = mycol.find_one(
            {"data_field": data_field},
            sort=[("timestamp", -1)]  
        )
        
        x = x["result"]
        return x
    
    def process(self):
                with st.spinner('Executive Summary...', show_time=True):
                        st.write('')
                        headers = {"Content-Type": "application/json", "x-api-key": f"{os.getenv('x-api-key')}"}         
                        try:
                                payload_txt = {"input_value": self.payload, "output_type": "text", "input_type": "chat"}
                                payload_txt_model = self.request_model(payload_txt, headers)
                                debug_info = {'data_field' : 'Executive Summary', 'result': payload_txt_model}
                                upload_response(debug_info)

                        except Exception as e:
                            pass
                        st.session_state['analyzing'] = False    
                      
    def row1(self):
            st.session_state['analyzing'] = False
            self.payload = ""
            
            self.website_and_tools_data = get_analyst_response("Website and Tools Analyst")
            self.sem_data = get_analyst_response("SEM/PPC Analyst")
            self.seo_data = get_analyst_response("SEO Analyst")
            self.on_page_data = get_analyst_response("On Page Analyst")
            self.off_page_data = get_analyst_response("Off Page Analyst")
            self.social_media_data = get_analyst_response("Social Media Analyst")
            self.content_data = get_analyst_response("Content Analyst")
            self.marketpalce_data = get_analyst_response("Marketplace Analyst")
            self.target_market_data = get_analyst_response("Target Market Analyst")
            self.website_audience_data = get_analyst_response("Pull through offers Analyst")
            self.pull_through_data = get_analyst_response("Website Audience Acquisition Analyst")
            self.lld_data = get_analyst_response("LLD/PM/LN Analyst")
            self.pna_data = get_analyst_response("Content - Process and Assets Analyst")
            
            analyst_data_dict = {
                "Website and Tools": self.website_and_tools_data,
                "SEM/PPC": self.sem_data,
                "SEO": self.seo_data,
                "On Page": self.on_page_data,
                "Off Page": self.off_page_data,
                "Social Media": self.social_media_data,
                "Content": self.content_data,
                "Marketplace": self.marketpalce_data,
                "Target Market": self.target_market_data,
                "Pull through offers": self.website_audience_data,
                "Website Audience Acquisition": self.pull_through_data,
                "LLD/PM/LN": self.lld_data,
                "Content - Process and Assets": self.pna_data
            }


            for analyst_name, data in analyst_data_dict.items():
                self.payload += f"\n\n--- {analyst_name} Analysis ---\n"
                if isinstance(data, list):
                    self.payload += "\n".join(map(str, data))
                else:
                    self.payload += str(data)
            
            self.process()
                                       
if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
