#!/usr/bin/python

# -- coding: utf-8 --

import sys
import time
import os
import urllib
import flickrapi
import auth
import webapp2
import logging
from time import mktime
from datetime import datetime, date, timedelta
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.ext import webapp
from urllib2 import urlopen, URLError
from flickrapi import FlickrAPI, FlickrError
from flickrapi.tokencache import TokenCache
from google.appengine.ext import db
from config import *
from weibo import APIClient
#from gaesessions import get_current_session
from userinfo import UserInfo
from flickrentity import FlickrRecord
from imageentity import ImageEntity
from google.appengine.api import urlfetch

from weibopy.auth import OAuthHandler
from weibopy.api import API
from weibopy.error import WeibopError

try:
    import json
except ImportError:
    from django.utils import simplejson as json


if sys.getdefaultencoding() != 'utf8':
    reload(sys)
    sys.setdefaultencoding('utf8')

_DEBUG=True



class FlickrListHandler(webapp2.RequestHandler):
    
    def Upload(self, weibo, status, source=None, lat=None, long=None, url=None, image=None):
        
        ext = ""
        filename = ""
        n = url.rfind('.')
        if n != (-1):
            ext = url[n:].lower()
        n = url.rfind('/')
        if n != (-1):
            filename = url[n+1:].lower()            
        
        if not V2:
            weibo.upload(str(filename), status, source=source, lat=lat, long=long, image=image)
            #weibo.update_status(status, lat=lat, long=lat)
        else:
            if ext == ".jpg":
                weibo.upload.statuses__upload(status=status, lat=lat, long=long, url=url, pic_jpg=image)
            elif ext == ".gif":
                weibo.upload.statuses__upload(status=status, lat=lat, long=long, url=url, pic_gif=image)                
            elif ext == ".png":
                weibo.upload.statuses__upload(status=status, lat=lat, long=long, url=url, pic_png=image)
                
    def PostWeibo(self, weibo, entity, imageentity, handleExcept=False):
        
        logging.info( "posting %s "% entity.photo_id)
        self.response.out.write( "posting %s <br/>"% entity.photo_id)
                
        n = imageentity.url.rfind('.')
        if n != (-1):
            ext = imageentity.url[n:].lower()
        
        title = (u'我上传了一些照片：%s %s' % (entity.title, entity.link))
        try:
            self.Upload(weibo, title, source = WEIBO_APP_KEY,lat=entity.latitude, long=entity.longitude, url=imageentity.url, image=imageentity.image)
            #weibo.post.statuses__upload_url_text(status=title, lat=entity.latitude, long=entity.longitude, url=imageentity.url)
            
            #elif 
            #weibo.post.statuses__update(status=title, lat=entity.latitude, long=entity.longitude)
            return True

        except Exception as e:
            logging.info( "post exception: %s "% (e))
            self.response.out.write("post exception: %s "% (e))
            #weibo = auth.WeiboReauth(weibo)
            #if not handleExcept:
            #    self.PostWeibo(weibo, entity, imageentity, handleExcept=False)
            return False
            
    def ClearImage(self):
        q = db.GqlQuery("SELECT * from ImageEntity")
        db.delete(q.fetch(200))

    def GetFlickrImages(self, flickr, userinfo):
        if userinfo.flickr_browse_type == "set":
            return self.GetFlickrImagesFromPhotoSet(flickr, userinfo)
        elif userinfo.flickr_browse_type == "tag":
            return self.GetFlickrImagesFromPhotoTag(flickr, userinfo, userinfo.flickr_browse_typename)
        else:
            return self.GetFlickrImagesFromPhotoStream(flickr, userinfo)
        
        
    def GetFlickrImagesFromPhotoStream(self, flickr, userinfo):
        list = self.GetFlickrImagesFromPhotoTag(flickr, userinfo, tags = None)
        return list
        
      
    def GetFlickrImagesFromPhotoSet(self, flickr, userinfo):
        list = []
        
        sets = flickr.photosets_getList(user_id=userinfo.flickr_id)       

        #这里每轮最多10张
        for photo in flickr.walk_set(photoset_id=userinfo.flickr_browse_setid, per_page='10'):
            photo_id = photo.attrib['id']
            title = photo.attrib['title']
            farm = photo.attrib['farm']
            server = photo.attrib['server']
            secret = photo.attrib['secret']
                        
            logging.info("get %s"% photo_id)
            self.response.out.write("get %s<br/>"% photo_id)
            photo = FlickrRecord.gql('WHERE photo_id=:1', photo_id).get()
            #photo = None
            if photo:
                logging.info("photo exist ")
                self.response.out.write("photo exist <br/>")
                continue
            url = "http://farm%s.staticflickr.com/%s/%s_%s.jpg"%(farm, server, photo_id, secret)
            link = "http://www.flickr.com/photos/%s/%s" % (userinfo.flickr_id, photo_id)

            e = FlickrRecord()
            e.photo_id = photo_id
            e.title = title
            e.url = url
            e.link = link
            list.append(e)
        return list
                
    
    def GetFlickrImagesFromPhotoTag(self, flickr, userinfo, tags):
        list = []
        #url = "http://api.flickr.com/services/feeds/photos_public.gne?id="+flickr_id+"&lang=en-us&format=rss_200"
        url = "http://api.flickr.com/services/feeds/photos_public.gne?id="+userinfo.flickr_id+"&lang=en-us&format=json" 
        if tags :
            url = url +"&tags="+tags
        #proxies = {'http': 'http://127.0.0.1:8580'}
        proxies={}
        feedinput = urllib.urlopen(url, proxies=proxies).read()
        p1 = feedinput.find("[")
        p2 = feedinput.rfind("]")
        feedinput1 = feedinput[p1: p2+1]  
        entries = json.loads(feedinput1)
        
        
        for entry in entries:
            title = entry["title"]
            url = entry["media"]['m'] 
            link = entry["link"]
            pos1 = link.rfind("/")
            pos2 = link.rfind("/",0,pos1-1)
            photo_id = link[pos2+1:pos1]
            photo_id = photo_id.strip()
            sd = entry["date_taken"]
            if sd[-6] == '-':
                sd = sd[0:-6]
            format = "%Y-%m-%dT%H:%M:%S"
            d = time.strptime(sd, format) 
            date_taken = datetime.fromtimestamp(mktime(d))
            current_time = datetime.now()
            delta = current_time - date_taken
            if delta> timedelta(days=userinfo.flickr_max_days):
                logging.info("%s: time exceed "%photo_id)
                self.response.out.write("time exceed exist %s <br/>"%photo_id)
                continue
                
            logging.info("%s"% photo_id)
            self.response.out.write("%s<br/>"% photo_id)
                
            photo = FlickrRecord.gql('WHERE photo_id=:1', photo_id).get()
            #photo = None
            if photo:
                logging.info("photo exist")
                self.response.out.write("photo exist <br/>")
                continue

            e = FlickrRecord()
            e.photo_id = photo_id
            e.title = title
            e.url = url
            e.link = link
            e.date = date_taken
            list.append(e)
        return list

        
    def get(self):
        #session = get_current_session()        
        #nickname = session.get("nickname", 0)
        #if not nickname:
        #    logging.info("not logged in")
        #    return
        #这里必须有nickname，否则不知道是谁
        nickname = self.request.get('nickname')
        userinfo = UserInfo.gql("WHERE nickname=:1", nickname).get()
        if not userinfo:
            logging.info("no userinfo found: %s",nickname)
            self.response.out.write("no userinfo found<br/>")
            return
            
        #此处不用认证，否则会加入很多未公开的图片的"
        flickr = auth.FlickrAuth(userinfo, no_token=True)
        if not flickr:             
            logging.info("flickr authentication failed")
            self.response.out.write("flickr authentication failed")
            return
        
        weibo = auth.WeiboAuth(userinfo)
        if not weibo:             
            logging.info("weibo authentication failed")
            self.response.out.write("weibo authentication failed")
            return
            
        #获得相片
        self.ClearImage()
        list = self.GetFlickrImages(flickr, userinfo)
        
        #获得位置需要认证
        flickr = auth.FlickrAuth(userinfo, no_token=False)
        if not flickr:             
            logging.info("flickr authentication failed")
            self.response.out.write("flickr authentication failed")
            return
        for e in list:
            location = None
            
            try:
                data = flickr.flickr_call(method='flickr.photos.geo.getLocation',  photo_id=e.photo_id, format='rest')
                
                l = flickr.parse_etree(data)
                location = l.find('photo/location')
            except FlickrError:
                logging.info( "%s has no location info."% (e.photo_id)) 
                self.response.out.write( "%s has no location info.<br/>"% (e.photo_id)) 
            

            if e.url[-6:] == "_m.jpg":
                e.url = e.url[:-5] + "b.jpg"
                url1 = "http://images0-focus-opensocial.googleusercontent.com/gadgets/proxy?container=focus&gadget=a&resize_h=500&url="+e.url                     
            else:
                url1 = e.url
            
            
            content = (urlfetch.fetch(url1)).content
            ie = ImageEntity()
            ie.url = e.url
            ie.url1 = url1
            ie.image = db.Blob(content)
            
            if location is not None:
                e.latitude = location.attrib['latitude']
                e.longitude = location.attrib['longitude']
                e.accuracy = location.attrib['accuracy']  

            if self.PostWeibo(weibo, e, ie) :
                e.put()
                ie.put()
        
        
        logging.info("sync ok")
        self.response.out.write("sync ok<br/>")
        
        
    
application = webapp2.WSGIApplication([
                                        ('/sync', FlickrListHandler)
                                     ],
                                     debug=True)  

def main():
    #util.run_wsgi_app(application)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()