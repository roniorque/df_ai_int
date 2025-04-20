import streamlit as st
import threading
from dotenv import load_dotenv
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button

class ThreadSafeHandler:
    def __init__(self, placeholder):
        self.placeholder = placeholder
        self.lock = threading.Lock()

    def update_info(self, message):
        with self.lock:
            try:
                self.placeholder.info(message)
            except Exception:
                pass

    def update_success(self, message):
        with self.lock:
            try:
                self.placeholder.success(message)
            except Exception:
                pass

    def update_error(self, message):
        with self.lock:
            try:
                self.placeholder.error(message)
            except Exception:
                pass

class CientSummary:
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
    
    def process(self):
        session = st.session_state.analyze
        if (self.client_summary or self.name or self.website) and session == 'clicked':
            try:
                # Prepare client data
                client_data = {
                    'client_summary': self.client_summary,
                    'client_name': self.name,
                    'client_website': self.website
                }

                # Placeholder to display feedback
                handler = ThreadSafeHandler(st.empty())

                def upload_client_data(field_key, field_value):
                    try:
                        handler.update_info(f"Uploading {field_key.replace('_', ' ').title()}...")
                        # Simulate the processing logic here
                        st.session_state[field_key] = 'uploaded'  # Mock upload success
                        collect_telemetry({'data_field': field_key.replace('_', ' ').title(), 'result': field_value})
                        handler.update_success(f"{field_key.replace('_', ' ').title()} uploaded.")
                    except Exception as e:
                        handler.update_error(f"Error uploading {field_key.replace('_', ' ').title()}: {e}")

                # Start threads for each client field
                threads = []
                for field_key, field_value in client_data.items():
                    thread = threading.Thread(target=upload_client_data, args=(field_key, field_value))
                    thread.start()
                    threads.append(thread)

                # Wait for all threads to complete
                for t in threads:
                    t.join()

                # Update session after processing
                st.session_state['analyzing'] = False
                st.success("🎉 Client Details Uploaded Successfully!")
            except AttributeError:
                st.info("Please fill out all fields first.")
                hide_button()

    def row1(self):
        self.client_summary = st.text_area("Client Summary:", help="Name of business, nature of business, location, products/services")
        session = st.session_state.analyze
        self.name = st.text_input("Client Name:")
        self.website = st.text_input("Client Website:")

        if (self.client_summary or self.name or self.website) and session == 'clicked':
            self.process()  # Call process method to initiate processing

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    upload = uploadFile()  # Assuming this is another helper class handling file uploads
