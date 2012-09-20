import os
import codecs
import logging
import auth
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.ext import webapp
from google.appengine.ext import db
from urllib2 import urlopen, URLError, HTTPError
from config import *
from login import LoginHandler
from userinfo import UserInfo
from weibo import APIClient



import sys
if sys.getdefaultencoding() != 'utf8':
    reload(sys)
    sys.setdefaultencoding('utf8')

_DEBUG=True



class WeiboCallbackHandler(webapp.RequestHandler):


    def get(self): 
        nickname = LoginHandler().checkLogin()
        if not nickname:
            self.redirect("/")
        code = self.request.get('code')
        if not code:
            self.response.out.write("no code given")
            return

        try:
            client = APIClient(app_key=WEIBO_APP_KEY, app_secret=WEIBO_APP_SECRET, redirect_uri=WEIBO_CALLBACK_URL)
            r = client.request_access_token(code)
            weibo_id = client.client_id
            weibo_access_token = r.access_token
            weibo_expires_in = r.expires_in

            client.set_access_token(weibo_access_token, weibo_expires_in)
            
            r = client.get.account__get_uid()
            weibo_uid = r.uid
            
            r = client.get.users__show(uid=weibo_uid)            
            weibo_avatar = r.avatar_large
        
        
            userInfo = db.GqlQuery("SELECT * FROM UserInfo WHERE nickname=:1", nickname).get()
            
            if not userInfo:
                self.response.out.write("no such user %s" %nickname)
                return
            
            
            userInfo.weibo_id = weibo_id
            userInfo.weibo_access_token = weibo_access_token
            userInfo.weibo_expires_in = weibo_expires_in
            userInfo.weibo_avatar = weibo_avatar
            userInfo.put()
            
            weibo_auth_url = client.get_authorize_url()
            
            
                  
            if not userInfo.flickr_id :
                userInfo.flickr_id = ""
            if not userInfo.flickr_api_key:
                userInfo.flickr_api_key = ""
            if not userInfo.flickr_api_secret:
                userInfo.flickr_api_secret = ""
            if not userInfo.flickr_browse_type:
                userInfo.flickr_browse_type = "stream"
            if not userInfo.flickr_browse_typename:
                userInfo.flickr_browse_typename = ""
            if not userInfo.weibo_id:
                userInfo.weibo_id = ""
            if not userInfo.weibo_access_token:
                userInfo.weibo_access_token = ""
            if not userInfo.weibo_expires_in:
                userInfo.weibo_expires_in = ""
            if not userInfo.weibo_avatar:
                userInfo.weibo_avatar = ""
            
            flick_login_url = None
            if not auth.GetFlickrToken(userInfo.nickname):
                flick_login_url = auth.GetFlickrLoginUrl(userInfo)
            
            template_values = {
                'nickname': userInfo.nickname,
                'flickr_id': userInfo.flickr_id,
                'flickr_api_key': userInfo.flickr_api_key,
                'flickr_api_secret': userInfo.flickr_api_secret,
                'flickr_browse_type': userInfo.flickr_browse_type,
                'flickr_browse_typename': userInfo.flickr_browse_typename,
                'flickr_browse_setid': userInfo.flickr_browse_setid,
                'flickr_max_days': userInfo.flickr_max_days,
                'flick_login_url':flick_login_url,
                'weibo_id': userInfo.weibo_id,
                'weibo_access_token': userInfo.weibo_access_token,
                'weibo_expires_in': userInfo.weibo_expires_in,
                'weibo_auth_url' : weibo_auth_url,
                'weibo_avatar' : userInfo.weibo_avatar,
                'message' : u"用户信息已经更新完毕"
            }

            cwd = os.path.dirname(__file__)
            path = os.path.join(cwd, 'templates', 'setting.html')
            self.response.out.write(template.render(path, template_values, debug=_DEBUG))
        except Exception as e:
            self.response.out.write( "Unexpected error: %s"% (e))
        
            
application = webapp.WSGIApplication([
                                        ('/weibocallback', WeiboCallbackHandler)
                                     ],
                                     debug=True)
def main():
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()