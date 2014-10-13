'''
Created on Oct 4, 2014

@author: sunnycomes
'''

from tornado.web import url, RequestHandler
from src.common.markdown_parser import get_all_parsed_hobby_posts
from src.common.settings import get_site_info

class HobbyIndexHandler(RequestHandler):
    '''
    This handler is used to deal with the requests for index page.
    Visiting url is http://localhost:9999/hobby
    '''
    def get(self):
        posts = get_all_parsed_hobby_posts()
        params = get_site_info()
        template_file_name = "hobbyindex.html"
        self.render(template_file_name, posts = posts, params = params)

handler = url(r"/hobby", HobbyIndexHandler)     