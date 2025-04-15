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
        text_amazon = output["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]["amazon"]
        text_ebay = output["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]["ebay"]
        text_amazon = json.loads(text_amazon)
        text_ebay = json.loads(text_ebay)
        text = text_amazon + text_ebay
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
    
    def process (self):    
        with st.spinner('Marketplace Analyst...', show_time=True):
                        st.write('')
                        headers = {"Content-Type": "application/json", "x-api-key": f"{os.getenv('x-api-key')}"}         
                        try:
                                payload_txt = {"input_value": self.payload, "output_type": "text", "input_type": "chat"}
                                payload_txt_model = self.request_model(payload_txt, headers)
                                debug_info = {'data_field' : 'Marketplace Analyst', 'result': payload_txt_model}
                                upload_response(debug_info)

                                st.session_state['product_title_amazon'] = ''
                                st.session_state['images_amazon'] = ''
                                st.session_state['bullet_points_amazon'] = ''
                                st.session_state['product_description_amazon'] = ''
                                st.session_state['product_title_ebay'] = ''
                                st.session_state['category_ebay'] = ''
                                st.session_state['images_ebay'] = ''
                                st.session_state['product_description_ebay'] = ''
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
                session_product_title_amazon = st.session_state['product_title_amazon']
                if session_product_title_amazon == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Product Title - Amazon")
                
            except Exception as e:
                pass
            try:
                session_images_amazon = st.session_state['images_amazon']
                if session_images_amazon == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Images - Amazon")
            except Exception as e:
                pass
            try:
                session_bullet_points_amazon = st.session_state['bullet_points_amazon']
                if session_bullet_points_amazon == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Bullet Points - Amazon")
                
            except Exception as e:
                pass
            try:
                session_product_description_amazon = st.session_state['product_description_amazon']
                if session_product_description_amazon == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Product Description - Amazon")            
            except Exception as e:
                pass
            try:
                session_product_title_ebay = st.session_state['product_title_ebay']
                if session_product_title_ebay == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Product Title - eBay")                 
            except Exception as e:
                pass
            try:
                session_category_ebay = st.session_state['category_ebay']
                if session_category_ebay == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Category - eBay")                 
            except Exception as e:
                pass
            try:
                session_images_ebay = st.session_state['images_ebay']
                if session_images_ebay == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Images - eBay")                 
            except Exception as e:
                pass
            try:
                session_product_description_ebay = st.session_state['product_description_ebay']
                if session_product_description_ebay == 'uploaded':
                    count += 1
                    self.payload += self.fetch_data("Product Description - eBay")                 
            except Exception as e:
                pass

            if count >= 1:
                summary = self.fetch_data("Client Summary")
                self.payload = summary + self.payload
                self.process()
            

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
