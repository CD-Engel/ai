import os
import streamlit as st
from streamlit_option_menu import option_menu
from groq import Groq
from vorlesungtools import Instruct
from instruct import instruct_execute

st.set_page_config(
    page_title="Instruct",
    page_icon="🤖",
    layout="wide",
)

instruct = Instruct()

def get_instruction():
    state['response'],_ = instruct_execute(state['sys_msg'], state['text'], state['model'])

init_values = {'text': '', 'sys_msg':'','response': '', 'model': 'groq-llama3'}
state = st.session_state
state.update({key: state.get(key, value) for key, value in init_values.items()})

state['sys_msg']="you are an assistant. Answer exactly what the user asks and do not provide additional information. You answer in English is elegant without exageration."

st.sidebar.title('**Lettre AI**')
with st.sidebar:
    selected = option_menu("", ["AI", 'Settings'], 
        icons=['house', 'gear'], menu_icon="cast", default_index=0)
    selected

    models = ["claude-opus","claude-haiku","groq-llama3","groq-mixtral"]
    state['model'] = st.sidebar.selectbox('Select model', models, index=2)

    if st.button("Senden"):
        get_instruction()

state['text'] = st.text_area("Ihre Instruktion", state['text'])
st.text_area("Antwort", state['response'],height=600)