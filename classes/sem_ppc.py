import streamlit as st
import threading
from dotenv import load_dotenv
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button


class Sem_PPC:
    def __init__(self, model_url):
        self.file_dict = {}
        self.model_url = model_url
        load_dotenv()
        self.initialize()
        self.row1()

    def initialize(self):
        for key in ['account_set_up', 'search_ads', 'display_ads', 'mobile_ads', 'video_ads', 'shopping_ads']:
            if key not in st.session_state:
                st.session_state[key] = ''

    def run_in_background(self):
        try:
            account_set_up = f"\nAccount Set Up: {self.account_set_up}" if self.account_set_up else ""
            search_ads = "\nSearch Ads" if self.search_ads else ""
            display_ads = "\nDisplay Ads" if self.display_ads else ""
            mobile_ads = "\nMobile Ads" if self.mobile_ads else ""
            video_ads = "\nVideo Ads" if self.video_ads else ""
            shopping_ads = "\nShopping Ads" if self.shopping_ads else ""

            # Simulated payload / model call here if needed

            # Logging/Telemetry (each individually)
            if self.account_set_up:
                st.session_state['account_set_up'] = 'uploaded'
                collect_telemetry({'data_field': 'Account Set Up - Google Ads', 'result': account_set_up})
            if self.search_ads:
                st.session_state['search_ads'] = 'uploaded'
                collect_telemetry({'data_field': 'Search Ads - Google Ads/SEMRush', 'result': search_ads})
            if self.display_ads:
                st.session_state['display_ads'] = 'uploaded'
                collect_telemetry({'data_field': 'Display Ads - Google Ads/SEMRush', 'result': display_ads})
            if self.mobile_ads:
                st.session_state['mobile_ads'] = 'uploaded'
                collect_telemetry({'data_field': 'Mobile Ads - Google Ads', 'result': mobile_ads})
            if self.video_ads:
                st.session_state['video_ads'] = 'uploaded'
                collect_telemetry({'data_field': 'Video Ads - Google Ads', 'result': video_ads})
            if self.shopping_ads:
                st.session_state['shopping_ads'] = 'uploaded'
                collect_telemetry({'data_field': 'Shopping Ads - Google Ads/SEMRush', 'result': shopping_ads})

        except Exception as e:
            st.error(f"Error during SEM/PPC processing: {e}")

        st.session_state['analyzing'] = False

    def process(self):
        session = st.session_state.get('analyze')
        if session == 'clicked' and (
            self.account_set_up or self.search_ads or self.display_ads or
            self.mobile_ads or self.video_ads or self.shopping_ads
        ):
            try:
                with st.spinner("Uploading SEM/PPC..."):
                    # Launch processing thread
                    thread = threading.Thread(target=self.run_in_background)
                    thread.start()
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

        self.process()


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    upload = uploadFile()
