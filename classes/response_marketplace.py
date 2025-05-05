import streamlit as st
import requests
from dotenv import load_dotenv
import os
from helper.upload_File import uploadFile
from pymongo import MongoClient
from helper.upload_response import upload_response
import json

class Marketplace:
    def __init__(self, model_url):
        self.model_url = model_url
        self.run_all = (st.session_state.get('run_all', {}))
        #self.analyst_name = analyst_name
        #self.data_src = data_src
        #self.analyst_description = analyst_description
        self.initialize()
        self.row1()

    def initialize(self):
        # FOR ENV
        load_dotenv()

            
    def request_model(self, payload_txt, headers):
        response = requests.post(self.model_url, json=payload_txt, headers=headers)
        response.raise_for_status()
        output = response.json()
        #st.write(output)
        text_amazon = output["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
        text_amazon = json.loads(text_amazon)
        #text_ebay = json.loads(text_ebay)
        #text = text_amazon + text_ebay
        #st.write(text_amazon)
        return text_amazon
    
    def fetch_backlinks(self, data_field):
        mongodb_uri = os.getenv("MONGODB_URI")
        myclient = MongoClient(mongodb_uri)
        mydb = myclient.get_database()
        mycol = mydb["df_data"]
        x = mycol.find_one({"data_field": data_field})
        x = x["result"]['question']
        return x
    
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
    
    def process (self):    
        with st.spinner('Marketplace Analyst...', show_time=True):
                        st.write('')
                        headers = {"Content-Type": "application/json", "x-api-key": f"{os.getenv('x_api_key')}"}         
                        try:
                                payload_txt = {"input_value": self.payload, "output_type": "text", "input_type": "chat"}
                                payload_txt_model = self.request_model(payload_txt, headers)
                                debug_info = {'data_field' : 'Marketplace Analyst', 'result': payload_txt_model}
                                upload_response(debug_info)
                               
                                st.session_state['amazon_marketplace_questionnaires'] = ''
                                st.session_state['ebay_marketplace_questionnaires'] = ''
                                count = 0
                        except Exception as e:
                            pass
                        st.session_state['analyzing'] = False    
             
    def row1(self):
            st.session_state['analyzing'] = False
            #st.write("") # FOR THE HIDE BUTTON
            #analyze_button = st.button("Analyze", disabled=initialize_analyze_session())
            self.payload = ""  
            count = 0
            
            try:
                session_amazon_marketplace_questionnaires = st.session_state['amazon_marketplace_questionnaires']
                if session_amazon_marketplace_questionnaires == 'uploaded' or self.run_all == True:
                    count += 1
                    self.payload += self.fetch_data("Marketplace Questionnaires - Amazon")                 
            except Exception as e:
                pass
            
            try:
                session_ebay_marketplace_questionnaires = st.session_state['ebay_marketplace_questionnaires']
                if session_ebay_marketplace_questionnaires == 'uploaded' or self.run_all == True:
                    count += 1
                    self.payload += self.fetch_data("Marketplace Questionnaires - eBay")                 
            except Exception as e:
                pass

            if count >= 1:
                summary = self.fetch_data("Client Summary")
                self.payload = summary + self.payload
                self.process()
            

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
