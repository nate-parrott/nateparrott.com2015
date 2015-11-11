import os
from util import all_child_dir_paths
from create_sections import create_project_item
from util import sanitize_name, ensure_clear_dir
from template import template

def create_detail_pages(gen):
    ensure_clear_dir(os.path.join(gen.site_path, 'projects'))
    projects_dir = os.path.join(gen.content_path, 'projects')
    for project_path in all_child_dir_paths(projects_dir):
        if os.path.isdir(project_path):
            create_detail_page(project_path, gen)

def create_detail_page(path, gen):
    data = create_project_item(path, gen)
    page_path = os.path.join(gen.site_path, 'projects', sanitize_name(data['name']) + '.html')
    open(page_path, 'w').write(template("project.html", data).encode('utf-8'))
