import os
import streamlit as st
from streamlit_option_menu import option_menu
from instruct import instruct_execute

st.set_page_config(
    page_title="Instruct",
    page_icon="🤖",
    layout="wide",
)

def get_instruction():
    state['response'],_ = instruct_execute(state['sys_msg'], state['text'], state['model'])

def page_ai():
    state['text'] = st.text_area("Instruktion", state['text'],height=state["instr_height"])
    head="**"+state['model']+"**\n\n"
    st.markdown(head+state['response'])

def page_settings():
    models = ["claude-haiku","groq-llama3","groq-mixtral"]
    state['model'] = st.sidebar.selectbox('Select model', models, index=2)
    state['instr_height']=st.number_input("instruction height",step=1,value=state['instr_height'])

init_values = {'text': '', 'sys_msg':'','response': '', 'model': 'groq-llama3',"instr_height":400}
state = st.session_state
state.update({key: state.get(key, value) for key, value in init_values.items()})

state['sys_msg']="you are an assistant. Answer exactly what the user asks and do not provide additional information. You answer in English is elegant without exageration."

st.sidebar.title('**Lettre AI**')
with st.sidebar:
    selected = option_menu("", ["AI", 'Settings'], 
        icons=['house', 'gear'], menu_icon="cast", default_index=0)
    if selected == "AI":
        if st.button("reasoning", type="primary"):
            get_instruction()

if selected == "AI":
    page_ai()
elif selected == "Settings":
    page_settings()