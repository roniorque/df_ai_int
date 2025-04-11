import os
import streamlit as st

import time

def display_outputs():
    client_name = "RMX Creatives"
    overview = f"""**{client_name}** is a financial services company based in Auckland, New Zealand, specializing in providing quick and flexible loan solutions for businesses and individuals. Represented by Paul Stone, LoansOne has enlisted ShoreMarketing to perform a deep dive into their digital footprint to have a view of the holistic status of their digital properties and determine how each property can play part in implementing a stronger digital marketing plan.\n
The Digital Marketing Footprint consists of deep-dive research by ShoreMarketing specialists to help the business leaders of LoansOne understand the effectiveness of their existing digital initiatives with the view of giving them an insight to developing a strategy and effectively allocating business resources to digital properties that will give them the best results.\n
This document represents the results of our audit of LoansOne’s digital marketing and management practices. Our audit covered reviews of key digital areas: Website and Tools, PPC/SEM, SEO, Social Media, and Market Places."""

    # (off_page_thread)
    # (on_page_thread)
    # (website_and_tools_thread)
    # (seo_thread)
    # (social_media_thread)
    st.markdown("## Digital Marketing Audit")
    st.markdown(f"### {client_name}")
    
    st.markdown("## DIGITAL FOOTPRINT OVERVIEW")
    st.markdown(f"{overview}")
    
    st.markdown("## WEBSITE AND TOOLS")
    st.markdown(f"""In today’s digital age, scaling a business is simply impossible without a website. Websites primarily serve as the center for all online conversions, which makes it equally important to guarantee that all pages are optimised to educate all traffic about the brand and ultimately to usher them into conversion. \n
In line with this, we have looked into the technology used by **{client_name}** as well as the different digital channels currently in place to see how they are structured and how they are performing.""")
    

if st.button("Back to Dashboard"):
        st.switch_page("pages/home.py")
display_outputs()