import os

from block_functions import markdown_to_html_node
from text_functions import extract_title

def generate_page(basepath, template_path, from_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    with open(from_path, 'r') as file:
        content = file.read()
    with open(template_path, 'r') as file:
        template = file.read()

    node = markdown_to_html_node(content)
    html_content = node.to_html()
    title = extract_title(content)
    html = template.replace("{{ Content }}", html_content).replace("{{ Title }}", title)
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')

    directory = os.path.dirname(dest_path)
    os.makedirs(directory, exist_ok=True)
    with open(dest_path, "w") as file:
            file.write(html)

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):    
    entries = os.listdir(dir_path_content)
    
    # Loop through each entry
    for entry in entries:
        # Create full path to the entry
        entry_path = os.path.join(dir_path_content, entry)
        
        # If it's a file
        if os.path.isfile(entry_path):
            if entry_path.endswith('.md'):
                # Replace 'content' with 'public' and '.md' with '.html'
                dest_path = entry_path.replace(dir_path_content, dest_dir_path).replace('.md', '.html')
                generate_page(basepath, template_path, entry_path, dest_path)
        
        elif os.path.isdir(entry_path):
            generate_pages_recursive(basepath, entry_path, template_path, os.path.join(dest_dir_path, entry))
