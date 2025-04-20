import streamlit as st
import threading
from dotenv import load_dotenv
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button

class ThreadSafeHandler:
    def __init__(self, placeholder):
        self.placeholder = placeholder
        self.lock = threading.Lock()

    def update_info(self, message):
        with self.lock:
            try:
                self.placeholder.info(message)
            except Exception:
                pass

    def update_success(self, message):
        with self.lock:
            try:
                self.placeholder.success(message)
            except Exception:
                pass

    def update_error(self, message):
        with self.lock:
            try:
                self.placeholder.error(message)
            except Exception:
                pass

class Sem_PPC:
    def __init__(self, model_url):
        self.file_dict = {}
        self.model_url = model_url
        self.initialize()
        self.row1()

    def initialize(self):
        load_dotenv()
        # Initialize session state for various ads
        for ad_type in ['account_set_up', 'search_ads', 'display_ads', 'mobile_ads', 'video_ads', 'shopping_ads']:
            if ad_type not in st.session_state:
                st.session_state[ad_type] = ''

    def process(self):
        session = st.session_state.analyze
        if any([self.account_set_up, self.search_ads, self.display_ads, self.mobile_ads, self.video_ads, self.shopping_ads]) and session == 'clicked':
            try:
                # Prepare ad data
                ad_data = {
                    'account_set_up': self.account_set_up,
                    'search_ads': self.search_ads,
                    'display_ads': self.display_ads,
                    'mobile_ads': self.mobile_ads,
                    'video_ads': self.video_ads,
                    'shopping_ads': self.shopping_ads
                }

                # Placeholder to display feedback
                handler = ThreadSafeHandler(st.empty())

                def upload_ads_data(ad_key, ad_value):
                    try:
                        handler.update_info(f"Uploading {ad_key.replace('_', ' ').title()}...")
                        # Simulate the processing logic here
                        st.session_state[ad_key] = 'uploaded'  # Mock upload success
                        collect_telemetry({'data_field': ad_key.replace('_', ' ').title(), 'result': ad_value})
                        handler.update_success(f"{ad_key.replace('_', ' ').title()} completed.")
                    except Exception as e:
                        handler.update_error(f"Error uploading {ad_key.replace('_', ' ').title()}: {e}")

                # Start threads for each ad type
                threads = []
                for ad_key, ad_value in ad_data.items():
                    thread = threading.Thread(target=upload_ads_data, args=(ad_key, ad_value))
                    thread.start()
                    threads.append(thread)

                # Wait for all threads to complete
                for t in threads:
                    t.join()

                # Update session after processing
                st.session_state['analyzing'] = False
                st.success("🎉 SEM/PPC Data Uploaded Successfully!")
            except AttributeError:
                st.info("Please upload CSV or PDF files first.")
                hide_button()

    def row1(self):
        self.account_set_up = st.text_input("Account Set Up - Google Ads:", placeholder='Enter Account Set Up')
        self.search_ads = st.checkbox("Search Ads - Google Ads/SEMRush")
        self.display_ads = st.checkbox("Display Ads - Google Ads/SEMRush")
        self.mobile_ads = st.checkbox("Mobile Ads - Google Ads")
        self.video_ads = st.checkbox("Video Ads - Google Ads")
        self.shopping_ads = st.checkbox("Shopping Ads - Google Ads/SEMRush")

        self.process()  # Call process method to initiate processing

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    upload = uploadFile()  # Assuming this is another helper class handling file uploads
