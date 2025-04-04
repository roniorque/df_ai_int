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

class Facebook:
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

        # AGENT NAME
        #st.header(self.analyst_name)

        # EVALUATION FORM LINK
        '''
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
        '''
        with st.expander("AI Analysis", expanded=True, icon="🤖"):
            st.table(df_output.style.set_table_styles(
            [{'selector': 'th:first-child, td:first-child', 'props': [('width', '20px')]},
            {'selector': 'th, td', 'props': [('width', '150px'), ('text-align', 'center')]}]
            ).set_properties(**{'text-align': 'center'}))
        '''

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

    def process(self):  
        start_time = time.time()
        session = st.session_state.analyze
        if session == 'clicked':
                hide_button()
                try:
                    if (self.fb_organic_post and self.fb_organic_post.name) or (self.fb_ads_campaign and self.fb_ads_campaign.name):
                        combined_text = ""
                        with st.spinner('Social Media Analyst...', show_time=True):
                            st.write('')
                            # INITIALIZING SESSIONS
                            #combined_text += f"Client Summary: {st.session_state.nature}\n"
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
            
                            # OUTPUT FOR SEO ANALYST
                            payload_txt = {"question": combined_text}
                            #result = self.request_model(payload_txt)
                            
                            end_time = time.time()
                            time_lapsed = end_time - start_time
                            debug_info = {'data_field' : 'Facebook', 'result': combined_text}
                            '''
                            debug_info = {
                                'analyst': self.analyst_name,
                                'url_uuid': self.model_url.split("-")[-1],
                                'time_lapsed': time_lapsed,
                                'facebook_organic_post': [fb_organic_post.name] if fb_organic_post else ['Not available'],
                                'fb_ads_campaign': [fb_ads_campaign.name] if fb_ads_campaign else ['Not available'],
                                'payload': payload_txt,
                                'result': result,
                            }
                            '''
                            collect_telemetry(debug_info)
                            
                            #with st.expander("Debug information", icon="⚙"):
                            #    st.write(debug_info)

                            
                            #del st.session_state[df]
                            #del st.session_state[facebook_ad_campaign]

                            st.session_state['analyzing'] = False 
                    
                except AttributeError:
                   
                    hide_button() 

    def row1(self):
            self.facebooks = st.number_input('Followers:', min_value=1, max_value=99999999, value=None, step=1, placeholder='Enter Followers')
            self.facebook_rr = st.text_input("Review Rate:", placeholder='Enter Review Rate')
            
            followers = {
                'Facebook Followers': self.facebooks if self.facebooks else 'N/A',
                'Facebook Review Rate': self.facebook_rr if self.facebook_rr else 'N/A',
            }

            self.fb_organic_post = self.file_upload("fb_post", "Organic Post CSV", "facebook_organic_post")
            self.fb_ads_campaign = self.file_upload("fb_campaign", "Ads Campaign CSV", "facebook_ad_campaign")
            
            self.fb_organic_post
            self.fb_ads_campaign
           
            '''
            st.write("") # FOR THE HIDE BUTTON
            st.write("") # FOR THE HIDE BUTTON
            st.write("AI Analyst Output: ")
            st.session_state['analyzing'] = False
            st.write("") # FOR THE HIDE BUTTON
           '''
            self.process()
            

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
