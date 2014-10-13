'''
Created on Oct 13, 2014

@author: cy
'''
from tornado.options import options
from tornado.web import url, RequestHandler
from src.common.markdown_parser import BasicParser
from src.common.settings import get_site_info

class HobbyPostHandler(RequestHandler):
    '''
    This handler is used to deal with the requests for single post page.
    Visiting url is http://localhost:9999/post_name.html
    '''
    def get(self):
        uri = self.request.uri
        print "ck:",uri
        post_name = uri.split("/")[3]
        full_name = post_name.split(".")[0] + ".markdown"
        post = BasicParser.parse(options.hobby_dir, full_name)
        params = get_site_info()
        template_file_name = "post.html"
        self.render(template_file_name, post = post, params = params)


handler = url(r"/hobby/post/.*", HobbyPostHandler)
