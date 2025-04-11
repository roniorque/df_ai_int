import streamlit as st

def hide_sync_button():
    st.markdown(
        """
                    <style>
                    .element-container:nth-of-type(1) button {
                    display: none;
                    }
                    </style>
            """,
            unsafe_allow_html=True,
        )
        
def unhide_sync_button():
    st.markdown(
        """
            <style>
            element-container:nth-of-type(1) button {
            display: inline;
            }
            </style>
        """,
        unsafe_allow_html=True,
    )