import os
import shutil

from markdown_blocks import (markdown_to_html_node,
    extract_title)

def cp_static_to_public():
    rm_public()
    path_list = os.listdir("./static")
    for path in path_list:
        recursive_cp(path)

def rm_public():
    remove_list = os.listdir("./public")
    for path in remove_list:
        full_path = os.path.join("./public", path)
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)
    
def recursive_cp(path):
    static_path = os.path.join("./static", path)
    public_path = os.path.join("./public", path)
    if os.path.isfile(static_path):
        print(f"Copying from {static_path} to {public_path}")
        shutil.copy(static_path, public_path)
    else:
        if not os.path.exists(public_path):
            print(f"Making directory {public_path}")
            os.mkdir(public_path)
        path_list = os.listdir(static_path)
        for child_path in path_list:
            recursive_cp(os.path.join(path, child_path))

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as markdown_file:
        markdown = markdown_file.read()
    with open(template_path) as template_file:
        template = template_file.read()
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    dest_dir = os.path.dirname(dest_path)
    dest_path = dest_path.replace(".md", ".html")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, mode = "w") as html_file:
        html_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path)
    else:
        path_list = os.listdir(dir_path_content)
        for child_path in path_list:
            full_child_path = os.path.join(dir_path_content, child_path)
            full_dest_path = os.path.join(dest_dir_path, child_path)
            generate_pages_recursive(full_child_path, template_path, full_dest_path)

def main():
    cp_static_to_public()
    generate_pages_recursive("./content", "./template.html", "./public")

main()

