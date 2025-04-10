import os
import streamlit as st
from classes.Off_Page import SeoOffPageAnalyst
from classes.On_Page_GT import SeoOnGT
from classes.On_Page_Crawl import SeoOnCrawl
from classes.Seo_Backlinks import SeoBacklinks
from classes.Seo import Seo
from classes.Social_Media_FB import Facebook
from classes.Social_Media_IG import Instagram
from classes.Twitter import Twitter
from classes.Youtube import YouTube
from classes.Linkedin import Linkedin
from classes.Tiktok import Tiktok
import asyncio
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
        if 'seo' not in st.session_state:
            st.session_state['seo'] = ''
        if 'twitter' not in st.session_state:
            st.session_state['twitter'] = ''
    
    async def create_row1(self):
        """Create the first row with four columns"""
        col1, col2, col3, col4 = st.columns(4, border=True, gap="medium", vertical_alignment="top")
        
        with col1:
            txt = st.text_area(
                "Client Summary:",
                f"{st.session_state.nature}",
                help="Name of business, nature of business, location, products/services" 
            )
            st.session_state.nature = txt

            analyze_button = st.button("Analyze", st.session_state['analyze'])
            if analyze_button == True:
                st.session_state["analyze"] = 'clicked'
                st.session_state['seo'] = 'clicked'
                st.session_state['twitter'] = 'clicked'
            else:
                st.session_state["analyze"] = ''
                st.session_state['seo'] = ''
                st.session_state['twitter'] = ''
            
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

            st.write('### YouTube')
            self.youtube = YouTube(os.getenv('MODEL_Social_Media_Analyst'))
            
            st.write('### Linkedin')
            self.linkedin = Linkedin(os.getenv('MODEL_Social_Media_Analyst'))

            st.write('### Tiktok')
            self.tiktok = Tiktok(os.getenv('MODEL_Social_Media_Analyst'))

        with col4:
            st.write("## Website Structure")
            self.crawl = SeoOnCrawl(os.getenv('MODEL_On_Page_Analyst'))
            self.gtmetrix = SeoOnGT(os.getenv('MODEL_On_Page_Analyst'))

        return col1, col2, col3, col4

    async def run_analysis(self):
        result = await asyncio.gather(
            self.gtmetrix.process(), 
            self.backlinks.process(), 
            self.keywords.process(), 
            self.facebook.process(), 
            self.instagram.process(), 
            self.twitter.process(), 
            self.youtube.process(), 
            self.linkedin.process(), 
            self.tiktok.process(), 
            self.crawl.process()
        )
        st.session_state.analyze = False

    async def main(self):
        """Main method to run the dashboard"""
        await self.create_row1()
        await self.run_analysis()

# Main execution
if __name__ == "__main__":
    dashboard = DigitalFootprintDashboard()
    asyncio.run(dashboard.main())