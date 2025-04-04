import streamlit as st
import pandas as pd
import pymupdf
from helper.button_behaviour import hide_button, unhide_button

class uploadFile:
    def __init__(self):
        self.file_dict = {}
        self.file_gt = {}
    
    def multiple_upload_file(self, uploaded_files):
        for _ in range(len(self.file_dict)):
            self.file_dict.popitem() 

        for uploaded_file in uploaded_files:
            if uploaded_file.type == "application/pdf":
                try:
                    with pymupdf.open(stream=uploaded_file.read(), filetype="pdf") as doc:  
                        text = chr(12).join([page.get_text() for page in doc])
                        self.file_dict[uploaded_file.name] = {'type': 'pdf', 'content': text}
                except Exception:
                    pass
            elif uploaded_file.type == "text/csv":
                try:
                    df = pd.read_csv(uploaded_file)
                    self.file_dict[uploaded_file.name] = {'type': 'csv', 'content': df}
                except Exception:
                    pass
   
            st.session_state['uploaded_files'] = self.file_dict

    def upload_file_seo(self, uploaded_files):
        for _ in range(len(self.file_dict)):
            self.file_dict.popitem() 

        for uploaded_file in uploaded_files:
            if uploaded_file.type == "application/pdf":
                try:
                    with pymupdf.open(stream=uploaded_file.read(), filetype="pdf") as doc:  
                        text = chr(12).join([page.get_text() for page in doc])
                        self.file_dict[uploaded_file.name] = {'type': 'pdf', 'content': text}
                except Exception:
                    pass
            elif uploaded_file.type == "text/csv":
                try:
                    content = uploaded_file.read().decode("utf-8")
                    self.file_dict[uploaded_file.name] = {'type': 'csv', 'content': content}
                except Exception:
                    pass
   
            st.session_state['uploaded_files'] = self.file_dict
    
    def upload_gt(self, gtmetrix):
        for _ in range(len(self.file_gt)):
            self.file_gt.popitem() 

        for gtmetrixs in gtmetrix:
            if gtmetrixs.type == "application/pdf":
                try:
                    with pymupdf.open(stream=gtmetrixs.read(), filetype="pdf") as doc:  
                        text = chr(12).join([page.get_text() for page in doc])
                        self.file_gt[gtmetrixs.name] = {'type': 'pdf', 'content': text}
                except Exception:
                    pass
            elif gtmetrixs.type == "text/csv":
                try:
                    content = gtmetrixs.read().decode("utf-8")
                    self.file_dict[gtmetrixs.name] = {'type': 'csv', 'content': content}
                except Exception:
                    pass
            st.session_state['uploaded_gt'] = self.file_gt

if __name__ == "__main__":
    app = uploadFile()
    st.set_page_config(layout="wide")



