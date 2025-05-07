import os
import shutil
import sys
from textnode import TextNode, TextType
from page_generator import generate_pages_recursive

basepath = "/"

if len(sys.argv) > 1:
    basepath = sys.argv[1]

def copy_static_files(src_dir, dest_dir):
    if os.path.exists(dest_dir):
        print(f"Removing existing directory: {dest_dir}")
        shutil.rmtree(dest_dir)
   
    print(f"Creating directory: {dest_dir}")
    os.makedirs(dest_dir, exist_ok=True)

    items = os.listdir(src_dir)

    for item in items:
        source_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} to {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            print(f"Copying directory: {source_path} to {dest_path}")
            shutil.copytree(source_path, dest_path)


def main():

    source_dir = "static"
    dest_dir = "docs"

    print(f"Copying static files from {source_dir} to {dest_dir}...")
    copy_static_files(source_dir, dest_dir)
    print("Static files copied successfully!")
    
    generate_pages_recursive(basepath, "content", "template.html", "docs")

if __name__ == "__main__":
    main()