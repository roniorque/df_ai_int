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
            output += f"\n\n **Current Footprint:** {current_footprint[i]}\n\n"
            output += f"**Number of Backlinks:** {number_of_backlinks[i]}"

        data = {
            "": [str(category) for category in categories],
            "Current Footprint": [str(footprint) for footprint in current_footprint],
            "Best of Breed Solutions": [str(backlink) for backlink in number_of_backlinks]
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
                    st.session_state['df_seo'] = pd.read_csv(self.uploaded_file_seo, encoding=encoding_seo, low_memory=False, key="seo3")
                except Exception:
                    pass
            
            
            self.uploaded_file = st.file_uploader("Traffic Channels - SEMRush", type='csv')
            if self.uploaded_file:
                self.delete_sessions() 
                try:
                    encoding = self.detect_encoding(self.uploaded_file)
                    st.session_state['df_traffic'] = pd.read_csv(self.uploaded_file, encoding=encoding, low_memory=False, key="seo4")
                except Exception:
                    pass
           
            st.write("") # FOR THE HIDE BUTTON
            self.others = st.file_uploader("Traffic Acquisition - GA4", type='csv', key="seo5")
            if self.others:
                self.delete_sessions()
                try:
                    st.session_state['others'] = pd.read_csv(self.others, skiprows=9)
                except Exception:
                    pass

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
            start_time = time.time()
            if st.session_state['analyze'] == 'clicked':
                hide_button()
                if self.uploaded_file or self.others or self.uploaded_file_seo:
                    combined_text = ""
                    with st.spinner('Seo Analyst...', show_time=True):
                        st.write('')
                        
                        # INITIALIZING SESSIONS
                        combined_text += f"Pages Indexed: {self.page_index}\n"
                        combined_text += f"Bounce Rate: {self.bounce_rate}\n"
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

                            combined_text += df_traffic.to_csv(index=True)

                            combined_text += f"\nOrganic Traffic: {organic_traffic}"
                            combined_text += f"\nPaid Traffic: {paid_traffic}"
                            combined_text += f"\nDirect Traffic: {direct_traffic}"
                            combined_text += f"\nReferral Traffic: {referral_traffic}"
                            
                        except KeyError:
                            pass
                        
                        try:
                            df_seo = st.session_state['df_seo']
                            self.keyword_ranking(df_seo)
                            keyword_ranking = st.session_state['keyword_ranking']    
                            combined_text += f"\nKeyword Ranking Top 10: {keyword_ranking['Keyword_top_10']}"
                            combined_text += f"\nKeyword Ranking Top 100: {keyword_ranking['Keyword_top_100']}\n\n"
                            
                            combined_text += df_seo.to_csv(index=True)
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
                            
                            combined_text += f"Traffics: {traffics}"
                            combined_text += f"Paid Traffic: {ga4_paid_social}\nOrganic Traffic: {ga4_organic_traffic}\nDirect Traffic: {ga4_direct_traffic}\nReferral Traffic: {ga4_referral_traffic}"
                        except KeyError:
                            pass
                        

                        # OUTPUT FOR SEO ANALYST
                        payload_txt = {"question": combined_text}
                        result = self.request_model(payload_txt)
                        end_time = time.time()
                        time_lapsed = end_time - start_time
                        debug_info = {
                            #'analyst': self.analyst_name,
                            'url_uuid': self.model_url.split("-")[-1],
                            'time_lapsed': time_lapsed,
                            #'backlink_files': [*st.session_state['uploaded_files']],
                            #'seo_file': [self.uploaded_file_seo.name] if self.uploaded_file_seo else ['Not available'],
                            'payload': payload_txt,
                            'result': result,
                        }
                        
                        collect_telemetry(debug_info)
                            
                        with st.expander("Debug information", icon="⚙"):
                            st.write(debug_info)

                        for df_traffic in st.session_state.keys():
                            del st.session_state[df_traffic]
                        for df_seo in st.session_state.keys():
                            del st.session_state[df_seo]
                        for others in st.session_state.keys():
                            del st.session_state[others]
                        print("done1")
                        st.session_state['analyzing'] = False    
                         

if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
