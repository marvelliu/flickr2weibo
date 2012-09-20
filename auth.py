from flickrapi import FlickrAPI
from userinfo import UserInfo
from weibo import APIClient
from gaesessions import get_current_session
from config import *
from tokenentity import TokenEntity
import flickrapi
import logging


from weibopy.auth import OAuthHandler
from weibopy.api import API
from weibopy.error import WeibopError

def WeiboAuth(userinfo):
    if V2:
        return WeiboAuthV2(userinfo)
    else:
        return WeiboAuthV1(userinfo)
    
    
def WeiboAuthV1(userinfo):
    api = None
    try:    
        auth = OAuthHandler(WEIBO_APP_KEY, WEIBO_APP_SECRET)
        auth.setToken(userinfo.weibo_access_token, userinfo.weibo_access_token_secret)
        api = API(auth)        
    except Exception as e:
        logging.info( "WeiboAuth error %s "% e)
    return api
    
    
def WeiboAuthV2(userinfo):
    client = None
    try:
        client = APIClient(app_key=WEIBO_APP_KEY, app_secret=WEIBO_APP_SECRET, redirect_uri=WEIBO_CALLBACK_URL)
        if userinfo:
            client.set_access_token(userinfo.weibo_access_token, userinfo.weibo_expires_in)
    except Exception as e:
        logging.info( "WeiboAuth error %s "% e)
    return client
    
    
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
    
    