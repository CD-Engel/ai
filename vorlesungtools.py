import streamlit as st
from groq import Groq

class Instruct:
    def __init__(self, model="llama3-70b-8192"):
        self.model = model
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)

    def instruction(self, sys_mess, instruct):
        message = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": sys_mess},
                {"role": "user", "content": instruct}
            ],
            model=self.model,
            temperature=0.0,
            response_format={"type": "text"},
        )
        return message.choices[0].message.content
