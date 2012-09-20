
from google.appengine.ext import db

class FlickrRecord(db.Model):
    photo_id = db.StringProperty(multiline=False)
    title = db.StringProperty(multiline=False)
    url = db.StringProperty(multiline=False)
    latitude = db.StringProperty(multiline=False)
    longitude = db.StringProperty(multiline=False)
    accuracy = db.StringProperty(multiline=False)
    #width = db.StringProperty(multiline=False)
    #height = db.StringProperty(multiline=False)
    date = db.DateTimeProperty()