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
    models = ["claude-haiku","groq-llama3","groq-mixtral"]
    state['model'] = st.sidebar.selectbox('Select model', models, index=1)
    state['text'] = st.text_area("Instruktion", state['text'],height=state["instr_height"])
    head="**"+state['model']+"**\n\n"
    st.markdown(head+state['response'])

def page_settings():
    state['instr_height']=st.number_input("instruction height",step=1,value=state['instr_height'])

init_values = {'text': '', 'sys_msg':'','response': '', 'model': 'groq-llama3',"instr_height":600}
state = st.session_state
state.update({key: state.get(key, value) for key, value in init_values.items()})


state['text']= '''
Use the method of truth-tables to determine, whether a given argument <argument> ARG </argument>  is
valid or not.  Use always the same letter for the same proposition.

<argument>
Wenn die Menschheit zu viel CO2 erzeugt, steigt der Wasserspiegel des Ozeans. 
Der Lebensstandard in Italien ist sehr hoch und die Menschheit erzeugt zu viel CO2. 
Der Lebensstandard in Indien ist nicht so hoch wie in Italien. 
Also steigt der Wasserspiegel.
</argument>
 
Use steps of reasoning:

  (i) tabulate the sentences in only two columns. Each row is one sentence. The conclusion as last row. The second column decompose the logical functions "and", "or", "if-then", "not".
  (ii) An argument consists of  assumptions which imply the truth of  a conclusion.
  (iii) Check the validity with a truth-table for validity: if the conclusion is true, all sentences as function of their propositions are true. 
(iv) Check those rows for which the conclusion is true. For those  only columns containing  the assumptions must be true. Do not consider elementary propositions. 

Output format is markdown format using LaTeX expressions
'''


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