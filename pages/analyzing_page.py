import os
import streamlit as st
import threading
import time
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
from classes.response_df_overview import dfOverview
from classes.response_desired_outcome import DesiredOutcome
from classes.response_conversion_analyst import ConversionAnalyst
from classes.response_website_audience_acquisition import WebsiteAudienceAcquisition
from classes.response_content_process_and_assets_analyst import Content_Process_and_Assets_Analyst
from classes.response_connection_analyst import ConnectionAnalyst
from classes.response_executive_summary import ExecutiveSummary
from classes.response_snapshot import Snapshot

# Initialize session state to track if analysis has been run
if 'analysis_completed' not in st.session_state:
    st.session_state.analysis_completed = False

# Create a thread-safe way to update the UI
class ThreadSafeAnalysis:
    def __init__(self, placeholder, name):
        self.placeholder = placeholder
        self.name = name
        self.lock = threading.Lock()
        
    def update_info(self, message):
        with self.lock:
            try:
                self.placeholder.info(message)
            except Exception:
                # Silently ignore errors here - this prevents "bad set index" errors
                pass
            
    def update_success(self, message):
        with self.lock:
            try:
                self.placeholder.success(message)
            except Exception:
                # Silently ignore errors here
                pass
            
    def update_error(self, message):
        with self.lock:
            try:
                self.placeholder.error(message)
            except Exception:
                # Silently ignore errors here
                pass

