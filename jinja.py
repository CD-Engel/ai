
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import re
import yaml
import streamlit as st

class Jinja:
    def __init__(self, tmpl_dir):
        tmpl_dir = Path(tmpl_dir)
        self.env = Environment(loader=FileSystemLoader(str(tmpl_dir)))
        self.tmpls = [
            {
                "file": f.stem,
                "params": re.findall(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}", self.env.loader.get_source(self.env, f.name)[0]),
                "content": self.env.get_template(f.name).render()
            }
            for f in tmpl_dir.glob("*.j2")
        ]

    def list(self):
        result = []
        for tmpl in self.tmpls:
            result.append({"file": tmpl['file'], "param": tmpl['params']})
        return result

    def show(self):
        for tmpl in self.tmpls:
            print(f"File: {tmpl['file']}")
            print(f"Parameters: {tmpl['params']}")
            print(f"Content:\n{tmpl['content']}")
            print("---")

    def chain(self, file_stems, dpara):
        self.list_chain = [
            {
                "file": f"{file_stem}.j2", 
                "para": dpara.get(file_stem, {}),
            }
            for file_stem in file_stems
        ]
        self.join_chain(dpara)
        return self.join

    def join_chain(self, dpara):
        join = ""
        mermaid_chart = "```mermaid\ngraph TD\n"
        previous_element = None
        for chain_obj in self.list_chain:
            file_stem = chain_obj['file'].split('.')[0]
            para_string = ', '.join(chain_obj['para'].keys())
            file_box_name = f"{file_stem}<br><small>{para_string}</small>"
            file_box = f"{file_stem}[{file_box_name}]"
            mermaid_chart += f"{file_box}\n"
            if previous_element:
                mermaid_chart += f"{previous_element} --> {file_box}\n"
            previous_element = file_box
            template = self.env.get_template(chain_obj["file"])
            chain_obj["content"] = template.render(chain_obj["para"])
            join += chain_obj["content"]
            if chain_obj["file"] in dpara:
                dpara[chain_obj["file"]] = chain_obj["content"]
        self.join = join
        self.mermaid_chart = mermaid_chart + "```"
    

class Documents:
    def __init__(self, source_dir):
        self.source_dir = Path(source_dir)
        self.source = self.load_documents()

    def load_documents(self):
        documents = {}
        for yaml_file in self.source_dir.glob('*.yaml'):
            with open(yaml_file, 'r') as file:
                yaml_dict = yaml.safe_load(file)
            documents[yaml_file.stem] = yaml_dict
        return documents