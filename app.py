import os
import streamlit as st
from streamlit_option_menu import option_menu
from groq import Groq
from vorlesungtools import Instruct


# Initialisierung der Klasse
instruct = Instruct()

init_values = {'text': '', 'response': ''}
st.session_state.update({key: st.session_state.get(key, value) for key, value in init_values.items()})

with st.sidebar:
    selected = option_menu("", ["AI", 'Settings'], 
        icons=['house', 'gear'], menu_icon="cast", default_index=1)
    selected

st.session_state['text'] = st.text_area("Geben Sie hier Ihren Text ein", st.session_state['text'])
sys_msg="you are an assistant. Answer exactly what the user asks and do not provide additional information. You answer in English is elegant without exageration."
if st.session_state['text']:
    st.session_state['response'] = instruct.instruction("sys_msg", st.session_state['text'])

st.text_area("Antwort", st.session_state['response'])