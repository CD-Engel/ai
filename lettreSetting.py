import streamlit as st

def ststyle():
    hide_st_style = """
    <style>
    MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stMarkdown {border: none !important;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)


def appform():
        st.set_page_config(
            page_title="LettresAI Studio",
            page_icon="🧊",
            layout="wide"
        )
        #ststyle()  # Ändern Sie dies von st_style() zu ststyle()
        custom_css = """
        <style>
            * {
                box-sizing: content-box !important;
            }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)