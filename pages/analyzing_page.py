import os
import streamlit as st
import threading
from streamlit.runtime.scriptrunner import add_script_run_ctx
from classes.response_off import SeoOffPageAnalyst
from classes.response_on_page import SeoOn
from classes.response_website_and_tools import WebsiteAndTools
from classes.response_seo import Seo

def run_analysis():
    # Retrieve uploaded files from session state
    off_page_file = st.session_state.get('off_page_file_uploaded')
    gt_file = st.session_state.get('GT_file_uploaded')
    website_and_tools = st.session_state.get('website_and_tools')
    seo = st.session_state.get('seo')
    # Placeholders for status updates
    off_page_status = st.empty()
    on_page_status = st.empty()
    website_and_tools_status = st.empty()
    seo_status = st.empty()
    # Function to run SEO Off Page Analysis
    def run_off_page_analysis():
        try:
            off_page_status.info("Starting SEO Off Page Analysis...")
            result = SeoOffPageAnalyst(os.getenv('MODEL_Off_Page_Analyst'))
            off_page_status.success("SEO Off Page Analysis completed successfully.")
            return result
        except Exception as e:
            off_page_status.error(f"SEO Off Page Analysis failed: {e}")
            return None

    # Function to run On Page Analysis
    def run_on_page_analysis():
        try:
            on_page_status.info("Starting On Page Analysis...")
            result = SeoOn(os.getenv('MODEL_On_Page_Analyst'))
            on_page_status.success("On Page Analysis completed successfully.")
            return result
        except Exception as e:
            on_page_status.error(f"On Page Analysis failed: {e}")
            return None
    
    def run_website_and_tools_analysis():
        try:
            website_and_tools_status.info("Starting Website and Tools Analysis...")
            result = WebsiteAndTools(os.getenv('Model_Website_and_Tools_Analyst'))
            website_and_tools_status.success("Website and Tools completed successfully.")
            return result
        except Exception as e:
            on_page_status.error(f"Website and Tools Analysis failed: {e}")
            return None
    def run_seo_analysis():
        try:
            seo_status.info("Starting SEO Analysis...")
            result = Seo(os.getenv('MODEL_SEO_Analyst'))
            seo_status.success("SEO Analysis completed successfully.")
            return result
        except Exception as e:
            seo_status.error(f"SEO Analysis failed: {e}")
            return None
        
    # Create threads for concurrent execution
    off_page_thread = threading.Thread(target=run_off_page_analysis)
    on_page_thread = threading.Thread(target=run_on_page_analysis)
    website_and_tools_thread = threading.Thread(target=run_website_and_tools_analysis)
    seo_thread = threading.Thread(target=run_seo_analysis)

    # Attach Streamlit context to threads
    add_script_run_ctx(off_page_thread)
    add_script_run_ctx(on_page_thread)
    add_script_run_ctx(website_and_tools_thread)
    add_script_run_ctx(seo_thread)

    # Start threads
    off_page_thread.start()
    on_page_thread.start()
    website_and_tools_thread.start()
    seo_thread.start()

    # Wait for threads to complete
    off_page_thread.join()
    on_page_thread.join()
    website_and_tools_thread.join()
    seo_thread.join()

# Execute the analysis
run_analysis()
