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
from classes.response_target_market import TargetMarket
from classes.response_executive_summary import ExecutiveSummary
from classes.response_snapshot import Snapshot

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
    sem_ppc_status = st.empty()
    marketplace_status = st.empty()
    target_market_status = st.empty()
    executive_summary_status = st.empty()
    snapshot_status = st.empty()

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
            website_and_tools_status.error(f"Website and Tools Analysis failed: {e}")
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
            sem_ppc_status.info("Starting SEM/PPC Analysis...")
            result = Sem_PPC(os.getenv('Model_SEM_PPC_Analyst'))
            sem_ppc_status.success("SEM/PPC Analysis completed successfully.")
            return result
        except Exception as e:
            sem_ppc_status.error(f"SEM/PPC Analysis failed: {e}")
            return None
        
    def run_marketplace_analysis():
        try:
            marketplace_status.info("Starting Marketplace Analysis...")
            result = Marketplace(os.getenv('Model_SEM_PPC_Analyst'))
            marketplace_status.success("Marketplace Analysis completed successfully.")
            return result
        except Exception as e:
            marketplace_status.error(f"Marketplace Analysis failed: {e}")
            return None
    
    def run_target_market_analysis():
        try:
            target_market_status.info("Starting Target Market Analysis...")
            result = TargetMarket(os.getenv('Model_Target_Market_Analyst'))
            target_market_status.success("Target Market Analysis completed successfully.")
            return result
        except Exception as e:
            target_market_status.error(f"Target Market Analysis failed: {e}")
            return None

    def run_snapshot_analysis():
        try:
            snapshot_status.info("Starting Snapshot by Channel Analysis...")
            result = Snapshot(os.getenv('Model_Snapshot_by_Channel_Analyst'))
            snapshot_status.success("Snapshot by Channel Analysis completed successfully.")
            return result
        except Exception as e:
            snapshot_status.error(f"Snapshot by Channel Analysis failed: {e}")
            return None

    def run_executive_summary_analysis():
        try:
            executive_summary_status.info("Starting Executive Summary Analysis...")
            result = ExecutiveSummary(os.getenv('Model_Executive_Summary_Analyst'))
            executive_summary_status.success("Executive Summary Analysis completed successfully.")
            return result
        except Exception as e:
            executive_summary_status.error(f"Executive Summary Analysis failed: {e}")
            return None
    
    # Create threads for first batch of concurrent execution
    first_batch_threads = [
        threading.Thread(target=run_off_page_analysis),
        threading.Thread(target=run_on_page_analysis),
        threading.Thread(target=run_website_and_tools_analysis),
        threading.Thread(target=run_seo_analysis),
        threading.Thread(target=run_social_media_analysis),
        threading.Thread(target=run_lld_pm_ln),
        threading.Thread(target=run_pull_through_offers),
        threading.Thread(target=run_content),
        threading.Thread(target=run_sem_ppc_analysis),
        threading.Thread(target=run_marketplace_analysis),
        threading.Thread(target=run_target_market_analysis)
    ]

    # Attach Streamlit context to first batch threads
    for thread in first_batch_threads:
        add_script_run_ctx(thread)

    # Start first batch threads
    for thread in first_batch_threads:
        thread.start()

    # Wait for first batch threads to complete
    for thread in first_batch_threads:
        thread.join()

    st.markdown("---")
    st.info("Initial analyses completed. Now generating Summary reports...")

    # Create threads for second batch of concurrent execution (Snapshot and Executive Summary)
    second_batch_threads = [
        threading.Thread(target=run_snapshot_analysis),
        threading.Thread(target=run_executive_summary_analysis)
    ]

    # Attach Streamlit context to second batch threads
    for thread in second_batch_threads:
        add_script_run_ctx(thread)

    # Start second batch threads
    for thread in second_batch_threads:
        thread.start()

    # Wait for second batch threads to complete
    for thread in second_batch_threads:
        thread.join()

    st.success("🎉 All analyses completed!") # Final success message

    # --- Display Button After Completion ---
    if st.button("View Results", icon="📃"):
        st.switch_page("pages/output.py")

# Execute the analysis
if st.button("Back"):
    st.switch_page("pages/home.py")
run_analysis()