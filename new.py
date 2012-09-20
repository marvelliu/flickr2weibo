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


    
class NewHandler(webapp.RequestHandler): 
        
    def post(self):
        nickname = self.request.get('nickname')
        password = self.request.get('password')
        confirmpassword = self.request.get('confirmpassword')
        
        if password != confirmpassword:
            self.response.out.write("Password not match")
            return
            
        userinfos = UserInfo.gql("WHERE nickname=:1",nickname)
        
        found = 0
        for userinfo in userinfos:
            userinfo = UserInfo()
            userinfo.nickname = nickname
            userinfo.password = password
            userinfo.put()
            found = 1
            break
        if found == 0:            
            userinfo = UserInfo()
            userinfo.nickname = nickname
            userinfo.password = password
            userinfo.put()
        self.response.out.write("updated")
        self.redirect("login.html")
            
            
            
application = webapp.WSGIApplication([
                                        ('/new', NewHandler)
                                     ],
                                     debug=True)
def main():
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()