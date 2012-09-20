from flickrapi import FlickrAPI
from userinfo import UserInfo
from weibo import APIClient
from gaesessions import get_current_session
from config import *
from tokenentity import TokenEntity
import flickrapi
import logging

def WeiboReauth(weibo):
    client = None
    try:
        client = auth.WeiboAuth(None)
        weibo_auth_url = client.get_authorize_url()        
        socket = urllib.urlopen(weibo_auth_url)
        reply = socket.read()
        socket.close()        
        logging.info( "reply: %s"% (reply))
        #puts("reply %s<br/>"% reply)
    except Exception as e:
        logging.info( "WeiboAuth error %s "% e)
    return client
        
#def WeiboAuth(userinfo):
    #client = None
    #try:
    #    client = APIClient(app_key=WEIBO_APP_KEY, app_secret=WEIBO_APP_SECRET, redirect_uri=WEIBO_CALLBACK_URL)
    #    if userinfo:
    #        client.set_access_token(userinfo.weibo_access_token, userinfo.weibo_expires_in)
    #except Exception as e:
    #    logging.info( "WeiboAuth error %s "% e)
    #return client
    
def FlickrAuth(userinfo, no_token = False):
    flickr = None
    try:
        flickr_api_key = userinfo.flickr_api_key
        
        if no_token :
            return flickrapi.FlickrAPI(flickr_api_key)
        flickr_api_secret = userinfo.flickr_api_secret
                
        flickr_token = GetFlickrToken(userinfo.nickname)
        if not flickr_token: 
            logging.info( "no flickr_token in database, visit /setting first")             
            return None
        flickr = flickrapi.FlickrAPI(flickr_api_key, flickr_api_secret, token=flickr_token)
    except Exception as e:
        logging.info( "FlickrAuth error %s "% e)
    return flickr
    
def GetFlickrToken(nickname):
    t = TokenEntity.gql("WHERE username=:1", nickname).get()
    if t:
        return t.token
    return None
    
def GetFlickrLoginUrl(userinfo):
    flickr_api_key = userinfo.flickr_api_key
    flickr_api_secret = userinfo.flickr_api_secret
    flickr = flickrapi.FlickrAPI(
                flickr_api_key, 
                flickr_api_secret)
    url = flickr.web_login_url('read')	
    return url
    
    