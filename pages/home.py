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

# Check login session
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.switch_page('app.py')
    st.stop()

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
        if 'run_all' not in st.session_state:
            st.session_state['run_all'] = False
        if 'is_competitor' not in st.session_state:
            st.session_state['is_competitor'] = False
        if 'competitor_name' not in st.session_state:
            st.session_state['competitor_name'] = False

    async def create_row1(self):
        """Create the first row with four columns"""
        # Add custom CSS for scrollable expanders
        st.markdown(
            """
            <style>
            .scrollable-expander > div[role='region'] {
                max-height: 350px;s
                overflow-y: auto;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        col1, col2, col3, col4 = st.columns(4, border=True, gap="medium", vertical_alignment="top")
        
        with col1:
            is_competitor = st.checkbox("Competitor", value=False, help="Select to compare this entity against client data")
            st.session_state['is_competitor'] = is_competitor

            run_all = st.checkbox("Run all", value=False, help="Run all processes (longer time); file upload optional")
            st.session_state['run_all'] = run_all
            
            button_label = "Uploading..." if st.session_state['uploading'] else "Sync Data"
            if st.button(button_label, key="sync_button", icon="🔄", use_container_width=True):
                st.session_state['uploading'] = True
                st.session_state['analyze'] = 'clicked'
                
                st.session_state['uploading'] = False
            else:
                st.session_state["analyze"] = ''

            analyze_disabled = st.session_state.get('analyze') != 'clicked'
            if st.button("Analyze", key="analyze_button", icon="✨", use_container_width=True, disabled=analyze_disabled):
                st.session_state.analysis_completed = False
                st.switch_page("pages/analyzing_page.py")
            
            if st.button("Show Output", key="show_output_button", icon="📃", use_container_width=True):
                st.switch_page("pages/output.py")

            st.session_state.run_all = run_all
            
            # Show Client Summary directly (not in expander)
            self.client_summary = ClientSummary()
            
        with col2:
            st.write("## Website Traffic")
            with st.expander("Backlinks", expanded=False):
                st.markdown('<div class="scrollable-expander">', unsafe_allow_html=True)
                self.backlinks = SeoOffPageAnalyst(os.getenv('MODEL_Off_Page_Analyst'))
                st.markdown('</div>', unsafe_allow_html=True)
            with st.expander("Keywords", expanded=False):
                st.markdown('<div class="scrollable-expander">', unsafe_allow_html=True)
                self.keywords = Seo(os.getenv('MODEL_SEO_Analyst'))
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.write("## Social Media")
            with st.expander("Facebook", expanded=False):
                st.markdown('<div class="scrollable-expander">', unsafe_allow_html=True)
                st.write("### Facebook")
                self.facebook = Facebook(os.getenv('MODEL_Social_Media_Analyst'))
                st.markdown('</div>', unsafe_allow_html=True)
            with st.expander("Instagram", expanded=False):
                st.markdown('<div class="scrollable-expander">', unsafe_allow_html=True)
                st.write('### Instagram')
                self.instagram = Instagram(os.getenv('MODEL_Social_Media_Analyst'))
                st.markdown('</div>', unsafe_allow_html=True)
            with st.expander("Twitter", expanded=False):
                st.markdown('<div class="scrollable-expander">', unsafe_allow_html=True)
                st.write('### Twitter')
                self.twitter = Twitter(os.getenv('MODEL_Social_Media_Analyst'))
                st.markdown('</div>', unsafe_allow_html=True)
            with st.expander("YouTube", expanded=False):
                st.markdown('<div class="scrollable-expander">', unsafe_allow_html=True)
                st.write('### YouTube')
                self.youtube = YouTube(os.getenv('MODEL_Social_Media_Analyst'))
                st.markdown('</div>', unsafe_allow_html=True)
            with st.expander("LinkedIn", expanded=False):
                st.markdown('<div class="scrollable-expander">', unsafe_allow_html=True)
                st.write('### Linkedin')
                self.linkedin = Linkedin(os.getenv('MODEL_Social_Media_Analyst'))
                st.markdown('</div>', unsafe_allow_html=True)
            with st.expander("TikTok", expanded=False):
                st.markdown('<div class="scrollable-expander">', unsafe_allow_html=True)
                st.write('### Tiktok')
                self.tiktok = Tiktok(os.getenv('MODEL_Social_Media_Analyst'))
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.write("## Website Structure")
            with st.expander("On Page SEO", expanded=False):
                st.markdown('<div class="scrollable-expander">', unsafe_allow_html=True)
                self.on_page = SeoOn(os.getenv('MODEL_On_Page_Analyst'))
                st.markdown('</div>', unsafe_allow_html=True)
            with st.expander("Website and Tools", expanded=False):
                st.markdown('<div class="scrollable-expander">', unsafe_allow_html=True)
                self.website_and_tools = WebsiteAndTools(os.getenv('MODEL_On_Page_Analyst'))
                st.markdown('</div>', unsafe_allow_html=True)
            with st.expander("LLD PM LN", expanded=False):
                st.markdown('<div class="scrollable-expander">', unsafe_allow_html=True)
                self.lld_pm_ln = LLD_PM_LN(os.getenv('Model_LLD_PM_LN_ANALYST'))
                st.markdown('</div>', unsafe_allow_html=True)
            with st.expander("Pull Through Offers", expanded=False):
                st.markdown('<div class="scrollable-expander">', unsafe_allow_html=True)
                self.pull_through_offers = PullThroughOffers(os.getenv('Model_Pull_Through_Offers_Analyst'))
                st.markdown('</div>', unsafe_allow_html=True)
        return col1, col2, col3, col4

    async def create_row2(self):
        """Create the first row with four columns"""
        col1, col4 = st.columns(2, border=True, gap="medium", vertical_alignment="top")
        
        with col1:
            st.write("## Ads")
            with st.expander("SEM/PPC"):
                self.sem_ppc = Sem_PPC(os.getenv('Model_SEM_PPC_Analyst'))

        with col4:
            st.write("## Website Content")
            with st.expander("Content"):
                self.content = Content(os.getenv('Model_Content'))
        return col1, col4
    
    async def delete_button(self):
        # Add a warning confirmation before resetting all
        if 'confirm_reset' not in st.session_state:
            st.session_state['confirm_reset'] = False
        if 'db_wiped' not in st.session_state:
            st.session_state['db_wiped'] = False

        # Use key for the reset button to avoid rerun issues
        reset_clicked = st.button("RESET ALL", icon="🗑️", use_container_width=True, key="reset_all_btn")
        if reset_clicked:
            st.session_state['confirm_reset'] = True
            st.session_state['db_wiped'] = False

        if st.session_state['db_wiped']:
            st.markdown("""
                <div style='display: flex; flex-direction: column; align-items: center;'>
                    <div style='width: 100%; text-align: center;'>
                        <span style='color: #008000; font-weight: 600; font-size: 1.1rem;'>✅ Database wiped out.</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.session_state['confirm_reset'] = False
        elif st.session_state['confirm_reset']:
            st.markdown("""
                <div style='display: flex; flex-direction: column; align-items: center;'>
                    <div style='width: 100%; text-align: center;'>
                        <span style='color: #b30000; font-weight: 600; font-size: 1.1rem;'>⚠️ Are you sure you want to reset all? This will wipe out the database and cannot be undone.</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height: 1.5em;'></div>", unsafe_allow_html=True)
            col_spacer1, col_buttons, col_spacer2 = st.columns([4.4,2,4])
            with col_spacer1:
                st.write("")
            with col_buttons:
                col_cancel, col_confirm = st.columns([2,2], gap="small")
                with col_cancel:
                    if st.button("Cancel", key="cancel_wipe"):
                        st.session_state['confirm_reset'] = False
                with col_confirm:
                    if st.button("Yes, wipe database", key="confirm_wipe", type="primary"):
                        # Run clear_collection in parallel for speed
                        import threading
                        t1 = threading.Thread(target=clear_collection, args=("df_data",))
                        t2 = threading.Thread(target=clear_collection, args=("df_response",))
                        t1.start()
                        t2.start()
                        t1.join()
                        t2.join()
                        st.session_state['confirm_reset'] = False
                        st.session_state['db_wiped'] = True
            with col_spacer2:
                st.write("")

    async def main(self):
        """Main method to run the dashboard"""
        await self.create_row1()
        await self.create_row2()
        await self.delete_button()

# Main execution
if __name__ == "__main__":
    dashboard = DigitalFootprintDashboard()
    asyncio.run(dashboard.main())