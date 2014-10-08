#!/usr/bin/env python

'''
Created on Oct 6, 2014

@author: sunnycomes
'''

import os
import shutil
from tornado.options import options
from src.common.utils import init_root_path, load_config
from src.common.template_parser import TemplateParser
from src.common.settings import get_site_info
from src.common import markdown_parser
from src.common.markdown_parser import BasicParser

def list_template_files():
    return os.listdir(options.current_template_dir)

def mkdir(dirx):
    if os.path.exists(dirx):
        return
    
    os.mkdir(dirx)
    
def rmdir(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    pass
    
def generate_index():
    posts = markdown_parser.get_all_parsed_posts()
    params = get_site_info()
    html = TemplateParser.parse(options.current_template_dir, "index.html", posts=posts, params=params)
    
    index_file = open("build/index.html", "wb")
    index_file.write(html)

def copy_static_files():
    dest = options.build_dir + os.sep + "static"
    rmdir(dest)
    shutil.copytree(options.static_resource_dir, dest)

def generate_posts():
    dest = options.build_dir + os.sep + "post"
    mkdir(dest)
    posts = markdown_parser.get_all_parsed_posts(brief=False)
    params = get_site_info()
    
    for post in posts:
        html = TemplateParser.parse(options.current_template_dir, "post.html", post=post, params=params)
        post_file = open(dest + os.sep + post["post_name"] + ".html", "wb")
        post_file.write(html)
    
def generate_about():  
    dest = options.build_dir + os.sep + "about"
    mkdir(dest)
    post = BasicParser.parse(options.about_dir, "about.markdown")
    post["title"] = options.author
    params = get_site_info()
    
    html = TemplateParser.parse(options.current_template_dir, "about.html", post=post, params=params)
    about_file = open(dest + os.sep + "index.html", "wb")
    about_file.write(html)

def generate():
    mkdir(options.build_dir)
    generate_index()
    copy_static_files()
    generate_posts()
    generate_about()
        
if __name__ == '__main__':
    root_path = os.path.dirname(os.path.abspath(__file__))
    init_root_path(root_path)
    
    config_file_path = root_path + os.sep + "setup.cfg"
    load_config(config_file_path)
    
    generate()
    