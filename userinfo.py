
from google.appengine.ext import db

class UserInfo(db.Model):
    nickname = db.StringProperty(multiline=False)
    password = db.StringProperty(multiline=False)
    flickr_id = db.StringProperty(multiline=False)
    flickr_api_key = db.StringProperty(multiline=False)
    flickr_api_secret = db.StringProperty(multiline=False)
    flickr_browse_type = db.StringProperty( choices=set(["stream", "set", "tag"]))
    flickr_browse_typename = db.StringProperty(multiline=False)
    flickr_browse_setid = db.IntegerProperty()
    flickr_max_days = db.IntegerProperty(default=40)
    weibo_id = db.StringProperty(multiline=False)
    weibo_access_token = db.StringProperty(multiline=False)
    weibo_expires_in = db.IntegerProperty()
    weibo_access_token_secret = db.StringProperty(multiline=False)
    weibo_avatar = db.StringProperty(multiline=False)
    
    