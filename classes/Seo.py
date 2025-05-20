import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import pandas._libs.tslibs.parsing
import time
import chardet
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button
from helper.initialize_analyze_session import initialize_analyze_session


class Seo:
    def __init__(self, model_url):
        self.uploaded_files = []
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
        '''url = os.getenv('Link')
        st.write('Evaluation Form: [Link](%s)' % url)

        # RETURN BUTTON
        try:
            if st.button("Return", type='primary'):
                st.switch_page("./pages/home.py")
        except Exception:
            pass'''
        if 'bounce_rate' not in st.session_state:
            st.session_state['bounce_rate'] = ''
        if 'seo_scope' not in st.session_state:
            st.session_state['seo_scope'] = ''
        if 'page_index' not in st.session_state:
            st.session_state['page_index'] = ''
        if 'others' not in st.session_state:
            st.session_state['others'] = ''
        if 'df_traffic' not in st.session_state:
            st.session_state['df_traffic'] = ''
        if 'df_seo' not in st.session_state:
            st.session_state['df_seo'] = ''
      
    def detect_encoding(self, uploaded_file):
        result = chardet.detect(uploaded_file.read(100000))
        uploaded_file.seek(0)  # Reset file pointer to the beginning
        return result['encoding']

    def keyword_ranking(self, df_seo):
        keyword_ranking = df_seo
        st.session_state['keyword_ranking'] = keyword_ranking

        keywords_ranking_sorted = keyword_ranking.sort_values("Position", ascending=True)

        keywords_ranking_top_10 = keywords_ranking_sorted[keywords_ranking_sorted["Position"] <= 10].shape[0]
        keywords_ranking_top_100 = keywords_ranking_sorted[keywords_ranking_sorted["Position"] <= 100].shape[0]

        keyword_ranking = {
            'Keyword_top_10': keywords_ranking_top_10,
            'Keyword_top_100': keywords_ranking_top_100
        }
        st.session_state['keyword_ranking'] = keyword_ranking

    def traffic_files(self, df_traffic):
        traffic_channels = df_traffic
        try:
            traffic_channels.rename(columns={traffic_channels.columns[0]: 'date'}, inplace=True)
            traffic_channels['date'] = pd.to_datetime(traffic_channels['date'], format='mixed')
        except pandas._libs.tslibs.parsing.DateParseError:
            pass
        traffic_channels_sort = traffic_channels.sort_values("date", ascending=False)

        organic_traffic = traffic_channels_sort['Organic Search'].values[0]
        paid_traffic = traffic_channels_sort['Paid Search'].values[0]
        direct_traffic = traffic_channels_sort['Direct'].values[0]
        referral_traffic = traffic_channels_sort['Referral'].values[0]

        st.session_state['organic_traffic'] = organic_traffic
        st.session_state['paid_traffic'] = paid_traffic
        st.session_state['direct_traffic'] = direct_traffic
        st.session_state['referral_traffic'] = referral_traffic
   
    def ga4_traffic(self, others):
        st.session_state['others'] = others

        ga4_paid_social = others['Sessions'].values[0]
        ga4_organic_traffic = others['Sessions'].values[4]
        ga4_direct_traffic = others['Sessions'].values[2]
        ga4_referral_traffic = others['Sessions'].values[3]
        
        st.session_state['ga4_paid_social'] = ga4_paid_social
        st.session_state['ga4_organic_traffic'] = ga4_organic_traffic
        st.session_state['ga4_direct_traffic'] = ga4_direct_traffic
        st.session_state['ga4_referral_traffic'] = ga4_referral_traffic

    def delete_sessions(self):
        try:
            del st.session_state['df_traffic']
            del st.session_state['others']
            del st.session_state['df_seo']
            del st.session_state['keyword_ranking']   
            del st.session_state['ga4_paid_social']
            del st.session_state['ga4_organic_traffic']
            del st.session_state['ga4_direct_traffic']
            del st.session_state['ga4_referral_traffic']
            del st.session_state['organic_traffic']
            del st.session_state['paid_traffic']
            del st.session_state['direct_traffic']
            del st.session_state['referral_traffic']
        except KeyError:
            pass
    
    def process (self):
        session = st.session_state.analyze
        if ((self.uploaded_file or self.others or self.uploaded_file_seo) or (self.page_index or self.bounce_rate or self.seo_scope)) and  session == 'clicked':
                    seo_keywords = ""
                    traffic_channels = ""
                    traffic_aqcuisition = ""
                    pages_index = ""
                    bounce_rate = ""
                    seo_scope = ""
                    with st.spinner('Uploading Seo Files...', show_time=True):
                        st.write('')
                        
                        # INITIALIZING SESSIONS
                        pages_index += f"\nPages Indexed - Google Search Console Report:\nPages Indexed: {self.page_index}\n"
                        bounce_rate += f"Bounce Rate - GA4 Report:\nBounce Rate: {self.bounce_rate}%\n"
                        seo_scope += f"SEO Scope: {self.seo_scope}\n"
                        '''
                        try:
                            backlink_files = self.file_dict
                            combined_text += f"Number of backlinks {backlink_files}\n\n"
                        except KeyError:
                            pass
                        '''
                        try:
                            df_traffic = st.session_state['df_traffic']
                            self.traffic_files(df_traffic)

                            organic_traffic = st.session_state['organic_traffic']
                            paid_traffic = st.session_state['paid_traffic']
                            direct_traffic = st.session_state['direct_traffic']
                            referral_traffic = st.session_state['referral_traffic']

                            traffic_channels += f"Traffic Channels - SEMRush Report:\nOrganic Traffic: {organic_traffic}"
                            traffic_channels += f"\nPaid Traffic: {paid_traffic}"
                            traffic_channels += f"\nDirect Traffic: {direct_traffic}"
                            traffic_channels += f"\nReferral Traffic: {referral_traffic}"
                            traffic_channels += df_traffic.to_csv(index=True)
                            
                        except AttributeError:
                            pass
                        except KeyError as e:
                            # Check if 'df_traffic' is the missing key (no file uploaded)
                            if self.uploaded_file_seo:
                                pass
                            else:
                                # This would be triggered if df_traffic exists but the other keys are missing
                                st.info("Incorrect Traffic Channels SEMRush format. Please upload a valid SEMRush file.")
                        
                        try:
                            df_seo = st.session_state['df_seo']
                            self.keyword_ranking(df_seo)
                            keyword_ranking = st.session_state['keyword_ranking']    
                            seo_keywords += f"SEO Keywords - SEMRush Report:\nKeyword Ranking Top 10: {keyword_ranking['Keyword_top_10']}"
                            seo_keywords += f"\nKeyword Ranking Top 100: {keyword_ranking['Keyword_top_100']}\n\n"
                            
                            seo_keywords += df_seo.to_csv(index=True)
                        except AttributeError:
                            pass
                        except KeyError:
                            pass
                        
                        try:
                            others = st.session_state['others']
                            self.ga4_traffic(others)
                            ga4_paid_social = st.session_state['ga4_paid_social']
                            ga4_organic_traffic = st.session_state['ga4_organic_traffic']
                            ga4_direct_traffic = st.session_state['ga4_direct_traffic']
                            ga4_referral_traffic = st.session_state['ga4_referral_traffic']

                            traffics = ga4_direct_traffic + ga4_organic_traffic + ga4_paid_social + ga4_referral_traffic
                            
                            traffic_aqcuisition += f"Traffic Acquisition - GA4 Report:\nTraffics: {traffics}"
                            traffic_aqcuisition += f"\nPaid Traffic: {ga4_paid_social}\nOrganic Traffic: {ga4_organic_traffic}\nDirect Traffic: {ga4_direct_traffic}\nReferral Traffic: {ga4_referral_traffic}"
                        except KeyError:
                            
                            if self.others:
                                pass
                            else:
                                # This would be triggered if df_traffic exists but the other keys are missing
                                #st.info("Incorrect Traffic Acquisition GA4 format. Please upload a valid GA4 file.")
                                pass
                        except TypeError:
                            st.info("Incorrect Traffic Acquisition GA4 format. Please upload a valid GA4 file.")

                        #result = self.request_model(payload_txt_seo_keywords)
                        #end_time = time.time()
                        #time_lapsed = end_time - start_time
                        self.competitor_name = st.session_state.competitor_name
                        self.is_competitor = st.session_state.is_competitor
                        #self.competitor_name += seo_keywords

                        seo_keywords = self.competitor_name + seo_keywords if self.is_competitor == True else seo_keywords
                        traffic_channels = self.competitor_name + traffic_channels if self.is_competitor == True else traffic_channels
                        traffic_aqcuisition = self.competitor_name + traffic_aqcuisition if self.is_competitor == True else traffic_aqcuisition
                        pages_index = self.competitor_name + pages_index if self.is_competitor == True else pages_index
                        bounce_rate = self.competitor_name + bounce_rate if self.is_competitor == True else bounce_rate
                        seo_scope = self.competitor_name + seo_scope if self.is_competitor == True else seo_scope
                        
                        if self.is_competitor:
                            debug_info_seo_keywords = {'data_field': 'SEO Keywords Competitor', 'result': seo_keywords}
                            debug_info_traffic_channels = {'data_field': 'Traffic Channels Competitor', 'result': traffic_channels}
                            debug_info_traffic_aqcuisition = {'data_field': 'Traffic Acquisition Competitor', 'result': traffic_aqcuisition}
                            debug_info_pages_index = {'data_field': 'Pages Indexed Competitor', 'result': pages_index}
                            debug_info_bounce_rate = {'data_field': 'Bounce Rate Competitor', 'result': bounce_rate}
                            debug_info_seo_scope = {'data_field': 'SEO Scope Competitor', 'result': seo_scope}
                        else:
                            debug_info_seo_keywords = {'data_field': 'SEO Keywords', 'result': seo_keywords}
                            debug_info_traffic_channels = {'data_field': 'Traffic Channels', 'result': traffic_channels}
                            debug_info_traffic_aqcuisition = {'data_field': 'Traffic Acquisition', 'result': traffic_aqcuisition}
                            debug_info_pages_index = {'data_field': 'Pages Indexed', 'result': pages_index}
                            debug_info_bounce_rate = {'data_field': 'Bounce Rate', 'result': bounce_rate}
                            debug_info_seo_scope = {'data_field': 'SEO Scope', 'result': seo_scope}

                        '''
                        debug_info = {
                            #'analyst': self.analyst_name,
                            'url_uuid': self.model_url.split("-")[-1],
                            'time_lapsed': time_lapsed,
                            #'backlink_files': [*st.session_state['uploaded_files']],
                            #'seo_file': [self.uploaded_file_seo.name] if self.uploaded_file_seo else ['Not available'],
                            'payload': payload_txt,
                            'result': result,
                        }
                        '''
                        if self.bounce_rate:
                            st.session_state['bounce_rate'] = 'uploaded'
                            collect_telemetry(debug_info_bounce_rate)
                        if self.page_index:
                            st.session_state['pages_index'] = 'uploaded'
                            collect_telemetry(debug_info_pages_index)
                        if self.seo_scope:
                            st.session_state['seo_scope'] = 'uploaded'
                            collect_telemetry(debug_info_seo_scope)
                        if self.others:
                            st.session_state['others'] = 'uploaded'
                            collect_telemetry(debug_info_traffic_aqcuisition)
                        if self.uploaded_file:
                            st.session_state['df_traffic'] = 'uploaded'
                            collect_telemetry(debug_info_traffic_channels)
                        if self.uploaded_file_seo:
                            st.session_state['df_seo'] = 'uploaded'
                            collect_telemetry(debug_info_seo_keywords)
                        
                        #with st.expander("Debug information", icon="⚙"):
                        #    st.write(debug_info)

                        
                        #del st.session_state[df_traffic]
                        
                        #del st.session_state[df_seo]
                        
                        #del st.session_state[others]

                        st.session_state['analyzing'] = False    
             
    def row1(self):
            #st.write("") # FOR SPACINGs
            
            #st.write("") # FOR SPACINGs
            '''
            self.uploaded_files = st.file_uploader("Backlinks (SEO)", type=['pdf', 'csv'], accept_multiple_files=True, key="seo1")
            if self.uploaded_files:
                self.delete_sessions() 
                upload.upload_file_seo(self.uploaded_files)
                self.file_dict = upload.file_dict
            '''
            #st.write("") # FOR THE HIDE BUTTON
            self.uploaded_file_seo = st.file_uploader("SEO Keywords - SEMRush", type='csv', key="seo2")
            if self.uploaded_file_seo:
                self.delete_sessions() 
                try:
                    encoding_seo = self.detect_encoding(self.uploaded_file_seo)
                    st.session_state['df_seo'] = pd.read_csv(self.uploaded_file_seo, encoding=encoding_seo, low_memory=False)
                except Exception:
                    pass
            
            
            self.uploaded_file = st.file_uploader("Traffic Channels - SEMRush", type='csv')
            if self.uploaded_file:
                self.delete_sessions() 
                try:
                    encoding = self.detect_encoding(self.uploaded_file)
                    st.session_state['df_traffic'] = pd.read_csv(self.uploaded_file, encoding=encoding, low_memory=False)
                except Exception:
                    pass
           
            st.write("") # FOR THE HIDE BUTTON
            self.others = st.file_uploader("Traffic Acquisition - GA4", type='csv', key="seo5")
            if self.others:
                
                try:
                    st.session_state['others'] = pd.read_csv(self.others, skiprows=9)
                except Exception:
                    pass
            
            self.seo_scope = st.text_input("SEO Scope:", placeholder='Enter SEO Scope', help="i.e. Google.com.au, Google.com.ph")
            self.page_index = st.text_input("Pages Indexed - Google Search Console:", placeholder='Enter Pages Indexed')
            self.bounce_rate = st.text_input("Bounce Rate - GA4:", placeholder='Enter Bounce Rate')
            
            followers = {
                'Pages Indexed': self.page_index if self.page_index else 'N/A',
                'Bounce Rate': self.bounce_rate if self.bounce_rate else 'N/A'
            }
            
            #st.write("") # FOR THE HIDE BUTTON
            #st.write("") # FOR THE HIDE BUTTON
            #st.write("AI Analyst Output: ")
            st.session_state['analyzing'] = False
            #st.write("") # FOR THE HIDE BUTTON
            #analyze_button = st.button("Analyze", disabled=initialize_analyze_session())
            
            self.process()

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
