import shutil, os
from bs4 import BeautifulSoup as BS
from template import template
import json
import imgheuristics
from util import create_relative_path, clear_dir, ensure_clear_dir
from create_sections import create_sections
from create_detail_pages import create_detail_pages

def lorem_ipsum():
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam cursus tortor eu metus auctor gravida. Sed ligula nulla, viverra et lectus vel, aliquet commodo lorem."

class SiteGenerator(object):
    def __init__(self):
        pass
    
    def generate(self, site_path):
        self.content_path = 'content'
        self.site_path = os.path.expanduser(site_path)
        ensure_clear_dir(self.site_path)
        
        # copy static dir:
        self.static_dir = os.path.join(os.path.dirname(__file__), 'static')
        shutil.copytree(self.static_dir, os.path.join(self.site_path, 'static'))
        
        # create assets dir:
        self.assets_dir = os.path.join(self.site_path, 'assets')
        os.mkdir(self.assets_dir)
        self.assets_map = {}
        
        self.create_index()
        
        create_detail_pages(self)
    
    def include_asset(self, path, filter=None):
        key = path + ('-' + filter.id() if filter else "")
        if key not in self.assets_map:
            _, ext = os.path.splitext(path)
            if filter and filter.ext(): ext = filter.ext()
            asset_path = os.path.join(self.assets_dir, str(len(self.assets_map)) + ext)
            data = open(path).read()
            if filter: data = filter.filter(data)
            open(asset_path, "w").write(data)
            self.assets_map[key] = asset_path
        return '/' + create_relative_path(self.assets_map[key], self.site_path)
    
    def create_index(self):
        # write the index:
        v = {
            "sections": create_sections(self)
        }
        open(os.path.join(self.site_path, 'index.html'), 'w').write(template("index.html", v).encode('utf-8'))
    
class AssetFilter(object):
    def id(self):
        return ""
    def ext(self):
        return None
    def filter(self, data):
        return data

if __name__ == '__main__':
    SiteGenerator().generate('~/Desktop/site')
