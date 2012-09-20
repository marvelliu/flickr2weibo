
from google.appengine.ext import db

class ImageEntity(db.Model):
    url = db.StringProperty(multiline=False)
    url1 = db.StringProperty(multiline=False)
    image = db.BlobProperty()
