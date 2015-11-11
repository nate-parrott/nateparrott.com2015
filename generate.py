import shutil, os
from bs4 import BeautifulSoup as BS
from template import template
import json
import imgheuristics
from util import create_relative_path, clear_dir
from create_sections import create_sections

def lorem_ipsum():
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam cursus tortor eu metus auctor gravida. Sed ligula nulla, viverra et lectus vel, aliquet commodo lorem."

class SiteGenerator(object):
    def __init__(self):
        pass
    
    def generate(self, site_path):
        self.content_path = 'content'
        self.site_path = os.path.expanduser(site_path)
        if not os.path.exists(self.site_path):
            os.mkdir(self.site_path)
        clear_dir(self.site_path)
        
        # copy static dir:
        self.static_dir = os.path.join(os.path.dirname(__file__), 'static')
        shutil.copytree(self.static_dir, os.path.join(self.site_path, 'static'))
        
        # create assets dir:
        self.assets_dir = os.path.join(self.site_path, 'assets')
        os.mkdir(self.assets_dir)
        self.assets_map = {}
        
        self.create_index()
    
    def include_asset(self, path):
        if path not in self.assets_map:
            _, ext = os.path.splitext(path)
            asset_path = os.path.join(self.assets_dir, str(len(self.assets_map)) + ext)
            shutil.copy(path, asset_path)
            self.assets_map[path] = asset_path
        return '/' + create_relative_path(self.assets_map[path], self.site_path)
    
    def create_index(self):
        # write the index:
        v = {
            "sections": create_sections(self)
        }
        open(os.path.join(self.site_path, 'index.html'), 'w').write(template("index.html", v).encode('utf-8'))
    
    
if __name__ == '__main__':
    SiteGenerator().generate('~/Desktop/site')
