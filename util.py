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

def ensure_clear_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    clear_dir(dir)

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

def sanitize_name(name):
    name = name.replace(" ", "-").lower()
    allowed = 'abcdefghijklmnopqrstuvwxyz0123456789_+'
    name = u''.join([c for c in name if c in allowed])
    return name

def link_assets(html, path, gen):
    b = BeautifulSoup(html, 'lxml')
    for img in b.find_all('img'):
        if img.get('src') and '/' not in img['src']:
            asset_path = os.path.join(path, img['src'])
            if os.path.exists(asset_path):
                img['src'] = gen.include_asset(asset_path)
            else:
                print "Asset missing:", asset_path
    return extract_body_from_soup(b)

def extract_body_from_soup(soup):
    body = soup.find('body')
    return u"\n".join(map(unicode, body.contents)) if body else ""

def kill_links(html):
    soup = BeautifulSoup(html, 'lxml')
    for a in soup.find_all('a'):
        a.name = 'span'
    return extract_body_from_soup(soup)
