import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import pandas._libs.tslibs.parsing
import time
import chardet
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button
from helper.initialize_analyze_session import initialize_analyze_session
from pymongo import MongoClient
from helper.data_field import data_field
from helper.upload_response import upload_response
import json

class Seo:
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

        # EVALUATION FORM LINK
        '''url = os.getenv('Link')
        st.write('Evaluation Form: [Link](%s)' % url)

        # RETURN BUTTON
        try:
            if st.button("Return", type='primary'):
                st.switch_page("./pages/home.py")
        except Exception:
            pass'''
    
    def request_model(self, payload_txt, headers):
        response = requests.post(self.model_url, json=payload_txt, headers=headers)
        response.raise_for_status()
        output = response.json()
        #st.write(output)
        text = output["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
        text = json.loads(text)
        #st.write(text)
        return text
    
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
    
    def detect_encoding(self, uploaded_file):
        result = chardet.detect(uploaded_file.read(100000))
        uploaded_file.seek(0)  # Reset file pointer to the beginning
        return result['encoding']

    def keyword_ranking(self, df_seo):
        keyword_ranking = df_seo
        st.session_state['keyword_ranking'] = keyword_ranking

        keywords_ranking_sorted = keyword_ranking.sort_values("Position", ascending=True)

        keywords_ranking_top_10 = keywords_ranking_sorted[keywords_ranking_sorted["Position"] <= 10].shape[0]
        keywords_ranking_top_100 = keywords_ranking_sorted[keywords_ranking_sorted["Position"] <= 100].shape[0]

        keyword_ranking = {
            'Keyword_top_10': keywords_ranking_top_10,
            'Keyword_top_100': keywords_ranking_top_100
        }
        st.session_state['keyword_ranking'] = keyword_ranking

    def traffic_files(self, df_traffic):
        traffic_channels = df_traffic
        try:
            traffic_channels.rename(columns={traffic_channels.columns[0]: 'date'}, inplace=True)
            traffic_channels['date'] = pd.to_datetime(traffic_channels['date'], format='mixed')
        except pandas._libs.tslibs.parsing.DateParseError:
            pass
        traffic_channels_sort = traffic_channels.sort_values("date", ascending=False)

        organic_traffic = traffic_channels_sort['Organic Search'].values[0]
        paid_traffic = traffic_channels_sort['Paid Search'].values[0]
        direct_traffic = traffic_channels_sort['Direct'].values[0]
        referral_traffic = traffic_channels_sort['Referral'].values[0]

        st.session_state['organic_traffic'] = organic_traffic
        st.session_state['paid_traffic'] = paid_traffic
        st.session_state['direct_traffic'] = direct_traffic
        st.session_state['referral_traffic'] = referral_traffic
   
    def ga4_traffic(self, others):
        st.session_state['others'] = others

        ga4_paid_social = others['Sessions'].values[0]
        ga4_organic_traffic = others['Sessions'].values[4]
        ga4_direct_traffic = others['Sessions'].values[2]
        ga4_referral_traffic = others['Sessions'].values[3]
        
        st.session_state['ga4_paid_social'] = ga4_paid_social
        st.session_state['ga4_organic_traffic'] = ga4_organic_traffic
        st.session_state['ga4_direct_traffic'] = ga4_direct_traffic
        st.session_state['ga4_referral_traffic'] = ga4_referral_traffic

    def delete_sessions(self):
        try:
            del st.session_state['df_traffic']
            del st.session_state['others']
            del st.session_state['df_seo']
            del st.session_state['keyword_ranking']   
            del st.session_state['ga4_paid_social']
            del st.session_state['ga4_organic_traffic']
            del st.session_state['ga4_direct_traffic']
            del st.session_state['ga4_referral_traffic']
            del st.session_state['organic_traffic']
            del st.session_state['paid_traffic']
            del st.session_state['direct_traffic']
            del st.session_state['referral_traffic']
        except KeyError:
            pass
    
    def process (self):    
        with st.spinner('Seo Analyst...', show_time=True):
                        st.write('')
                        headers = {"Content-Type": "application/json", "x-api-key": f"{os.getenv('x-api-key')}"}         
                        try:
                                payload_txt = {"input_value": self.payload, "output_type": "text", "input_type": "chat"}
                                payload_txt_model = self.request_model(payload_txt, headers)
                                debug_info = {'data_field' : 'SEO Analyst', 'result': payload_txt_model}
                                upload_response(debug_info)

                                st.session_state['bounce_rate'] = ''
                                st.session_state['pages_index'] = ''
                                st.session_state['others'] = ''
                                st.session_state['df_traffic'] = ''
                                st.session_state['df_seo'] = ''
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
                session_traffic_aqcuisition = st.session_state['df_seo']
                if session_traffic_aqcuisition == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("SEO Keywords")
                
            except Exception as e:
                pass
            try:
                session_traffic_channels = st.session_state['df_traffic']
                if session_traffic_channels == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Traffic Channels")
            except Exception as e:
                pass
            try:
                session_others = st.session_state['others']
                if session_others == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Traffic Acquisition")
                
            except Exception as e:
                pass
            try:
                session_page_index = st.session_state['pages_index']
                if session_page_index == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Pages Indexed")            
            except Exception as e:
                pass
            try:
                session_bounce_rate = st.session_state['bounce_rate']
                if session_bounce_rate == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Bounce Rate")                 
            except Exception as e:
                pass
            try:
                session_backlinks = st.session_state["off_page_file_uploaded"] 
                if session_backlinks == 'uploaded':
                    self.payload += self.fetch_backlinks("Backlinks") 
            except Exception as e:
                pass

            if count >= 1:
                summary = self.fetch_data("Client Summary")
                self.payload = summary + self.payload
                self.process()
            

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
