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
    
class LoginHandler(webapp.RequestHandler):    
        
    def checkLogin(self):
        session = get_current_session()
        nickname = session.get("nickname", 0)
        if nickname:
            return nickname
        else:
            return False
            
    def checkReg(self):        
        userinfos = db.GqlQuery("SELECT * FROM UserInfo")  
        return (userinfos.count() > 0)
        
            
    def get(self):
        self.redirect("login.html")
        
    def post(self):
        nickname = self.request.get('nickname')
        password = self.request.get('password')
        
        userinfos = UserInfo.gql("WHERE nickname=:1", nickname)
        
        for userinfo in userinfos:
            if userinfo.password == password:
                session = get_current_session()
                session["nickname"] = nickname
                
        
                template_values = {
                    'nickname': nickname,
                    'message' : "login successfully"
                }
                cwd = os.path.dirname(__file__)
                path = os.path.join(cwd, 'templates', 'index.html')
                self.response.out.write(template.render(path, template_values, debug=_DEBUG))              
            else:
                self.response.out.write("Login failed") 
                self.response.out.write("<br/><a href=\"/login\">retry</a>")
            break
            
            
application = webapp.WSGIApplication([
                                        ('/login', LoginHandler)
                                     ],
                                     debug=True)
def main():
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()