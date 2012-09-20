
'''Persistent token cache management for the Flickr API'''

import os.path
import logging
import time
from google.appengine.ext import db
from tokenentity import TokenEntity

from flickrapi.exceptions import LockingError

logging.basicConfig()
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

__all__ = ('TokenCache', 'SimpleTokenCache')

class SimpleTokenCache(object):
    '''In-memory token cache.'''
    
    def __init__(self):
        self.token = None

    def forget(self):
        '''Removes the cached token'''

        self.token = None

class TokenCache(object):
    '''On-disk persistent token cache for a single application.
    
    The application is identified by the API key used. Per
    application multiple users are supported, with a single
    token per user.
    '''

    def getUsername(self):        
        if self.username:
            name = self.username
        else:
            name = "ur"
        return name
        
    def __init__(self, api_key, username=None):
        '''Creates a new token cache instance'''
        
        self.api_key = api_key
        self.username = username        
        self.memory = {}
        
    def get_cached_token(self):
        """Read and return a cached token, or None if not found.

        The token is read from the cached token file.
        """

        # Only read the token once
        if self.username in self.memory:
            return self.memory[self.username]
        
        name = self.getUsername()
        
        entities = TokenEntity.gql("WHERE username=:1",name)
        #entities = ""
        
        if not entities:
            return None
        for entity in entities:
            return entity.token.strip()
        return None
            
    def set_cached_token(self, token):
        """Cache a token for later use."""

        # Remember for later use
        self.memory[self.username] = token

        name = self.getUsername()
        
        entities = TokenEntity.gql("WHERE username:=", name)
        
        e = ""
        for entity in entities:
            e = entity
            break
        if not e:
            e = TokenEntity()
        print "eeeeeeeeee"
        e.apikey = self.api_key
        e.username = username
        e.token = token
        e.put()
        print "xxxxxxxxxxxxxxx"
        
    def forget(self):
        '''Removes the cached token'''
        
        if self.username in self.memory:
            del self.memory[self.username]
        
        name = self.getUsername()
        
        entities = TokenEntity.gql("WHERE username:=", name)
        
        for entity in entities:
            entity.delete()

    token = property(get_cached_token, set_cached_token, forget, "The cached token")
