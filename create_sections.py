import os
from util import all_child_dir_paths, render_naked_markdown, link_assets, sanitize_name, kill_links
from bs4 import BeautifulSoup
import markdown
import random
import json
from dominant_colors import ui_colors

def create_sections(gen):
    order = ['flashlight', 'gerbil', 'aamoji', 'hackatbrown', 'squawk', 'brown apps', 'thisdayinhistory', 'swiftdial', 'instagrade', 'r2']
    project_items = create_project_items(gen)
    project_items.sort(key=lambda x: order.index(x['name']) if x['name'] in order else 99999)
    about = [item for item in project_items if item['name'] == 'about'][0]
    project_items.remove(about)
    project_items = [about] + project_items
    return [project_items]

def create_project_items(gen):
    projects_dir = os.path.join(gen.content_path, 'projects')
    items = [create_project_item(path, gen) for path in all_child_dir_paths(projects_dir)]
    return [i for i in items if i != None]

def create_project_item(path, gen):
    def render_md(name, asset_filter=None):
        md = open(os.path.join(path, name)).read()
        html = markdown.markdown(md.decode('utf-8'))
        return link_assets(html, path, gen, asset_filter=asset_filter)
    
    data_path = os.path.join(path, 'data.json')
    data = json.load(open(data_path)) if os.path.exists(data_path) else {}
    
    preview_html = render_md('preview.markdown')
    
    d = {
        "preview_html": preview_html,
        "preview_html_for_tile": kill_links(render_md('preview.markdown')),
        "content_html": render_md('content.markdown'),
        "name": path.split('/')[-1],
        "classes": u" ".join(data.get('classes', [])),
        "title": u"".join(map(unicode, BeautifulSoup(preview_html, 'lxml').find('h1').contents)),
        "link": data.get("link")
    }
    
    from crop import SquareCropAssetFilter
    tile_filter = SquareCropAssetFilter(size=500)
    tile_path = os.path.join(path, 'tile.png')
    if os.path.exists(tile_path):
        colors = ui_colors(tile_path)
        
        d['project_css'] = "<style>.header{ background-color: BG; color: COLOR; } .project_content a:link, .project_content a:visited { color: COLOR } </style>".replace('COLOR', colors['text']).replace('BG', colors['background'])
        
        d['style'] = u"background-image: url({0})".format(gen.include_asset(tile_path, filter=tile_filter))
        
        
    d['url'] = '/projects/' + sanitize_name(d['name']) + '.html'
    return d

def find_first_image_url(html):
    b = BeautifulSoup(html, 'lxml')
    img = b.find('img')
    if img:
        return img.get('src')
    return ""

