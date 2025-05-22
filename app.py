import streamlit as st
import os
from dotenv import load_dotenv

# Create an empty container
placeholder = st.empty()
load_dotenv()

actual_email = os.getenv('email')
actual_password = os.getenv('password')

# Simple login form
with placeholder.form("login"):
    st.markdown("#### Digital Footprint AI Team")
    email = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit and email == actual_email and password == actual_password:
    st.session_state['logged_in'] = True
    st.switch_page("pages/home.py")
    st.success("Login successful")
elif submit and email != actual_email and password != actual_password:
    st.error("Login failed")
else:
    pass