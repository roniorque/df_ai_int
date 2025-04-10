import streamlit as st

def hide_button():
    st.markdown(
        """
                    <style>
                    .element-container:nth-of-type(3) button {
                    display: none;
                    }
                    </style>
            """,
            unsafe_allow_html=True,
        )
        
def unhide_button():
    st.markdown(
        """
            <style>
            element-container:nth-of-type(3) button {
            display: inline;
            }
            </style>
        """,
        unsafe_allow_html=True,
    )