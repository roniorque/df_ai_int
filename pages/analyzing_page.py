import os
import streamlit as st
import threading
from streamlit.runtime.scriptrunner import add_script_run_ctx
from classes.response_off import SeoOffPageAnalyst
from classes.response_on_page import SeoOn
from classes.response_website_and_tools import WebsiteAndTools
from classes.response_seo import Seo
from classes.response_social_media import SocialMedia
from classes.response_lld_pm_ln import LLD_PM_LN
from classes.response_pull_through_offers import PullThroughOffers
from classes.response_content import Content
from classes.response_sem_ppc import Sem_PPC
from classes.response_marketplace import Marketplace

def run_analysis():
    # Placeholders for status updates
    off_page_status = st.empty()
    on_page_status = st.empty()
    website_and_tools_status = st.empty()
    seo_status = st.empty()
    social_media_status = st.empty()
    lld_pm_ln_status = st.empty()
    pull_through_offers_status = st.empty()
    content_status = st.empty()
    sem_ppc = st.empty()
    marketplace = st.empty()

    def run_off_page_analysis():
        try:
            off_page_status.info("Starting SEO Off Page Analysis...")
            result = SeoOffPageAnalyst(os.getenv('MODEL_Off_Page_Analyst'))
            off_page_status.success("SEO Off Page Analysis completed successfully.")
            return result
        except Exception as e:
            off_page_status.error(f"SEO Off Page Analysis failed: {e}")
            return None

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
        
    def run_lld_pm_ln():
        try:
            lld_pm_ln_status.info("Starting LLD/PM/LN Analysis...")
            result = LLD_PM_LN(os.getenv('Model_LLD_PM_LN_ANALYST'))
            lld_pm_ln_status.success("LLD/PM/LN completed successfully.")
            return result
        except Exception as e:
            lld_pm_ln_status.error(f"LLD/PM/LN Analysis failed: {e}")
            return None
        
    def run_pull_through_offers():
        try:
            pull_through_offers_status.info("Starting Pull through offer Analysis...")
            result = PullThroughOffers(os.getenv('Model_Pull_Through_Offers_Analyst'))
            pull_through_offers_status.success("Pull through offer completed successfully.")
            return result
        except Exception as e:
            pull_through_offers_status.error(f"Pull through offer Analysis failed: {e}")
            return None
        
    def run_content():
        try:
            content_status.info("Starting Content Analysis...")
            result = Content(os.getenv('Model_Content'))
            content_status.success("Content Analysis completed successfully.")
            return result
        except Exception as e:
            content_status.error(f"Content Analysis failed: {e}")
            return None
        
    def run_sem_ppc_analysis():
        try:
            sem_ppc.info("Starting SEM/PPC Analysis...")
            result = Sem_PPC(os.getenv('Model_SEM_PPC_Analyst'))
            sem_ppc.success("SEM/PPC Analysis completed successfully.")
            return result
        except Exception as e:
            sem_ppc.error(f"SEM/PPC Analysis failed: {e}")
            return None
        
    def run_marketplace_analysis():
        try:
            marketplace.info("Starting Marketplace Analysis...")
            result = Marketplace(os.getenv('Model_SEM_PPC_Analyst'))
            marketplace.success("Marketplace Analysis completed successfully.")
            return result
        except Exception as e:
            marketplace.error(f"Marketplace Analysis failed: {e}")
            return None
    
    # Create threads for concurrent execution
    off_page_thread = threading.Thread(target=run_off_page_analysis)
    on_page_thread = threading.Thread(target=run_on_page_analysis)
    website_and_tools_thread = threading.Thread(target=run_website_and_tools_analysis)
    seo_thread = threading.Thread(target=run_seo_analysis)
    social_media_thread = threading.Thread(target=run_social_media_analysis)
    llm_pm_ln_thread = threading.Thread(target=run_lld_pm_ln)
    pull_through_offers_thread = threading.Thread(target=run_pull_through_offers)
    content_thread = threading.Thread(target=run_content)
    content_sem_ppc_thread = threading.Thread(target=run_sem_ppc_analysis)
    marketplace_thread = threading.Thread(target=run_marketplace_analysis)

    # Attach Streamlit context to threads
    add_script_run_ctx(off_page_thread)
    add_script_run_ctx(on_page_thread)
    add_script_run_ctx(website_and_tools_thread)
    add_script_run_ctx(seo_thread)
    add_script_run_ctx(social_media_thread)
    add_script_run_ctx(llm_pm_ln_thread)
    add_script_run_ctx(pull_through_offers_thread)
    add_script_run_ctx(content_thread)
    add_script_run_ctx(content_sem_ppc_thread)
    add_script_run_ctx(marketplace_thread)

    # Start threads
    off_page_thread.start()
    on_page_thread.start()
    website_and_tools_thread.start()
    seo_thread.start()
    social_media_thread.start()
    llm_pm_ln_thread.start()
    pull_through_offers_thread.start()
    content_thread.start()
    content_sem_ppc_thread.start()
    marketplace_thread.start()

    # Wait for threads to complete
    off_page_thread.join()
    on_page_thread.join()
    website_and_tools_thread.join()
    seo_thread.join()
    social_media_thread.join()
    llm_pm_ln_thread.join()
    pull_through_offers_thread.join()
    content_thread.join()
    content_sem_ppc_thread.join()
    marketplace_thread.join()

    st.success("🎉 All analyses completed!") # Final success message
    # --- Display Button After Completion ---
    if st.button("View Results"):
        st.switch_page("pages/output.py")

# Execute the analysis
if st.button("Back"):
        st.switch_page("pages/home.py")
run_analysis()
