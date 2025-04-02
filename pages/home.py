import os
import streamlit as st
st.set_page_config(layout="wide")
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


# Create a dashboard that will display various agents on the page 
st.write("# Digital Footprint AI Team")
if 'nature' not in st.session_state:
    st.session_state['nature'] = ''
if 'analyze' not in st.session_state:
            st.session_state['analyze'] = False
        
def row1():
    col1, col2, col3, col4 = st.columns(4, border=True, gap="medium", vertical_alignment="top")
    with col1:
        txt = st.text_area(
                "Client Summary:",
                f"{st.session_state.nature}",help="Name of business, nature of business, location, products/services" 
            )
        st.session_state.nature = txt
        if 'analyze' not in st.session_state:
            st.session_state['analyze'] = False

        analyze_button = st.button("Analyze", st.session_state['analyze'])
        if analyze_button:
            st.session_state['analyze'] = 'clicked'
        
    with col2:
        st.write("## Website Traffic")
        backlinks = SeoOffPageAnalyst(os.getenv('MODEL_Off_Page_Analyst'))
        #backlinks = SeoBacklinks(os.getenv('MODEL_SEO_Analyst'))
        keywords = Seo(os.getenv('MODEL_SEO_Analyst'))    

    with col3:
        st.write("## Social Media")
        st.write("### Facebook")
        facebook = Facebook(os.getenv('MODEL_Social_Media_Analyst'))

        st.write('### Instagram')
        instagram = Instagram(os.getenv('MODEL_Social_Media_Analyst'))

        st.write('### Twitter')
        twitter = Twitter(os.getenv('MODEL_Social_Media_Analyst'))

        st.write('### YouTube')
        youtube = YouTube(os.getenv('MODEL_Social_Media_Analyst'))

        st.write('### Linkedin')
        linkedin = Linkedin(os.getenv('MODEL_Social_Media_Analyst'))

        st.write('### Tiktok')
        tiktok = Tiktok(os.getenv('MODEL_Social_Media_Analyst'))

    with col4:
        st.write("## Website Structure")
        crawl = SeoOnCrawl(os.getenv('MODEL_On_Page_Analyst'))
        gtmetrix = SeoOnGT(os.getenv('MODEL_On_Page_Analyst'))
       

    return col1, col2, col3, col4

row1()

