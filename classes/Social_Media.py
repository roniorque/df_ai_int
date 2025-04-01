import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import time
import chardet
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button
from helper.initialize_analyze_session import initialize_analyze_session

class SocialMediaAnalyst:
    def __init__(self, model_url):
        self.file_dict = {}
        self.model_url = model_url
        #self.analyst_name = analyst_name
        #self.data_src = data_src
        #self.analyst_description = analyst_description
        self.initialize()
        self.row1()

    def initialize(self):
        # FOR ENV
        load_dotenv()
        '''
        # AGENT NAME
        st.header(self.analyst_name)

        # EVALUATION FORM LINK
        url = os.getenv('Link')
        st.write('Evaluation Form: [Link](%s)' % url)

        # RETURN BUTTON
        try:
            if st.button("Return", type='primary'):
                st.switch_page("./pages/home.py")
        except Exception:
            pass
        '''

    def request_model(self, payload_txt):
        response = requests.post(self.model_url, json=payload_txt)
        response.raise_for_status()
        output = response.json()
        
        categories = []
        current_footprint = []
        number_of_backlinks = []

        for key, value in output.items():
            if key == 'json':
                for item in value:
                    categories.append(item.get('category', 'N/A').replace('_', ' ').title())
                    current_footprint.append(item.get('current_footprint', 'N/A'))
                    number_of_backlinks.append(item.get('best_of_breed_solution', 'N/A'))    

        output = ""
        for i in range(len(categories)):
            output += f"\n\n---\n **Category:** {categories[i]}"
            output += f"\n\n **Count:** {current_footprint[i]}\n\n"
            output += f"**Best of Breed Solution:** {number_of_backlinks[i]}"

        data = {
            "": [str(category) for category in categories],
            "Current Footprint": [str(footprint) for footprint in current_footprint],
            "Best of Breed Solution": [str(backlink) for backlink in number_of_backlinks]
        }
        df_output = pd.DataFrame(data)
        with st.expander("AI Analysis", expanded=True, icon="🤖"):
            st.table(df_output.style.set_table_styles(
            [{'selector': 'th:first-child, td:first-child', 'props': [('width', '20px')]},
            {'selector': 'th, td', 'props': [('width', '150px'), ('text-align', 'center')]}]
            ).set_properties(**{'text-align': 'center'}))

        return output
      
    def detect_encoding(self, uploaded_file):
        result = chardet.detect(uploaded_file.read(100000))
        uploaded_file.seek(0)  # Reset file pointer to the beginning
        return result['encoding']

    def facebook_ad_campaign(self, facebook_ad_campaign):
        facebook_ads = facebook_ad_campaign[~facebook_ad_campaign['Ad name'].isna()].shape[0]
        st.session_state['facebook_ads'] = facebook_ads
        return facebook_ads
    
    def facebook_organic(self, facebook_organic_post):
        try:
            facebook_engagement_rate = (facebook_organic_post['Reactions, Comments and Shares'].mean() / self.facebooks).round(2)
            st.session_state['facebook_engagement_rate'] = facebook_engagement_rate
        except TypeError:
            pass
        # Post Frequency
        facebook_post_frequency = facebook_organic_post[~facebook_organic_post['Post ID'].isna()].shape[0]
        st.session_state['facebook_post_frequency'] = facebook_post_frequency
        st.session_state['facebook_review_rate'] = self.facebook_rr
        st.session_state['facebook_followers'] = self.facebooks
        
        try:
            return facebook_post_frequency, facebook_engagement_rate 
        except UnboundLocalError:
            return facebook_post_frequency

    def linkedin_content_metrics(self, linkedin_content_metrics):
        # Avg. engagement rate
        try:
            linkedin_engagement_rate = linkedin_content_metrics['Engagement rate (organic)'].mean().round(2)
        except Exception:
            new_header = linkedin_content_metrics.iloc[0] #grab the first row for the header
            linkedin_content_metrics = linkedin_content_metrics[1:] #take the data less the header row
            linkedin_content_metrics.columns = new_header #set the header row as the df header
            linkedin_content_metrics['Engagement rate (organic)'] = pd.to_numeric(linkedin_content_metrics['Engagement rate (organic)'], errors='coerce')
            linkedin_engagement_rate = linkedin_content_metrics['Engagement rate (organic)'].mean().round(2)
        # Post Frequency
        
        st.session_state['linkedin_engagement_rate'] = linkedin_engagement_rate
        
        return linkedin_engagement_rate
    
    def linkedin_content_post(self, linkedin_content_post):
        try:
            linkedin_post_frequency = linkedin_content_post[~linkedin_content_post['Post title'].isna()].shape[0]
        except Exception:
            new_header = linkedin_content_post.iloc[0]
            linkedin_content_post = linkedin_content_post[1:]
            linkedin_content_post.columns = new_header
            linkedin_post_frequency = linkedin_content_post[~linkedin_content_post['Post title'].isna()].shape[0]
            st.write(linkedin_content_post)
            
        st.session_state['linkedin_post_frequency'] = linkedin_post_frequency
        return linkedin_post_frequency

    def terminate_session(self, session):
        try:
            del st.session_state[session]
        except KeyError:
            pass

    def file_upload(self, file_name, file_desc, session):
        st.write("") # FOR THE HIDE BUTTON
        file_name = st.file_uploader(f"{file_desc}", type='csv')
        if file_name:
                try:
                    self.terminate_session(session)
                except UnboundLocalError:
                    pass
                try:
                    encoding = self.detect_encoding(file_name)
                    st.session_state[f'{session}'] = pd.read_csv(file_name, encoding=encoding, low_memory=False)
                except Exception:
                    pass
                return file_name
        
    def row1(self):
        
     
            self.facebooks = st.number_input('Facebook Followers:', min_value=1, max_value=99999999, value=None, step=1, placeholder='Enter Facebook Followers')
            self.facebook_rr = st.text_input("Facebook Review Rate:", placeholder='Enter Facebook Review Rate')
            
            self.instagram = st.text_input("Instagram Followers:", placeholder='Enter Instagram Followers')
            self.instagram_er = st.text_input("Instagram Audience Engagement Rate:", placeholder='Enter Instagram Audience Engagement Rate')
            self.instagram_pf = st.text_input("Instagram Post Frequency:", placeholder='Enter Instagram Post Frequency')
            
            self.twitter = st.text_input("Twitter Followers:", placeholder='Enter Twitter Followers')
            self.twitter_er = st.text_input("Twitter Audience Engagement Rate:", placeholder='Enter Twitter Audience Engagement Rate')
            self.twitter_pf = st.text_input("Twitter Post Frequency:", placeholder='Twitter Post Frequency')
            
            self.youtube = st.text_input("Youtube Followers:", placeholder='Enter Youtube Followers')
            self.youtube_er = st.text_input("Youtube Audience Engagement Rate:", placeholder='Enter Youtube Audience Engagement Rate')
            self.youtube_pf = st.text_input("Youtube Post Frequency:", placeholder='Youtube Post Frequency')

            self.linkedin_f = st.text_input("Linkedin Followers:", placeholder='Enter Linkedin Followers')
            
            self.tiktok_f = st.text_input("Tiktok Followers:", placeholder='Enter Tiktok Followers')
            self.tiktok_er = st.text_input("Tiktok Audience Engagement Rate:", placeholder='Enter Tiktok Audience Engagement Rate')
            self.tiktok_pf = st.text_input("Tiktok Post Frequency:", placeholder='Enter Tiktok Post Frequency')

            followers = {
                'Facebook Followers': self.facebooks if self.facebooks else 'N/A',
                'Facebook Review Rate': self.facebook_rr if self.facebook_rr else 'N/A',
                'Instagram Followers': self.instagram if self.instagram else 'N/A',
                'Twitter Followers': self.twitter if self.twitter else 'N/A',
                'Youtube Followers': self.youtube if self.youtube else 'N/A',
                'Linkedin Followers': self.linkedin_f if self.linkedin_f else 'N/A',
                'Tiktok Followers': self.tiktok_f if self.tiktok_f else 'N/A'
            }

            fb_organic_post = self.file_upload("fb_post", "Upload Facebook Organic Post CSV", "facebook_organic_post")
            fb_ads_campaign = self.file_upload("fb_campaign", "Upload Facebook Ads Campaign CSV", "facebook_ad_campaign")
            linkedin_metrics = self.file_upload("linkedin_content_metrics", "Upload Linkedin Content Metrics CSV", "linkedin_content_metrics")
            linkedin_post = self.file_upload("linkedin_content_post", "Upload Linkedin Content Post CSV", "linkedin_content_post") 
            tiktok_post = self.file_upload("Tiktok", "Upload Tiktok Content post", "Tiktok")
            
            fb_organic_post
            fb_ads_campaign
            linkedin_metrics
            linkedin_post
            tiktok_post
           
  
            st.write("") # FOR THE HIDE BUTTON
            st.write("") # FOR THE HIDE BUTTON
            st.write("AI Analyst Output: ")
            st.session_state['analyzing'] = False
            st.write("") # FOR THE HIDE BUTTON
            #analyze_button = st.button("Analyze", disabled=initialize_analyze_session())
            start_time = time.time()
            if st.session_state['analyze'] == 'clicked':
                hide_button()
                try:
                    if (fb_organic_post and fb_organic_post.name) or (fb_ads_campaign and fb_ads_campaign.name) or (linkedin_metrics and linkedin_metrics.name) or (linkedin_post and linkedin_post.name) or (tiktok_post and tiktok_post.name):
                        combined_text = ""
                        with st.spinner('Analyzing...', show_time=True):
                            st.write('')
                            # INITIALIZING SESSIONS
                            combined_text += f"Client Summary: {st.session_state.nature}\n"
                            try: # FACEBOOK
                                try: # ORGANIC POST
                                    combined_text += f"\nFacebook Followers: {self.facebooks}"
                                    facebook_organic_post = st.session_state['facebook_organic_post']
                                    self.facebook_organic(facebook_organic_post)
                                    facebook_post_frequency = st.session_state['facebook_post_frequency']
                                    combined_text += f"\nFacebook Post Frequency: {facebook_post_frequency}"
                                    try: # ENGAGEMENT RATE TRY CATCH
                                        facebook_engagement_rate = st.session_state['facebook_engagement_rate']
                                        combined_text += f"\nFacebook Audience Engagement Rate: {facebook_engagement_rate}%"
                                    except KeyError:
                                        pass
                
                                except KeyError:
                                    pass
                                try: # AD CAMPAIGN
                                    combined_text += f"\nFacebook Review Rate: {self.facebook_rr}"
                                    facebook_ad_campaign = st.session_state['facebook_ad_campaign']
                                    self.facebook_ad_campaign(facebook_ad_campaign)
                                    facebook_ads = st.session_state['facebook_ads']
                                    combined_text += f"\nFacebook Ads: {facebook_ads}"
                                except KeyError:
                                    pass
                                try: # FACEBOOK ORGANIC POST CSV
                                    combined_text += f"\nFacebook Organic Post CSV: {facebook_organic_post.to_csv(index=True)}"
                                except UnboundLocalError:
                                    pass
                                try: # FACEBOOK ADS CAMPAIGN CSV
                                    combined_text += f"\nFacebook Ads Campaign CSV: {facebook_ad_campaign.to_csv(index=True)}"
                                except UnboundLocalError:
                                    pass
                            except KeyError:
                                pass

                            try: # LINKEDIN
                                try: # LINKEDIN CONTENT POST
                                    combined_text += f"\nLinkedin Followers: {self.linkedin_f}"
                                    linkedin_content_post = st.session_state['linkedin_content_post'] 
                                    self.linkedin_content_post(linkedin_content_post)
                                    linkedin_post_frequency = st.session_state['linkedin_post_frequency']
                                    combined_text += f"\nLinkedin Post Frequency: {linkedin_post_frequency}"
                                except KeyError:
                                    pass
                                try: # LINKEDIN CONTENT METRICS
                                    linkedin_content_metrics = st.session_state['linkedin_content_metrics']  
                                    self.linkedin_content_metrics(linkedin_content_metrics)
                                    linkedin_engagement_rate = st.session_state['linkedin_engagement_rate'] 
                                    combined_text += f"\nLinkedin Engagement Rate: {linkedin_engagement_rate}%"
                                except KeyError:
                                    pass
                                try: # LINKEDIN CONTENT METRICS CSV
                                    combined_text += f"\nLinkedin Content Metrics: {linkedin_content_metrics.to_csv(index=True)}"
                                except UnboundLocalError:
                                    pass
                                try: # LINKEDIN CONTENT POST CSV
                                    combined_text += f"\nLinkedin Content Post: {linkedin_content_post.to_csv(index=True)}"
                                except UnboundLocalError:
                                    pass
                            except KeyError:
                                pass
    
                            try:
                                combined_text += f"\nInstagram Followers: {self.instagram}"
                                combined_text += f"\nInstagram Audience Engagement Rate: {self.instagram_er}%"
                                combined_text += f"\nInstagram Post Frequency: {self.instagram_pf}"
                            except KeyError:
                                pass

                            try:
                                combined_text += f"\nTwitter Followers: {self.twitter}"
                                combined_text += f"\nTwitter Audience Engagement Rate: {self.twitter_er}%"
                                combined_text += f"\nTwitter Post Frequency: {self.twitter_pf}"
                            except KeyError:
                                pass

                            try:
                                combined_text += f"\nYoutube Followers: {self.youtube}"
                                combined_text += f"\nYoutube Audience Engagement Rate: {self.youtube_er}%"
                                combined_text += f"\nYoutube Post Frequency: {self.youtube_pf}"

                            except KeyError:
                                pass

                            try:
                                combined_text += f"\nTiktok Followers: {self.tiktok_f}"
                                combined_text += f"\nTiktok Audience Engagement Rate: {self.tiktok_er}%"
                                combined_text += f"\nTiktok Post Frequency: {self.tiktok_pf}"

                            except KeyError:
                                pass

            
                            # OUTPUT FOR SEO ANALYST
                            payload_txt = {"question": combined_text}
                            result = self.request_model(payload_txt)
                            
                            end_time = time.time()
                            time_lapsed = end_time - start_time
                            debug_info = {
                                'analyst': self.analyst_name,
                                'url_uuid': self.model_url.split("-")[-1],
                                'time_lapsed': time_lapsed,
                                'facebook_organic_post': [fb_organic_post.name] if fb_organic_post else ['Not available'],
                                'fb_ads_campaign': [fb_ads_campaign.name] if fb_ads_campaign else ['Not available'],
                                'linkedin_content_metrics': [linkedin_metrics.name] if linkedin_metrics else ['Not available'],
                                'linkedin_content_post': [linkedin_post.name] if linkedin_post else ['Not available'],
                                'payload': payload_txt,
                                'result': result,
                            }
                            
                            collect_telemetry(debug_info)
                            
                            with st.expander("Debug information", icon="⚙"):
                                st.write(debug_info)

                            for df in st.session_state.keys():
                                del st.session_state[df]
                            for facebook_ad_campaign in st.session_state.keys():
                                del st.session_state[facebook_ad_campaign]

                            st.session_state['analyzing'] = False 
                    else:
                        st.info("Please upload CSV or PDF files first.")
                        hide_button()    
                except AttributeError:
                    st.info("Please upload CSV or PDF files first.")
                    hide_button() 

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
