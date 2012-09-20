import os
import sys
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.ext import webapp
from urllib2 import urlopen, URLError
import os
import flickrapi
from flickrapi import FlickrAPI
from flickrapi.tokencache import TokenCache
from google.appengine.ext import db
import webapp2
from config import *
from gaesessions import get_current_session
from userinfo import UserInfo
from tokenentity import TokenEntity

_DEBUG=True

class FlickrCallbackHandler(webapp.RequestHandler):
    def get(self):
        session = get_current_session()        
        frob = self.request.get('frob') 
        if not frob:
            self.response.out.write("no frob")
            return
        
        nickname = session.get("nickname", 0)
        if not nickname:
            self.response.out.write("no nickname")
            return
        userinfo = UserInfo.gql("WHERE nickname=:1", nickname).get()
        if not userinfo:
            self.response.out.write("no user")
            return
             
        flickr_api_key = userinfo.flickr_api_key
        flickr_api_secret = userinfo.flickr_api_secret
        flickr = flickrapi.FlickrAPI(
                    flickr_api_key, 
                    flickr_api_secret, 
                    store_token=False)
            
        try:
            token = flickr.get_token(frob)
            e = TokenEntity.gql("WHERE nickname=:1", nickname).get()
            if not e:
                e = TokenEntity()
            e.username = nickname
            e.token = token
            e.put()
            #session['flickr_token'] = token
        except Exception as e:
            print "Unexpected error:", e.message
        self.redirect('/setting')

        
application = webapp.WSGIApplication([
                                        ('/flickrcallback', FlickrCallbackHandler)
                                     ],
                                     debug=True)
def main():
    #util.run_wsgi_app(application)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()