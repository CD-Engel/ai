import os
import streamlit as st
from streamlit_option_menu import option_menu
from instruct import instruct_execute
from groq_instruct import instruct
from pathlib import Path
from jinja import Jinja,Documents
import yaml

st.set_page_config(
    page_title="Instruct",
    page_icon="🤖",
    layout="wide",
)


def exec_instruction():
    state['response'] = instruct(state['sys_msg'], state['text'])
def page_ai():
    state["index"]=st.sidebar.number_input("Instruction index",step=1,value=state["index"])
    arg=d.source["arguments"][state["index"]]["text"]
    state["text"]=t.chain(['argument_valid', 'output_markdown'], {'argument_valid': {'argument': arg}})
    state['text'] = st.text_area("Instruktion", state['text'],height=state["instr_height"])
    exec_instruction()
def page_reasoning():
    if st.sidebar.button("reasoning", type="primary"):
        exec_instruction()
    rform=st.sidebar.radio("edit",["text","response"])
    if rform=="text":
        state['text'] = st.text_area("Instruktion", state['response'],height=state["instr_height"])
    else:    
        st.markdown(state["response"],unsafe_allow_html=True)
def page_settings():
    state['instr_height']=st.number_input("instruction height",step=1,value=state['instr_height'])
def init():
    d = Documents("./documents")
    t = Jinja("./templates")
    msg=d.source["sysmsg"][0]["text"]
    return t,d,msg

t,d,msg=init()
init_values = {'text': '', 'sys_msg':'','index':1,'response': '', 'model': 'groq-llama3',"instr_height":700,"arg":"","msg":msg}
state = st.session_state
state.update({key: state.get(key, value) for key, value in init_values.items()})



state["sys_msg"]=state["msg"]
st.sidebar.title('**Lettre AI**')
with st.sidebar:
    selected = option_menu("", ["Instruct","AI reasoning", 'Settings'], 
        icons=['house', 'house','gear'], menu_icon="cast", default_index=0)


if selected == "Instruct":
    page_ai()
elif selected == "AI reasoning":
    page_reasoning()
elif selected == "Settings":
    page_settings()