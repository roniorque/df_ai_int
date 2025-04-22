import os
import streamlit as st
from classes.Off_Page import SeoOffPageAnalyst
from classes.On_Page import SeoOn
from classes.Seo import Seo
from classes.Social_Media_FB import Facebook
from classes.Social_Media_IG import Instagram
from classes.Twitter import Twitter
from classes.Youtube import YouTube
from classes.Linkedin import Linkedin
from classes.Tiktok import Tiktok
from classes.website_and_tools import WebsiteAndTools
from classes.client_summary import ClientSummary
from classes.pull_through_offers import PullThroughOffers
from classes.lld_pm_ln import LLD_PM_LN
from classes.content import Content
from classes.sem_ppc import Sem_PPC
from classes.amazon import Amazon
from classes.ebay import eBay
import asyncio
from helper.upload_button import hide_button, unhide_button
from helper.telemetry import clear_collection
import time

class DigitalFootprintDashboard:
    def __init__(self):
        # Set page configuration
        st.set_page_config(layout="wide")
        
        # Initialize session state variables
        self._init_session_state()
        
        # Create dashboard title
        st.write("# Digital Footprint AI Team")
    
    def _init_session_state(self):
        """Initialize session state variables if they don't exist"""
        if 'nature' not in st.session_state:
            st.session_state['nature'] = ''
        if 'analyze' not in st.session_state:
            st.session_state['analyze'] = ''
        if 'analysis_completed' not in st.session_state:
            st.session_state.analysis_completed = False
        if 'uploading' not in st.session_state:
            st.session_state['uploading'] = False

    async def create_row1(self):
        """Create the first row with four columns"""
        col1, col2, col3, col4, col5 = st.columns(5, border=True, gap="medium", vertical_alignment="top")
        
        with col1:
            button_label = "Uploading..." if st.session_state['uploading'] else "Sync Data"
            if st.button(button_label, key="sync_button", icon="🔄", use_container_width=True):
                st.session_state['uploading'] = True
                st.session_state['analyze'] = 'clicked'
                
                st.session_state['uploading'] = False
            else:
                st.session_state["analyze"] = ''

            #self.upload_file_button = st.button("Sync Data", st.session_state['analyze'], icon="🔄", use_container_width=True)
            
            #if self.upload_file_button == True:
            #    st.session_state["analyze"] = 'clicked'
                #unhide_button()
            #else:
            #    st.session_state["analyze"] = ''
            
            analyze_disabled = st.session_state.get('analyze') != 'clicked'
            if st.button("Analyze", key="analyze_button", icon="✨", use_container_width=True, disabled=analyze_disabled):
                st.session_state.analysis_completed = False
                st.switch_page("pages/analyzing_page.py")
            
            
            self.client_summary = ClientSummary()
            
        with col2:
            st.write("## Website Traffic")
            self.backlinks = SeoOffPageAnalyst(os.getenv('MODEL_Off_Page_Analyst'))
            self.keywords = Seo(os.getenv('MODEL_SEO_Analyst'))    

        with col3:
            st.write("## Social Media")
            st.write("### Facebook")
            self.facebook = Facebook(os.getenv('MODEL_Social_Media_Analyst'))

            st.write('### Instagram')
            self.instagram = Instagram(os.getenv('MODEL_Social_Media_Analyst'))

            st.write('### Twitter')
            self.twitter = Twitter(os.getenv('MODEL_Social_Media_Analyst'))

            
        with col4:
            st.write("## Social Media")
            st.write('### YouTube')
            self.youtube = YouTube(os.getenv('MODEL_Social_Media_Analyst'))
            
            st.write('### Linkedin')
            self.linkedin = Linkedin(os.getenv('MODEL_Social_Media_Analyst'))

            st.write('### Tiktok')
            self.tiktok = Tiktok(os.getenv('MODEL_Social_Media_Analyst'))
        
        with col5:
            st.write("## Website Structure")
            #self.crawl = SeoOnCrawl(os.getenv('MODEL_On_Page_Analyst'))
            self.on_page = SeoOn(os.getenv('MODEL_On_Page_Analyst'))
            self.website_and_tools = WebsiteAndTools(os.getenv('MODEL_On_Page_Analyst'))
            self.lld_pm_ln = LLD_PM_LN(os.getenv('Model_LLD_PM_LN_ANALYST'))
            self.pull_through_offers = PullThroughOffers(os.getenv('Model_Pull_Through_Offers_Analyst'))

        return col1, col2, col3, col4, col5

    async def create_row2(self):
        """Create the first row with four columns"""
        col1, col4 = st.columns(2, border=True, gap="medium", vertical_alignment="top")
        # col1, col2, col3, col4 = st.columns(4, border=True, gap="medium", vertical_alignment="top")
        
        with col1:
            st.write("## Ads")
            self.sem_ppc = Sem_PPC(os.getenv('Model_SEM_PPC_Analyst'))
        # with col2:
        #     st.write("## Amazon")
        #     self.amazon = Amazon(os.getenv('Model_SEM_PPC_Analyst'))
        # with col3:
        #     st.write("## eBay")
        #     self.ebay = eBay(os.getenv('Model_SEM_PPC_Analyst'))
        with col4:
            st.write("## Website Content")
            self.content = Content(os.getenv('Model_Content'))
        return col1, col4
    
    async def delete_button(self):
        reset_button = st.button("RESET ALL",icon="🗑️", use_container_width=True)

        if reset_button:
    # Use session state to track the state of deletion process
            if 'delete_state' not in st.session_state:
                st.session_state.delete_state = 'confirmation'
            
            # Show confirmation dialog
            if st.session_state.delete_state == 'confirmation':
                st.warning("⚠️ Are you sure you want to delete all data? This action cannot be undone.")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Yes, delete data", key="confirm_btn"):
                        # Perform the deletion
                        clear_collection("df_data")
                        clear_collection("df_response")
                        st.session_state.delete_state = 'success'
                        st.rerun()  # Using st.rerun() instead of experimental_rerun
                with col2:
                    if st.button("Cancel", key="cancel_btn"):
                        st.session_state.delete_state = 'idle'
                        st.rerun()  # Using st.rerun() instead of experimental_rerun
            
            # Show success message
            elif st.session_state.delete_state == 'success':
                st.success("✅ Data deleted successfully!")
                # Reset state after showing success
                st.session_state.delete_state = 'idle'

    async def main(self):
        """Main method to run the dashboard"""
        await self.create_row1()
        await self.create_row2()
        await self.delete_button()
        #self.run_analysis()

# Main execution
if __name__ == "__main__":
    dashboard = DigitalFootprintDashboard()
    asyncio.run(dashboard.main())