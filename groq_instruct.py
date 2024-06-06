from groq import Groq
from IPython.display import Markdown

def instruct(sysmsg, instr):
    c = Groq()
    r = c.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": sysmsg
            },
            {
                "role": "user",
                "content": instr
            }
        ],
        temperature=0.0,
        max_tokens=8192,
        top_p=1,
        stream=False,
        stop=None,
    )

    m = r.choices[0].message.content
    return m