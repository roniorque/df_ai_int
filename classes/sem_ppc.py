import streamlit as st
from dotenv import load_dotenv
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button


class Sem_PPC:
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
        if 'account_set_up' not in st.session_state:
            st.session_state['account_set_up'] = ''
        if 'search_ads' not in st.session_state:
            st.session_state['search_ads'] = ''
        if 'display_ads' not in st.session_state:
            st.session_state['display_ads'] = ''
        if 'mobile_ads' not in st.session_state:
            st.session_state['mobile_ads'] = ''
        if 'video_ads' not in st.session_state:
            st.session_state['video_ads'] = ''
        if 'shopping_ads' not in st.session_state:
            st.session_state['shopping_ads'] = ''

    def process(self):
        session = st.session_state.analyze
        if (self.account_set_up or self.search_ads or self.display_ads or self.mobile_ads or self.video_ads or self.shopping_ads) and session == 'clicked':
                    try:
                        account_set_up = ""
                        search_ads = ""
                        display_ads = ""
                        mobile_ads = ""
                        video_ads = ""
                        shopping_ads = ""
                        with st.spinner('Uploading SEM/PPC...', show_time=True):
                                st.write('')
                                # INITIALIZING SESSIONS
                                #combined_text += f"Client Summary: {st.session_state.nature}\n"
                                try:
                                    account_set_up += f"\nGoogle Ads Report:\nAccount Set Up: {self.account_set_up}"
                                except KeyError:
                                    pass
                                try:
                                    search_ads += f"\nGoogle Ads Report:\nSearch Ads: {self.search_ads}"
                                except KeyError:
                                    pass
                                try:
                                    display_ads += f"\nGoogle Ads Report:\nDisplay Ads: {self.display_ads}"
                                except KeyError:
                                    pass
                                try:
                                    mobile_ads += f"\nGoogle Ads Report:\nMobile Ads: {self.mobile_ads}"
                                except KeyError:
                                    pass
                                try:
                                    video_ads += f"\nGoogle Ads Report:\nVideo Ads: {self.video_ads}"
                                except KeyError:
                                    pass
                                try:
                                    shopping_ads += f"\nGoogle Ads Report:\nShopping Ads: {self.shopping_ads}"
                                except KeyError:
                                    pass

                                # OUTPUT FOR SEO ANALYST
                                #payload_txt = {"question": combined_text}
                                #result = self.request_model(payload_txt)
                                
                                #end_time = time.time()
                                #time_lapsed = end_time - start_time
                                
                                self.competitor_name = st.session_state.competitor_name
                                self.is_competitor = st.session_state.is_competitor

                                account_set_up = self.competitor_name + account_set_up if self.is_competitor == True else account_set_up
                                search_ads = self.competitor_name + search_ads if self.is_competitor == True else search_ads
                                display_ads = self.competitor_name + display_ads if self.is_competitor == True else display_ads
                                mobile_ads = self.competitor_name + mobile_ads if self.is_competitor == True else mobile_ads
                                video_ads = self.competitor_name + video_ads if self.is_competitor == True else video_ads
                                shopping_ads = self.competitor_name + shopping_ads if self.is_competitor == True else shopping_ads
                        
                                if self.is_competitor:
                                    debug_info_account_set_up = {'data_field' : 'Account Set Up - Google Ads Competitor', 'result': account_set_up}
                                    debug_info_search_ads = {'data_field' : 'Search Ads - Google Ads/SEMRush Competitor', 'result': search_ads}
                                    debug_info_display_ads = {'data_field' : 'Display Ads - Google Ads/SEMRush Competitor', 'result': display_ads}
                                    debug_info_mobile_ads = {'data_field' : 'Mobile Ads - Google Ads Competitor', 'result': mobile_ads}
                                    debug_info_video_ads = {'data_field' : 'Video Ads - Google Ads Competitor', 'result': video_ads}
                                    debug_info_shopping_ads = {'data_field' : 'Shopping Ads - Google Ads/SEMRush Competitor', 'result': shopping_ads}
                                else:
                                    debug_info_account_set_up = {'data_field' : 'Account Set Up - Google Ads', 'result': account_set_up}
                                    debug_info_search_ads = {'data_field' : 'Search Ads - Google Ads/SEMRush', 'result': search_ads}
                                    debug_info_display_ads = {'data_field' : 'Display Ads - Google Ads/SEMRush', 'result': display_ads}
                                    debug_info_mobile_ads = {'data_field' : 'Mobile Ads - Google Ads', 'result': mobile_ads}
                                    debug_info_video_ads = {'data_field' : 'Video Ads - Google Ads', 'result': video_ads}
                                    debug_info_shopping_ads = {'data_field' : 'Shopping Ads - Google Ads/SEMRush', 'result': shopping_ads}
                                '''
                                debug_info = {
                                    #'analyst': self.analyst_name,
                                    'url_uuid': self.model_url.split("-")[-1],
                                    'time_lapsed': time_lapsed,
                                    'payload': payload_txt,
                                    'result': result,
                                }
                                '''
                                if self.account_set_up:
                                    st.session_state['account_set_up'] = 'uploaded'
                                    collect_telemetry(debug_info_account_set_up)
                                if self.search_ads:
                                    st.session_state['search_ads'] = 'uploaded'
                                    collect_telemetry(debug_info_search_ads)
                                if self.display_ads:
                                    st.session_state['display_ads'] = 'uploaded'
                                    collect_telemetry(debug_info_display_ads)
                                if self.mobile_ads:
                                    st.session_state['mobile_ads'] = 'uploaded'
                                    collect_telemetry(debug_info_mobile_ads)
                                if self.video_ads:
                                    st.session_state['video_ads'] = 'uploaded'
                                    collect_telemetry(debug_info_video_ads)
                                if self.shopping_ads:
                                    st.session_state['shopping_ads'] = 'uploaded'
                                    collect_telemetry(debug_info_shopping_ads)
                                
                
                                
                                #with st.expander("Debug information", icon="⚙"):
                                #    st.write(debug_info)

                                st.session_state['analyzing'] = False 
                    except AttributeError:
                        st.info("Please upload CSV or PDF files first.")
                        hide_button() 

    def row1(self):
            self.account_set_up = st.text_input("Account Set Up - Google Ads:", placeholder='Enter Account Set Up')
            self.search_ads = st.checkbox("Search Ads - Google Ads/SEMRush")
            self.display_ads = st.checkbox("Display Ads - Google Ads/SEMRush")
            self.mobile_ads = st.checkbox("Mobile Ads - Google Ads")
            self.video_ads = st.checkbox("Video Ads - Google Ads")
            self.shopping_ads = st.checkbox("Shopping Ads - Google Ads/SEMRush")

            '''
            st.write("") # FOR THE HIDE BUTTON
            st.write("") # FOR THE HIDE BUTTON
            st.write("AI Analyst Output: ")
            st.session_state['analyzing'] = False
            st.write("") # FOR THE HIDE BUTTON'
            '''
            #analyze_button = st.button("Analyze", disabled=initialize_analyze_session())
            self.process()
            
if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
