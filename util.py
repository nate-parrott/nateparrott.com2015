import os, shutil
import markdown
from bs4 import BeautifulSoup

def create_relative_path(path, relative_to):
    path_parts = path.split('/')
    relative_parts = relative_to.split('/')
    while len(path_parts) > 0 and len(relative_parts) > 0 and path_parts[0] == relative_parts[0]:
        path_parts = path_parts[1:]
        relative_parts = relative_parts[1:]
    return os.path.join(*path_parts)

def clear_dir(dir):
    for the_file in os.listdir(dir):
        file_path = os.path.join(dir, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
             shutil.rmtree(file_path)

def all_child_dir_paths(path):
    children = [os.path.join(path, name) for name in os.listdir(path)]
    return [child for child in children if os.path.isdir(child)]

def render_naked_markdown(md):
    soup = BeautifulSoup(markdown.markdown(md), 'lxml')
    return u"\n".join(map(unicode, soup.find('body').children))
