import os
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.ext import webapp
from google.appengine.ext import db
from config import *
from gaesessions import get_current_session
from userinfo import UserInfo


import sys
if sys.getdefaultencoding() != 'utf8':
    reload(sys)
    sys.setdefaultencoding('utf8')

_DEBUG=True
    
class LogoutHandler(webapp.RequestHandler):    
               
            
    def get(self):
        session = get_current_session()
        session.terminate()
        
        template_values = {
            'message' : "logout successfully"
        }
        cwd = os.path.dirname(__file__)
        path = os.path.join(cwd, 'templates', 'index.html')
        self.response.out.write(template.render(path, template_values, debug=_DEBUG))      
        
            
application = webapp.WSGIApplication([
                                        ('/logout', LogoutHandler)
                                     ],
                                     debug=True)
def main():
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()