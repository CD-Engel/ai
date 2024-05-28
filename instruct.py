import os
from groq import Groq
from openai import OpenAI
import anthropic
import ollama



def instruct_execute(sys_mess, instruct, model_short):
    model_vendors = {
        'claude-opus': {"model":"claude-3-opus-20240229",'vendor': 'anthropic', 'api_key': 'ANTHROPIC_API_KEY'},
        'claude-haiku': {'model': 'claude-3-haiku-20240307','vendor': 'anthropic', 'api_key': 'ANTHROPIC_API_KEY'},
        'groq-llama3': {'model':'llama3-70b-8192','vendor': 'groq', 'api_key': 'GROQ_API_KEY'},
        'groq-mixtral': {'model':'mixtral-8x7b-32768','vendor': 'groq', 'api_key': 'GROQ_API_KEY'},
        'gpt-4o': {'model':'gpt-4o','vendor': 'openai', 'api_key': 'OPENAI_API_KEY'},
        'dbrx': {'model':'dbrx','vendor': 'ollama', 'api_key': ''},
        'llama3': {'model':'llama3','vendor': 'ollama', 'api_key': ''},
        'llama3-70': {'model':'llama3:70b','vendor': 'ollama', 'api_key': ''},
        'mixtral': {'model':'mixtral:8x22b','vendor':'ollama','api_key': ''},
        'phi3-medium': {'model':'phi3:medium','vendor': 'ollama', 'api_key': ''},
        'aya-35b': {'model':'aya:35b','vendor':'ollama','api_key': ''},
        'llama3-chatqa': {'model':'llama3-chatqa:70b-v1.5-q4_1','vendor': 'ollama', 'api_key': ''},
    }

    if model_short not in model_vendors:
        raise ValueError("Invalid model")

    model = model_vendors[model_short]['model']
    vendor = model_vendors[model_short]['vendor']
    api_key = os.getenv(model_vendors[model_short]['api_key'])

    print(f"Chosen model: {model}, Vendor: {vendor.capitalize()}")

    if vendor == 'anthropic':
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=model, 
            max_tokens=4096,
            system=sys_mess,
            messages=[{"role": "user", "content": [{"type": "text", "text": instruct}]}]
        )
        gg = message.content[0].text

    elif vendor == 'groq':
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
        gg = message.choices[0].message.content

    elif vendor == 'openai':
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": sys_mess},
                {"role": "user", "content": instruct}
            ]
        )
        gg = response.choices[0].message.content

    elif vendor == 'ollama':
        response = ollama.chat(
            model=model, 
            messages=[
                {'role': 'system', 'content': sys_mess},
                {'role': 'user', 'content': instruct},
            ]
        )
        gg = response['message']['content']

    return gg, vendor

