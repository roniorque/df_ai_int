import os
import streamlit as st
import threading
from streamlit.runtime.scriptrunner import add_script_run_ctx
from classes.response_off import SeoOffPageAnalyst
from classes.response_on_page import SeoOn
from classes.response_website_and_tools import WebsiteAndTools
from classes.response_seo import Seo
from classes.response_social_media import SocialMedia

def run_analysis():
    # Placeholders for status updates
    off_page_status = st.empty()
    on_page_status = st.empty()
    website_and_tools_status = st.empty()
    seo_status = st.empty()
    social_media_status = st.empty()
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
        
    def run_social_media_analysis():
        try:
            social_media_status.info("Starting Social Media Analysis...")
            result = SocialMedia(os.getenv('MODEL_Social_Media_Analyst'))
            social_media_status.success("Social Media Analysis completed successfully.")
            return result
        except Exception as e:
            social_media_status.error(f"Social Media Analysis failed: {e}")
            return None
        
    # Create threads for concurrent execution
    off_page_thread = threading.Thread(target=run_off_page_analysis)
    on_page_thread = threading.Thread(target=run_on_page_analysis)
    website_and_tools_thread = threading.Thread(target=run_website_and_tools_analysis)
    seo_thread = threading.Thread(target=run_seo_analysis)
    social_media_thread = threading.Thread(target=run_social_media_analysis)

    # Attach Streamlit context to threads
    add_script_run_ctx(off_page_thread)
    add_script_run_ctx(on_page_thread)
    add_script_run_ctx(website_and_tools_thread)
    add_script_run_ctx(seo_thread)
    add_script_run_ctx(social_media_thread)

    # Start threads
    off_page_thread.start()
    on_page_thread.start()
    website_and_tools_thread.start()
    seo_thread.start()
    social_media_thread.start()

    # Wait for threads to complete
    off_page_thread.join()
    on_page_thread.join()
    website_and_tools_thread.join()
    seo_thread.join()
    st.success("🎉 All analyses completed!") # Final success message
    # --- Display Button After Completion ---
    if st.button("View Results"):
        st.switch_page("pages/output.py")
   
    



# Execute the analysis
if st.button("Back"):
        st.switch_page("pages/home.py")
run_analysis()
