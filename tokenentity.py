
from google.appengine.ext import db

class TokenEntity(db.Model):
    username = db.StringProperty(multiline=False)
    token = db.StringProperty(multiline=False)
    