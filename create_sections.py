import os
from util import all_child_dir_paths, render_naked_markdown
from bs4 import BeautifulSoup
import markdown
import random
import json

def create_sections(gen):
    project_items = create_project_items(gen)
    random.shuffle(project_items)
    about = [item for item in project_items if item['name'] == 'about'][0]
    project_items.remove(about)
    project_items = [about] + project_items
    return [project_items]

def create_project_items(gen):
    projects_dir = os.path.join(gen.content_path, 'projects')
    items = [create_project_item(path, gen) for path in all_child_dir_paths(projects_dir)]
    return [i for i in items if i != None]

def create_project_item(path, gen):
    def render_md(name):
        md = open(os.path.join(path, 'preview.markdown')).read()
        html = markdown.markdown(md)
        return link_assets(html, path, gen)
    
    data_path = os.path.join(path, 'data.json')
    data = json.load(open(data_path)) if os.path.exists(data_path) else {}
    
    d = {
        "preview_html": render_md('preview.markdown'),
        "content_html": render_md('content.markdown'),
        "name": path.split('/')[-1],
        "classes": u" ".join(data.get('classes', []))
    }
    tile_path = os.path.join(path, 'tile.png')
    if os.path.exists(tile_path):
        d['style'] = u"background-image: url({0})".format(gen.include_asset(tile_path))
    return d

def find_first_image_url(html):
    b = BeautifulSoup(html, 'lxml')
    img = b.find('img')
    if img:
        return img.get('src')
    return ""

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
    return u"\n".join(map(unicode, soup.find('body').contents))
