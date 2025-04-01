import streamlit as st

if 'analyze' not in st.session_state:
    st.session_state['analyze'] = ''


analyze_button = st.button("Analyze")

if analyze_button:
    st.session_state['analyze'] = 'clicked'

