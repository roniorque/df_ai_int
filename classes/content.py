import streamlit as st
import requests
from dotenv import load_dotenv
import os
import time
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button, unhide_button
from helper.initialize_analyze_session import initialize_analyze_session
import pandas as pd

class Content:
    def __init__(self, model_url):
        self.uploaded_files = []
        self.file_dict = {}
        self.file_gt = {}
        self.model_url = model_url
        #self.analyst_name = analyst_name
        #self.data_src = data_src
        #self.analyst_description = analyst_description
        self.initialize()
        
        self.row1()

    def initialize(self):
        # FOR ENV
        load_dotenv()

        if 'content_in_the_website' not in st.session_state:
            st.session_state['content_in_the_website'] = ''
        if 'content_outside_the_website' not in st.session_state:
            st.session_state['content_outside_the_website'] = ''
    
    def process(self):
                session = st.session_state.analyze

                if (self.content_in_the_website or self.content_outside_the_website) and session == 'clicked':
                    with st.spinner('Uploading Contents...', show_time=True):
                        st.write('')
                        content_in_the_website = ""
                        content_outside_the_website = ""
                        try:
                            content_in_the_website += f"\nContent in the Website: {self.content_in_the_website}"
                        except KeyError:
                            pass
                        try:
                            content_outside_the_website += f"\nContent outside the Website: {self.content_outside_the_website}"
                        except KeyError:
                            pass

                        debug_info_content_in_the_website = {'data_field' : 'Content in the Website', 'result': content_in_the_website}
                        debug_info_content_outside_the_website = {'data_field' : 'Content outside the Website', 'result': content_outside_the_website}

                        if self.content_in_the_website:
                            if self.content_in_the_website != self.template_content_in_the_website:
                                st.session_state['content_in_the_website'] = 'uploaded'
                                collect_telemetry(debug_info_content_in_the_website)
                            else:
                                 pass
                        if self.content_outside_the_website:
                            if self.content_outside_the_website != self.template_content_outside_the_website:
                                st.session_state['content_outside_the_website'] = 'uploaded'
                                collect_telemetry(debug_info_content_outside_the_website)
                            else:
                                pass
                    
                        #with st.expander("Debug information", icon="⚙"):
                        #    st.write(debug_info)


                        st.session_state['analyzing'] = False
                        try:
                            self.file_dict.popitem()
                        except KeyError:
                            pass
                        
    def row1(self):
            self.template_content_in_the_website = ("Content and Messaging:\n"
                                                    "a. Is the text easy to read and understand?\n"
                                                    "b. Does it clearly explain what the business offers?\n"
                                                    "c. Are the brand’s Unique Selling Propositions (USPs) clearly emphasized?\n"
                                                    "d. Other Remarks:\n\n"
                                                    
                                                    "Call-to-Action (CTAs):\n"
                                                    "a. Are CTAs prominently placed and easy to find?\n"
                                                    "b. Are the CTAs strong and action-focused?\n"
                                                    "c. Do they appear in the right places?\n"
                                                    "d. Other Remarks:\n\n"
                                                    
                                                    "Images and Videos:\n"
                                                    "a. Are the images and videos high quality?\n"
                                                    "b. Do they clearly show the product or service?\n"
                                                    "c. Are the videos easy to watch (no unnecessary clicks or extra steps)?\n"
                                                    "d. Are the visuals engaging upon first glance?\n"
                                                    "e. Other Remarks:\n\n"
                                                    
                                                    "Blog and SEO:\n"
                                                    "a. Does the site have a blog section?\n"
                                                    "b. Is the blog updated regularly?\n"
                                                    "c. Are the articles helpful, relevant, and informative?\n"
                                                    "d. Are internal links used to guide users to related or deeper content?\n"
                                                    "e. Other Remarks:\n\n"
                                                    
                                                    "User Experience (UX) and Navigation:\n"
                                                    "a. Is the site easy to navigate with clear menus and categories?\n"
                                                    "b. Can users quickly find important information?\n"
                                                    "c. Are any interactions creating unnecessary friction (e.g., signups to view content)?\n"
                                                    "d. Other Remarks:\n\n"
                                                    
                                                    "Product or Services (For E-Commerce):\n"
                                                    "a. Does the site clearly explain the company’s products or services?\n"
                                                    "b. Are product or service details clear?\n"
                                                    "c. Are there enough pictures or videos?\n"
                                                    "d. Is there a sense of urgency or promotions to encourage action?\n"
                                                    "e. Other Remarks:")
            self.template_content_outside_the_website = ("Backlinks and Referring Domains:\n"
                                                            "a. Are there backlinks from relevant and authoritative websites?\n"
                                                            "b. Do the referring sites belong to the same industry or niche?\n"
                                                            "c. Are there spammy or low-quality backlinks (e.g., thin directories)?\n"
                                                            "d. Are the backlinks helpful and align with Google’s Helpful Content guidelines?\n"
                                                            "e. Are there any guest posts or articles on other websites?\n"
                                                            "f. Other Remarks:\n\n"
                                                            
                                                            "Community Engagement (Forums and Platforms):\n"
                                                            "a. Is the brand/product/company mentioned in online forums (e.g., Reddit, or Quora)?\n"
                                                            "b. Are the mentions from forums and platforms generally positive?\n"
                                                            "c. Are the mentions from forums and platforms generally negative?\n"
                                                            "d. Is it actively participating or present in these communities?\n"
                                                            "e. Is there a strategy for using personas or ambassadors to represent the client’s company/brand/product?\n"
                                                            "f. Other Remarks:\n\n"
                                                            
                                                            "Online Reviews and Reputation Management:\n"
                                                            "a. Are there recent reviews on platforms like Google, Trustpilot, or Yelp?\n"
                                                            "b. Are the reviews mostly positive?\n"
                                                            "c. Are the reviews mostly negative?\n"
                                                            "d. Is the client responding to reviews, especially complaints or fake ones?\n"
                                                            "e. Do the reviews mention recurring issues (e.g., poor support, unsolicited emails)?\n"
                                                            "f. Other Remarks:\n\n"
                                                            
                                                            "Public Relations and Media Coverage:\n"
                                                            "a. Has the client’s company been featured in news sites or magazines?\n"
                                                            "b. Are the articles helpful and recent?\n"
                                                            "c. Are PR opportunities being used to boost awareness?\n"
                                                            "d. Other Remarks:\n\n"
                                                            
                                                            "Branded Blog Networks:\n"
                                                            "a. Are there any off-page blog sites created by the client’s company?\n"
                                                            "b. Is the content unique, helpful, and adding SEO value?\n"
                                                            "c. Can the content be moved or consolidated into the main site?\n"
                                                            "d. Other Remarks:\n\n"
                                                            
                                                            "Email Marketing & CRM Engagement:\n"
                                                            "a. Is email being used to follow up with customers or leads (e.g., newsletters, cart recovery)?\n"
                                                            "b. Are they sending follow-up emails?\n"
                                                            "c. Are emails building relationships and promoting content or reviews?\n"
                                                            "d. Other Remarks:")
            
            self.content_in_the_website = st.text_area("Content in the Website:", 
                                                       value=self.template_content_in_the_website,
                                                        height=600)
            self.content_outside_the_website = st.text_area("Content outside the Website:", 
                                                            value=self.template_content_outside_the_website,
                                                            height=600)

            self.process()

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()