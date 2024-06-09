import streamlit as st
from streamlit_option_menu import option_menu
from instruct import instruct
from pathlib import Path
from jinja import Jinja, Documents

class App:
    def __init__(self):
        self.model_list = ["groq-llama3", "haiku", "qwen", "opus", "gpt-4o"]
        self.d = Documents("./documents")
        self.t = Jinja("./templates")
        self.msg = self.d.source["sysmsg"][0]["text"]
        self.state = st.session_state
        self.init_values = {'text': '', 'sys_msg': self.msg, 'index': 1, 'response': '', 'model': "groq-llama3", "instr_height": 700, "arg": "", "msg": self.msg}
        if 'initialized' not in self.state:
            self.state.update(self.init_values)
            self.state['initialized'] = True
    def exec_instruction(self):
        self.state['response'] = instruct(self.state['sys_msg'], self.state['text'], self.state["model"])
    def page_ai(self):
        self.state["index"] = st.sidebar.number_input("Instruction index", step=1, value=self.state["index"])
        arg = self.d.source["arguments"][self.state["index"]]["text"]
        self.state["text"] = self.t.chain(['argument_valid', 'output_markdown'], {'argument_valid': {'argument': arg}})
        self.state['text'] = st.text_area("Instruktion", self.state['text'], height=self.state["instr_height"])
        if st.sidebar.button("reasoning", args=("primary",)):
            self.exec_instruction()
        st.markdown(self.state["response"], unsafe_allow_html=True)
    def page_reasoning(self):
        rform = st.sidebar.radio("edit", ["text", "response"])
        if rform == "text":
            self.state['text'] = st.text_area("Instruktion", self.state['response'], height=self.state["instr_height"])
        else:
            st.markdown(self.state["response"], unsafe_allow_html=True)
    def page_settings(self):
        self.state['instr_height'] = st.number_input("instruction height", step=1, value=self.state['instr_height'])
    def run(self):
        st.sidebar.title('**Lettre AI**')
        with st.sidebar:
            selected = option_menu("", ["Instruct", "AI reasoning", 'Settings'], icons=['house', 'house', 'gear'], menu_icon="cast", default_index=0)
        if selected == "Instruct":
            self.page_ai()
        elif selected == "AI reasoning":
            self.page_reasoning()

app = App()
app.run()