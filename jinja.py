from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
import yaml
import streamlit as st
from jinja2.meta import find_undeclared_variables

class Jinja:
    def __init__(self, template_dir):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.tmpls = [
            {
                'file': t,
                'content': self.env.loader.get_source(self.env, t)[0],
                'params': list(find_undeclared_variables(self.env.parse(self.env.loader.get_source(self.env, t)[0])))
            }
            for t in self.env.list_templates()
        ]

    def render(self, file_stem, **kwargs):
        file_name = f"{file_stem}.j2"
        template = next((t for t in self.tmpls if t['file'] == file_name), None)
        if template is not None:
            jinja_template = self.env.from_string(template['content'])
            return jinja_template.render(**kwargs)
        else:
            raise ValueError(f"Template '{file_name}' not found.")

    def list(self):
        return [{"file": tmpl['file'], "params": tmpl['params']} for tmpl in self.tmpls]

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
