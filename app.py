import streamlit as st
from streamlit_option_menu import option_menu
from pathlib import Path
from jinja import Jinja, Documents
from instruct import instruct
from lettreSetting import appform



class App:
    def __init__(self):
        appform()
        self.model_list = ["groq-llama3", "claude-haiku", "claude-opus", "gpt-4o"]
        self.d = Documents("./documents")
        self.t = Jinja("./templates")
        self.msg = self.d.source["sysmsg"][0]["text"]
        self.state = st.session_state
        self.init_values = self.get_init_values()
        self.initialize_state()


    def get_init_values(self):
        return {'text': '', 'sys_msg': self.msg, 'index': 1, 'response': '', 'model': "groq-llama3", "instr_height": 700, "arg": "", "msg": self.msg}

    def initialize_state(self):
        if 'initialized' not in self.state:
            self.state.update(self.init_values)
            self.state['initialized'] = True


    def update_state(self):
        self.state["index"] = st.sidebar.number_input("Instruction index", step=1, value=self.state["index"])
        arg = self.d.source["arguments"][self.state["index"]]["text"]
        self.state["text"] = self.t.chain(['argument_valid', 'output_json'], {'argument_valid': {'argument': arg}})
        self.state['text'] = st.text_area("Instruktion", self.state['text'], height=self.state["instr_height"])

    def page_ai(self):
        self.update_state()
        if st.sidebar.button('reasoning',type="primary"):
            self.state['response'], _ = instruct(self.state['sys_msg'], self.state['text'], self.state["model"])
            ##st.markdown(self.state["response"], unsafe_allow_html=True)
            gg = {"markdown": self.state["response"]}
            ggg = self.t.chain(["output_md2html"], gg)
            st.markdown(ggg, unsafe_allow_html=True)

    def page_settings(self):
        self.state['instr_height'] = st.number_input("instruction height", step=1, value=self.state['instr_height'])
        self.state['model'] = st.selectbox("Choose model", self.model_list, index=self.model_list.index(self.state.get('model', 'groq-llama3')))

### RUN
    def run(self):
        st.sidebar.title('**Lettre AI**')
        with st.sidebar:
            selected = option_menu("", ["Instruct", 'Settings'], icons=['house', 'house', 'gear'], menu_icon="cast", default_index=0)
        if selected == "Instruct":
            self.page_ai()
        elif selected == "AI reasoning":
            self.page_reasoning()
        elif selected == "Settings":
            self.page_settings()
app = App()
app.run()