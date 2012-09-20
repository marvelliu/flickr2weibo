import os
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.ext import webapp
from config import *

_DEBUG=True

class PostHandler(webapp.RequestHandler):
    def get(self):
        content=self.request.get('content')

        template_values = {
            'content': content,
        }

        cwd = os.path.dirname(__file__)
        path = os.path.join(cwd, 'templates', 'postresult.html')
        self.response.out.write(template.render(path, template_values, debug=_DEBUG))

        
application = webapp.WSGIApplication([
                                        ('/post', PostHandler)
                                     ],
                                     debug=True)
def main():
    #util.run_wsgi_app(application)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()