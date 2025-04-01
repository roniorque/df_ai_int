import streamlit as st

def initialize_analyze_session():
        if 'analyzing' not in st.session_state:
            st.session_state['analyzing'] = False
        return st.session_state.get('analyzing', False)
    