def run_analysis():
    st.write(st.session_state.get('run_all', {}))
    pass
    # Create placeholders for status updates
    placeholders = {
        "off_page": st.empty(),
        "on_page": st.empty(),
        "website_tools": st.empty(),
        "seo": st.empty(),
        "social_media": st.empty(),
        "lld_pm_ln": st.empty(),
        "pull_through": st.empty(),
        "content": st.empty(),
        "sem_ppc": st.empty(),
        "marketplace": st.empty(),
        "target_market": st.empty(),
        "df_overview": st.empty(),
        "desired_outcome": st.empty(),
        "conversion": st.empty(),
        "website_audience": st.empty(),
        "content_process_and_assets": st.empty(),
        "connection": st.empty(),
        "snapshot": st.empty(),
        "executive_summary": st.empty(),
        
    }
    
    # Create thread-safe handlers for each analysis type
    handlers = {name: ThreadSafeAnalysis(placeholder, name) 
                for name, placeholder in placeholders.items()}
    
    # Define all analysis functions
    def run_off_page_analysis():
        handler = handlers["off_page"]
        try:
            handler.update_info("Running SEO Off Page Analysis...")
            result = SeoOffPageAnalyst(os.getenv('MODEL_Off_Page_Analyst'))
            handler.update_success("SEO Off Page Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"SEO Off Page Analysis failed: {str(e)}")
            return None

    def run_on_page_analysis():
        handler = handlers["on_page"]
        try:
            handler.update_info("Running On Page Analysis...")
            result = SeoOn(os.getenv('MODEL_On_Page_Analyst'))
            handler.update_success("On Page Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"On Page Analysis failed: {str(e)}")
            return None
    
    def run_website_and_tools_analysis():
        handler = handlers["website_tools"]
        try:
            handler.update_info("Running Website and Tools Analysis...")
            result = WebsiteAndTools(os.getenv('Model_Website_and_Tools_Analyst'))
            handler.update_success("Website and Tools completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"Website and Tools Analysis failed: {str(e)}")
            return None
        
    def run_seo_analysis():
        handler = handlers["seo"]
        try:
            handler.update_info("Running SEO Analysis...")
            result = Seo(os.getenv('MODEL_SEO_Analyst'))
            handler.update_success("SEO Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"SEO Analysis failed: {str(e)}")
            return None
        
    def run_social_media_analysis():
        handler = handlers["social_media"]
        try:
            handler.update_info("Running Social Media Analysis...")
            result = SocialMedia(os.getenv('MODEL_Social_Media_Analyst'))
            handler.update_success("Social Media Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"Social Media Analysis failed: {str(e)}")
            return None
        
    def run_lld_pm_ln():
        handler = handlers["lld_pm_ln"]
        try:
            handler.update_info("Running LLD/PM/LN Analysis...")
            result = LLD_PM_LN(os.getenv('Model_LLD_PM_LN_ANALYST'))
            handler.update_success("LLD/PM/LN completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"LLD/PM/LN Analysis failed: {str(e)}")
            return None
        
    def run_pull_through_offers():
        handler = handlers["pull_through"]
        try:
            handler.update_info("Running Pull through offer Analysis...")
            result = PullThroughOffers(os.getenv('Model_Pull_Through_Offers_Analyst'))
            handler.update_success("Pull through offer completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"Pull through offer Analysis failed: {str(e)}")
            return None
        
    def run_content():
        handler = handlers["content"]
        try:
            handler.update_info("Running Content Analysis...")
            result = Content(os.getenv('Model_Content'))
            handler.update_success("Content Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"Content Analysis failed: {str(e)}")
            return None
        
    def run_sem_ppc_analysis():
        handler = handlers["sem_ppc"]
        try:
            handler.update_info("Running SEM/PPC Analysis...")
            result = Sem_PPC(os.getenv('Model_SEM_PPC_Analyst'))
            handler.update_success("SEM/PPC Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"SEM/PPC Analysis failed: {str(e)}")
            return None
        
    def run_marketplace_analysis():
        handler = handlers["marketplace"]
        try:
            handler.update_info("Running Marketplace Analysis...")
            result = Marketplace(os.getenv('Model_Marketplace_Analyst'))
            handler.update_success("Marketplace Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"Marketplace Analysis failed: {str(e)}")
            return None
    
    def run_target_market_analysis():
        handler = handlers["target_market"]
        try:
            handler.update_info("Running Target Market Analysis...")
            result = TargetMarket(os.getenv('Model_Target_Market_Analyst'))
            handler.update_success("Target Market Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"Target Market Analysis failed: {str(e)}")
            return None
        
    def run_df_overview_analysis():
        handler = handlers["df_overview"]
        try:
            handler.update_info("Running DF Overview Analysis...")
            result = dfOverview(os.getenv('Model_DF_Overview_Analyst'))
            handler.update_success("DF Overview Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"DF Overview Analysis failed: {str(e)}")
            return None
    
    def run_desired_outcomes_analysis():
        handler = handlers["desired_outcome"]
        try:
            handler.update_info("Running Desired Outcomes Analysis...")
            result = DesiredOutcome(os.getenv('Model_Desired_Outcomes_DM_Analyst'))
            handler.update_success("Desired Outcomes Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"Desired Outcomes Analysis failed: {str(e)}")
            return None
    
    def run_conversion_analysis():
        handler = handlers["conversion"]
        try:
            handler.update_info("Running Conversion Analysis...")
            result = ConversionAnalyst(os.getenv('Model_Conversion_Analyst'))
            handler.update_success("Conversion Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"Conversion Analysis failed: {str(e)}")
            return None
            
    def run_website_audience():
        handler = handlers["website_audience"]
        try:
            handler.update_info("Running Website Audience Acquisition Analysis...")
            result = WebsiteAudienceAcquisition(os.getenv('Model_Website_Audience_Acquisition_Analyst'))
            handler.update_success("Website Audience Acquisition Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"Website Audience Acquisition Analysis failed: {str(e)}")
            return None
        
    def run_content_process_and_assets_analysis():
        handler = handlers["content_process_and_assets"]
        try:
            handler.update_info("Running Content - Process and Assets Analysis...")
            result = Content_Process_and_Assets_Analyst(os.getenv('Model_Content_Process_and_Assets_Analyst'))
            handler.update_success("Content - Process and Assets Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"Content - Process and Assets Analysis failed: {str(e)}")
            return None

    def run_connection_analysis():
        handler = handlers["connection"]
        try:
            handler.update_info("Connection Analysis...")
            result = ConnectionAnalyst(os.getenv('Model_Connection_Analyst'))
            handler.update_success("Connection Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"Connection Analysis failed: {str(e)}")
            return None

    def run_snapshot_analysis():
        handler = handlers["snapshot"]
        try:
            handler.update_info("Running Snapshot by Channel Analysis...")
            result = Snapshot(os.getenv('Model_Snapshot_by_Channel_Analyst'))
            handler.update_success("Snapshot by Channel Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"Snapshot by Channel Analysis failed: {str(e)}")
            return None
    
    def run_executive_summary_analysis():
        handler = handlers["executive_summary"]
        try:
            handler.update_info("Running Executive Summary Analysis...")
            result = ExecutiveSummary(os.getenv('Model_Executive_Summary_Analyst'))
            handler.update_success("Executive Summary Analysis completed successfully.")
            return result
        except Exception as e:
            handler.update_error(f"Executive Summary Analysis failed: {str(e)}")
            return None

    # Define first batch of analyses
    threads_first_batch = [
        (run_off_page_analysis, "off_page"),
        (run_on_page_analysis, "on_page"),
        (run_website_and_tools_analysis, "website_tools"),
        (run_seo_analysis, "seo"),
        (run_social_media_analysis, "social_media"),
        (run_lld_pm_ln, "lld_pm_ln"),
        (run_pull_through_offers, "pull_through"),
        (run_content, "content"),
        (run_sem_ppc_analysis, "sem_ppc"),
        #(run_marketplace_analysis, "marketplace"),
        (run_target_market_analysis, "target_market"),
        (run_df_overview_analysis, "df_overview"),
        (run_desired_outcomes_analysis, "desired_outcome"),
        (run_content_process_and_assets_analysis, "content_process_and_assets"),
        (run_conversion_analysis, "conversion"),
        (run_website_audience, "website_audience"),
        (run_connection_analysis, "connection")
    ]
    
    # Create and start first batch threads with small delays to prevent UI conflicts
    thread_objects_first_batch = []
    for i, (func, name) in enumerate(threads_first_batch):
        # Add a small stagger to thread start times to reduce conflicts
        time.sleep(0.1)
        thread = threading.Thread(target=func, name=name)
        add_script_run_ctx(thread)  # Attach Streamlit context
        thread_objects_first_batch.append(thread)
        thread.start()
    
    # Wait for all first batch threads to complete
    for thread in thread_objects_first_batch:
        thread.join()
    
    # Add a separator
    try:
        st.markdown("---")
    except Exception:
        pass
    
    # Wait a bit to let UI stabilize before starting second batch
    time.sleep(0.5)
    
    # Create threads for second batch (snapshot and executive summary)
    threads_second_batch = [
        (run_snapshot_analysis, "snapshot"),
        (run_executive_summary_analysis, "executive_summary")
    ]
    
    # Create and start second batch threads
    thread_objects_second_batch = []
    for i, (func, name) in enumerate(threads_second_batch):
        # Add a small stagger between threads
        time.sleep(0.2)
        thread = threading.Thread(target=func, name=name)
        add_script_run_ctx(thread)  # Attach Streamlit context
        thread_objects_second_batch.append(thread)
        thread.start()
    
    # Wait for second batch threads to complete
    for thread in thread_objects_second_batch:
        thread.join()
    
    # Set analysis_completed to True when all analyses are done
    st.session_state.analysis_completed = True
    try:
        st.success("🎉 All analyses completed!")
    except Exception:
        pass

# Navigation button
if st.button("Back"):
    st.switch_page("pages/home.py")

# Main logic
if not st.session_state.analysis_completed:
    run_analysis()
else:
    st.info("Analysis has already been completed.")

# View Results button (only displayed after analysis is completed)
if st.session_state.analysis_completed and st.button("View Results", icon="📃"):
    st.switch_page("pages/output.py")
    st.session_state.analysis_completed = False