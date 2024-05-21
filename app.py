import streamlit as st
import os
from groq import Groq

def instruction(sys_mess,instruct,model="llama3-70b-8192"):
    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    message = client.chat.completions.create(
        messages=[
            {"role": "system", "content":sys_mess},
            {"role": "user", "content": instruct}
        ],
        model=model,
        temperature=0.0,
        response_format={"type": "text"},
    )
    return message.choices[0].message.content

init_values = {'text': 'input instruct', 'response': ''}
st.session_state.update({key: st.session_state.get(key, value) for key, value in init_values.items()})

st.session_state['text'] = st.text_area("Instruktion", st.session_state['text'])

if st.session_state['text']:
    st.session_state['response'] = instruction("Systemnachricht", st.session_state['text'])

st.text_area("Antwort", st.session_state['response'])