import os
import codecs
import logging
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.ext import webapp
from google.appengine.ext import db
from urllib2 import urlopen, URLError, HTTPError
from config import *
from login import LoginHandler
from userinfo import UserInfo
from weibo import APIClient
import auth



import sys
if sys.getdefaultencoding() != 'utf8':
    reload(sys)
    sys.setdefaultencoding('utf8')

_DEBUG=True



class SettingHandler(webapp.RequestHandler):


    def get(self): 
        nickname = LoginHandler().checkLogin()
        if not nickname:
            self.redirect("/")
        
        #if True:
        try:
            userInfo = db.GqlQuery("SELECT * FROM UserInfo WHERE nickname=:1", nickname).get()
            
            if not userInfo:
                self.response.out.write("no such a user")
                return
            
            
            #client = APIClient(app_key=WEIBO_APP_KEY, app_secret=WEIBO_APP_SECRET, redirect_uri=WEIBO_CALLBACK_URL)
            weibo = auth.WeiboAuth(None)
            #client = OAuthHandler(WEIBO_APP_KEY, WEIBO_APP_SECRET)
            #weibo_auth_url = client.get_authorization_url()
        
            weibo_auth_url = None
            if V2:
                weibo_auth_url = weibo.get_authorize_url()
        
            if not userInfo.nickname:
                userInfo.nickname = ""        
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
            if not userInfo.weibo_access_token_secret:
                userInfo.weibo_access_token_secret = ""
            if not userInfo.weibo_avatar:
                userInfo.weibo_avatar = ""
                
            #flick_login_url = None
            #if not auth.GetFlickrToken(userInfo.nickname):
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
                'weibo_access_token_secret': userInfo.weibo_access_token_secret,
                'weibo_auth_url' : weibo_auth_url,
                'weibo_avatar' : userInfo.weibo_avatar
            }

            cwd = os.path.dirname(__file__)
            path = os.path.join(cwd, 'templates', 'setting.html')
            self.response.out.write(template.render(path, template_values, debug=_DEBUG))
        except Exception as e:
            self.response.out.write( "Unexpected error: %s"% (e))
        
    def post(self):
        if not LoginHandler().checkLogin():
            self.redirect("login.html")
        nickname = self.request.get('nickname')
        message = ""

        #if True:
        try:
            #client = APIClient(app_key=WEIBO_APP_KEY, app_secret=WEIBO_APP_SECRET, redirect_uri=WEIBO_CALLBACK_URL)
        
            userInfo = UserInfo.gql("WHERE nickname=:1",nickname).get()
            if not userInfo: 
                self.response.out.write( "No such a user: %s"% (nickname))
                return
            weibo = auth.WeiboAuth(userInfo)
            flickr = auth.FlickrAuth(userInfo)
            
            weibo_auth_url = None
            if V2:
                weibo_auth_url = weibo.get_authorize_url()
            
            userInfo.flickr_id = self.request.get('flickr_id')
            userInfo.flickr_api_key = self.request.get('flickr_api_key')
            userInfo.flickr_api_secret = self.request.get('flickr_api_secret')
            userInfo.flickr_browse_type = self.request.get('flickr_browse_type')
            userInfo.flickr_browse_typename = self.request.get('flickr_browse_typename')
            userInfo.weibo_id = self.request.get('weibo_id')
            userInfo.weibo_access_token = self.request.get('weibo_access_token')
            userInfo.weibo_access_token_secret = self.request.get('weibo_access_token_secret')
            
            if  userInfo.flickr_browse_type == "set" :
                #check flickr photoset
                sets = flickr.photosets_getList(user_id=userInfo.flickr_id)
                
                set_id = -1
                found = False
                for set in sets.findall('photosets/photoset'):
                    set_title = set.find('title').text        
                    if set_title == userInfo.flickr_browse_typename:                
                        set_id = int(set.attrib['id'])
                        found = True
                        break
                if found == False:
                    self.response.out.write( "No such photoset: %s"% (userInfo.flickr_browse_typename))
                    return            
                userInfo.flickr_browse_setid = set_id
            userInfo.flickr_max_days = int(self.request.get('flickr_max_days'))
            userInfo.put()
            message = "user information updated"
            
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
                'weibo_access_token_secret': userInfo.weibo_access_token_secret,
                'weibo_avatar' : userInfo.weibo_avatar,
                'weibo_auth_url' : weibo_auth_url,
                'message' : u"用户信息已经更新完毕"
                
            }

            cwd = os.path.dirname(__file__)
            path = os.path.join(cwd, 'templates', 'setting.html')
            self.response.out.write(template.render(path, template_values, debug=_DEBUG))
        except Exception as e:
            self.response.out.write( "Unexpected error: %s"% (e))
            
            
            
application = webapp.WSGIApplication([
                                        ('/setting', SettingHandler)
                                     ],
                                     debug=True)
def main():
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()