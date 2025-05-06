import os

from block_functions import markdown_to_html_node
from text_functions import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    with open(from_path, 'r') as file:
        content = file.read()
    with open(template_path, 'r') as file:
        template = file.read()

    node = markdown_to_html_node(content)
    html_content = node.to_html()
    title = extract_title(content)
    html = template.replace("{{ Content }}", html_content).replace("{{ Title }}", title)

    directory = os.path.dirname(dest_path)
    os.makedirs(directory, exist_ok=True)
    with open(dest_path, "w") as file:
            file.write(html)

