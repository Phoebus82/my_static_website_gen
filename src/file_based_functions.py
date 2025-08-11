
import os
import shutil
from blocks import markdown_to_html_node, extract_title

def clean_b(b):
    if os.path.exists(b):
        shutil.rmtree(b)
    os.mkdir(b)

def copy_from_a_to_b(a, b):
    for i in os.listdir(a):
        i_a_path = os.path.join(a, i)
        i_b_path = os.path.join(b, i)
        if os.path.isfile(i_a_path):
            shutil.copy(i_a_path, i_b_path)
        else:
            os.mkdir(i_b_path)
            copy_from_a_to_b(i_a_path, i_b_path)

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path}, to {dest_path}, using {template_path}")
    with open(from_path,"r") as fi:
        md = fi.read()
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    with open(template_path, "r") as temp:
        tempo = temp.read()
    tempor = tempo.replace("{{ Title }}", title).replace("{{ Content }}", html)
    tempor = tempor.replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')
    if os.path.dirname(dest_path) != "":
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as fo:
        fo.write(tempor)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(entry_path) and entry_path.endswith(".md"):
            dest_file = entry.replace(".md", ".html")
            generate_page(entry_path, template_path, os.path.join(dest_dir_path, dest_file), base_path)
        else:
            new_dest = os.path.join(dest_dir_path, entry)
            os.makedirs(new_dest, exist_ok=True)
            generate_pages_recursive(entry_path, template_path, new_dest, base_path)

    