import streamlit as st
from dotenv import load_dotenv
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button
from helper.initialize_analyze_session import initialize_analyze_session


class ClientSummary:
    def __init__(self):
        self.initialize()
        self.row1()

    def initialize(self):
        # FOR ENV
        load_dotenv()
        if 'client_summary' not in st.session_state:
            st.session_state['client_summary'] = ''
        if 'client_name' not in st.session_state:
            st.session_state['client_name'] = ''
        if 'client_website' not in st.session_state:
            st.session_state['client_website'] = ''
        if 'target_market' not in st.session_state:
            st.session_state['target_market'] = ''
    
    def process (self):
            with st.spinner('Uploading Client Details...', show_time=True):
                        st.write('')
                        #client_summary = ""
                        #client_name = ""
                        #client_website = ""
                        # 
                        #client_summary = ""
                        client_summary = f"{self.c_summary} {self.client_summary}\n"
                        client_name = f"{self.c_name} {self.name}\n"
                        client_website = f"{self.c_website} {self.website}\n"

                        debug_client_summary = {'data_field' : f'{self.c_summary}', 'result': client_summary}
                        debug_client_name = {'data_field' : f'{self.c_name}', 'result': client_name}
                        debug_client_website = {'data_field' : f'{self.c_website}', 'result': client_website}

                        if self.client_summary:
                            st.session_state['client_summary'] = 'uploaded'
                            st.session_state['target_market'] = 'uploaded'
                            collect_telemetry(debug_client_summary)
                        if self.name:
                            st.session_state['client_name'] = 'uploaded'
                            collect_telemetry(debug_client_name)
                        if self.website:
                            st.session_state['client_website'] = 'uploaded'
                            collect_telemetry(debug_client_website)
             
    def row1(self):
            is_competitor = st.session_state.is_competitor
            self.c_summary = "Competitor Summary: " if is_competitor == True else "Client Summary: "
            self.c_name = "Competitor Name: " if is_competitor == True else "Client Name: "
            self.c_website = "Competitor Website: " if is_competitor == True else "Client Website: "
            self.client_summary = st.text_area(f"{self.c_summary}", help="Name of business, nature of business, location, products/services")
            session = st.session_state.analyze
            self.name = st.text_input(f"{self.c_name}")
            self.website = st.text_input(f"{self.c_website}")

            if (self.client_summary or self.name or self.website) and session == 'clicked':
                self.process()


if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
