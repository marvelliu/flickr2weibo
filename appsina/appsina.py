#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# AppEngineSina
# http://code.google.com/p/appsina/
#
# Base on AppEngineTwitter:
# http://0-oo.net/sbox/python-box/appengine-twitter
#
# Modified by Kavin Gray
#
# Licensed under the MIT license;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.opensource.org/licenses/mit-license.php
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

'''Sina weibo API wrapper for applications on Google App Engine'''

__author__ = 'grayseason@gmail.com'
__version__ = '0.0.1'


import base64
import urllib,urllib2,re
from django.utils import simplejson
from appoauth import AppEngineOAuth
from google.appengine.api import urlfetch
 
 
class AppEngineSina(object):
  
  def __init__(self, key , name='', pswd=''):
    '''
    Note: Some actions require password or OAuth.
    '''
    self._api_url = 'http://api.t.sina.com.cn'
    self._name = name
    self._app_key = key
    self._oauth = None
    self._content = None
    self._headers = {}
    if pswd != '':
      auth = base64.encodestring(name + ':' + pswd)[:-1]
      self._headers['Authorization'] = 'Basic ' + auth



  def getContent(self):
    '''
    return the content
    '''
    return self._content
  

  

  # ========= Status Methods ===========

  
  def show_status(self, id):
    '''
    Returns a single status, specified by the id parameter below.
    The status's author will be returned inline.
    Sucess => Retrun 200 status and set response to self.content/
    Fialed => Return other HTTP status
    '''
    status =self._get('/statuses/show/id.json',
                      {'id': id,
                       'source':self._app_key})
    if(status==200):
      self._content=self.last_response.content
    return status



  def update_status(self,
                    status,
                    lat=0,
                    long=0):
    '''
    Post a msg
    Sucess => Retrun 200
    Fialed => Return other HTTP status
    '''
    status=urllib2.quote(status)
    return self._post('/statuses/update.json',
                      {'status': status,
                       'lat': lat,
                       'long': long,
                       'source':self._app_key})



  def del_status(self,id):
    '''
    Destroy a msg
    Sucess => Retrun 200
    Fialed => Return other HTTP status
    '''        
    return self._post('/statuses/destroy/id.json',
                      {'id': id,
                       'source':self._app_key})



  def rt_status(self,
                id,
                status=''):
    '''
    Repost a msg
    Sucess => Retrun 200
    Fialed => Return other HTTP status
    '''
    status=urllib2.quote(status)
    return self._post('/statuses/repost.json',
                      {'id': id,
                       'status': status,
                       'source':self._app_key})


  
  def update_comment(self,
                     id,
                     comment,
                     cid=0):
    '''
    Post a comment
    Sucess => Retrun 200
    Fialed => Return other HTTP status
    '''
    comment=urllib2.quote(comment)
    return self._post('/statuses/comment.json',
                      {'id': id,
                       'comment': comment,
                       'cid':cid,
                       'source':self._app_key})


  
  def del_comment(self,id):
    '''
    Destroy a comment
    Sucess => Retrun 200
    Fialed => Return other HTTP status
    '''        
    return self._post('/statuses/comment_destroy/id.json',
                      {'id': id,
                       'source':self._app_key})



  def reply_comment(self,
                    id,
                    cid,
                    comment):
    '''
    Reply a comment
    Sucess => Retrun 200
    Fialed => Return other HTTP status
    '''
    comment=urllib2.quote(comment)
    return self._post('/statuses/reply.json',
                      {'id': id,
                       'cid':cid,
                       'comment':comment,
                       'source':self._app_key})




  # ========= Timeline Methods =========

  
  def public_timeline(self):
    '''
    get and save public Timeline  
    Sucess => Retrun 200 status and set response to self.content/
    Fialed => Return error HTTP status
    '''
    status = self._get('/statuses/public_timeline.json', {'source':self._app_key})
    if(status==200):
      self._content=self.last_response.content
    return status

  
  
  def friends_timeline(self,
                       since_id=0,
                       max_id=0,
                       count=20,
                       page=1):
    '''
    get and save friends Timeline  
    Sucess => Retrun 200 status and set response to self.content/
    Fialed => Return error HTTP status
    '''
    status = self._get('/statuses/friends_timeline.json',
                       {'since_id':since_id,
                        'max_id':max_id,
                        'count':count,
                        'page':page,
                        'source':self._app_key})
    if(status==200):
      self._content=self.last_response.content
    return status

  

  def user_timeline(self,
                    id,
                    screen_name='',
                    user_id=0,
                    since_id=0,
                    max_id=0,
                    count=20,
                    page=1):
    '''
    get and save user Timeline  
    Sucess => Retrun 200 status and set response to self.content/
    Fialed => Return error HTTP status
    '''
    status = self._get('/statuses/user_timeline.json',
                       {'id':id,
                        'user_id':user_id,
                        'screen_name':screen_name,
                        'since_id':since_id,
                        'max_id':max_id,
                        'count':count,
                        'page':page,
                        'source':self._app_key})
    if(status==200):
      self._content=self.last_response.content
    return status



  def mentions(self,
               since_id=0,
               max_id=0,
               count=20,
               page=1):
    '''
    get and save Mention timeline
    Sucess => Retrun 200 status and set response to self.content/
    Fialed => Return error HTTP status
    '''  
    status = self._get('/statuses/mentions.json',
                       {'since_id':since_id,
                        'max_id':max_id,
                        'count':count,
                        'page':page,
                        'source':self._app_key})      
    if(status==200):
      self._content=self.last_response.content
    return status



  def comments(self,
               since_id=0,
               max_id=0,
               count=20,
               page=1):
    '''
    get and save comments timeline
    Sucess => Retrun 200 status and set response to self.content/
    Fialed => Return error HTTP status
    '''  
    status = self._get('/statuses/comments_timeline.json',
                       {'since_id':since_id,
                        'max_id':max_id,
                        'count':count,
                        'page':page,
                        'source':self._app_key})      
    if(status==200):
      self._content=self.last_response.content
    return status



  def comments_by_me(self,
                     since_id=0,
                     max_id=0,
                     count=20,
                     page=1):
    '''
    get and save comments timeline by me
    Sucess => Retrun 200 status and set response to self.content/
    Fialed => Return error HTTP status
    '''  
    status = self._get('/statuses/comments_by_me.json',
                       {'since_id':since_id,
                        'max_id':max_id,
                        'count':count,
                        'page':page,
                        'source':self._app_key})      
    if(status==200):
      self._content=self.last_response.content
    return status



  def comments_for_status(self,
                          id,
                          count=20,
                          page=1):
    '''
    get and save comments for status 
    Sucess => Retrun 200 status and set response to self.content/
    Fialed => Return error HTTP status
    '''  
    status = self._get('/statuses/comments.json',
                       {'id':id,
                        'count':count,
                        'page':page,
                        'source':self._app_key})      
    if(status==200):
      self._content=self.last_response.content
    return status



  # ========= User Methods =========


  def show_user(self,
                id,
                user_id=0,
                screen_name=''):
    '''
    Get and save user info
    Sucess => Retrun 200 status and set content to self._content
    Fialed => Return error HTTP status
    '''
    status = self._get('/users/show.json',
                       {'id':id,
                        'user_id':user_id,
                        'screen_name':screen_name,
                        'source':self._app_key})      
    if(status==200):
      self._content=self.last_response.content
    return status



  def friends(self,
              id,
              user_id=0,
              screen_name='',
              cursor=-1,
              count=20):
    '''
    Get and save friends from user
    Sucess => Retrun 200 status and set content to self._content
    Fialed => Return error HTTP status
    '''
    status = self._get('/statuses/friends.json',
                       {'id':id,
                        'user_id':user_id,
                        'screen_name':screen_name,
                        'cursor':cursor,
                        'count':count,
                        'source':self._app_key})      
    if(status==200):
      self._content=self.last_response.content
    return status



  def followers(self,
                id,
                user_id=0,
                screen_name='',
                cursor=-1,
                count=20):
    '''
    Get and save followers from user
    Sucess => Retrun 200 status and set content to self._content
    Fialed => Return error HTTP status
    '''
    status = self._get('/statuses/followers.json',
                       {'id':id,
                        'user_id':user_id,
                        'screen_name':screen_name,
                        'cursor':cursor,
                        'count':count,
                        'source':self._app_key})      
    if(status==200):
      self._content=self.last_response.content
    return status 


  
  # ========= Direct Message Methods =========

  
  def direct_messages(self,
                      since_id=0,                      
                      max_id=0,
                      count=20,
                      page=1):
    '''
    get and save Direct Messages timeline
    Sucess => Retrun 200 status and set content to self._content
    Fialed => Return other HTTP status
    '''
    status = self._get('/direct_messages.json',
                       {'since_id':since_id,
                        'max_id':max_id,
                        'count':count,
                        'page':page,
                        'source':self._app_key})
    if(status==200):
      self._content=self.last_response.content
    return status



  def send_direct_messages(self,
                           since_id=0,
                           max_id=0,
                           count=20,
                           page=1):
    '''
    get and save direct messages timeline you have send
    Sucess => Retrun 200 status and set content to self._content
    Fialed => Return other HTTP status
    '''
    status = self._get('/direct_messages/sent.json',
                       {'since_id':since_id,
                        'max_id':max_id,
                        'count':count,
                        'page':page,
                        'source':self._app_key})
    if(status==200):
      self._content=self.last_response.content
    return status
  


  def new_direct_messages(self,
                          screen_name,
                          text,
                          user_id=0):
    '''
    Sent a Direct Messages
    Sucess => Retrun 200
    Fialed => Return other HTTP status
    '''
    text=urllib2.quote(text)
    return self._post('/direct_messages/new.json',
                      {'user_id':user_id,
                       'screen_name':screen_name,
                       'text':text,
                       'source':self._app_key})


 
  def destroy_direct_messages(self,id):
    '''
    Destroy a Direct Messages
    Sucess => Retrun 200
    Fialed => Return other HTTP status
    '''
    return self._post('/direct_messages/destroy/id.json',
                      {'id':id,
                       'source':self._app_key})



 
  # ========= Friendships methods =========

  
  def follow_user(self,
                  id,
                  user_id=0,
                  screen_name=''):
    '''
    Follow user
    Sucess => Retrun 200
    Fialed => Return other HTTP status
    '''
    return self._post('/friendships/create/id.json',
                      {'id':id,
                       'user_id':user_id,
                       'screen_name':screen_name,
                       'source':self._app_key})



  def unfollow_user(self,
                    id,
                    user_id=0,
                    screen_name=''):
    '''
    Unfollow user
    Sucess => Retrun 200
    Fialed => Return other HTTP status
    '''
    return self._post('/friendships/destroy/id.json',
                      {'id':id,
                       'user_id':user_id,
                       'screen_name':screen_name,
                       'source':self._app_key})



  def isfollow_user(self,
                    target_screen_name,
                    target_id=0,
                    source_screen_name='',
                    source_id=0):
    '''
    the existence of friendship between two users
    Sucess => Retrun 200 status and set content to self._content
    Fialed => Return other HTTP status
    '''
    param={'target_id':target_id,
           'target_screen_name':target_screen_name,
           'source':self._app_key}
    
    if(source_id<>0 or source_screen_name<>''):
      param['source_id']=source_id
      param['source_screen_name']=source_screen_name
      
    status = self._get('/friendships/show.json',param)
    if(status==200):
      self._content=self.last_response.content
    return status

  


  # =========  Social Graph methods ===========


  def friends_ids(self,
                  id,
                  user_id=0,
                  screen_name='',
                  cursor=-1,
                  count=20):
    '''
    Get and save a list of id from the target user's frineds
    Sucess => Retrun 200 status and set content to self._content
    Fialed => Return other HTTP status
    '''
    status = self._get('/friends/ids.json',
                       {'id':id,
                        'user_id':user_id,
                        'screen_name':screen_name,
                        'cursor':cursor,
                        'count':count,
                        'source':self._app_key})
    if(status==200):
      self._content=self.last_response.content
    return status
    


  def followers_ids(self,
                    id,
                    user_id=0,
                    screen_name='',
                    cursor=-1,
                    count=20):
    '''
    Get and save a list of id from the target user's followers
    Sucess => Retrun 200 status and set content to self._content
    Fialed => Return other HTTP status
    '''
    status = self._get('/followers/ids.json',
                       {'id':id,
                        'user_id':user_id,
                        'screen_name':screen_name,
                        'cursor':cursor,
                        'count':count,
                        'source':self._app_key})
    if(status==200):
      self._content=self.last_response.content
    return status



  # =========  Account methods  ==========


  def verify_credentials(self):
    '''
    Verify Credentials and save info
    Sucess => Retrun 200 status and set content to self._content
    Fialed => Return other HTTP status
    '''
    status = self._get('/account/verify_credentials.json', {'source':self._app_key})
    if(status==200):
      self._content=self.last_response.content
    return status



  def rate_limit_status(self):
    '''
    Get and save rate limit status
    Sucess => Retrun 200 status and set content to self._content
    Fialed => Return other HTTP status
    '''
    status = self._get('/account/rate_limit_status.json', {'source':self._app_key})
    if(status==200):
      self._content=self.last_response.content
    return status



  def end_session(self):
    '''
    End session of the user
    Sucess => Retrun 200 
    Fialed => Return other HTTP status
    '''
    return self._post('/account/end_session.json', {'source':self._app_key})



  def register(self,
               nick,
               gender,
               password,
               email):
    '''
    Register a new account
    Sucess => Retrun 200 
    Fialed => Return other HTTP status
    '''     
    return self._post('/account/register.json',
                      {'nick':nick,
                       'gender':gender,
                       'password':password,
                       'email':email,
                       'source':self._app_key})



  def update_profile(self, param):
    '''
    param is a dict with the following key:
    name, gender, province, city, description
    Sucess => Retrun 200 
    Fialed => Return other HTTP status
    '''
    param['source']=self._app_key
    return self._post('/account/update_profile.json',param)




  # =========  Favorites methods  =========


  def favorites(self, page=1):
    '''
    Get and save favorites timeline
    Sucess => Retrun 200 status and set content to self._content
    Fialed => Return other HTTP status
    '''    
    status = self._get('/favorites.json',
                       {'page':page,
                        'source':self._app_key})
    if(status==200):
      self._content=self.last_response.content
    return status



  def create_favorite(self,id):
    '''
    Create favorite
    Sucess => Retrun 200 
    Fialed => Return other HTTP status
    '''  
    return self._post('/favorites/create.json',
                      {'id':id,
                       'source':self._app_key})
   

    
  def destroy_favorite(self,id):
    '''
    Destroy favorite
    Sucess => Retrun 200 
    Fialed => Return other HTTP status
    '''  
    return self._post('/favorites/destroy/id.json',
                      {'id':id,
                       'source':self._app_key})


  # =========  OAuth methods ==========


  def set_oauth(self,
                key,
                secret,
                acs_token='',
                acs_token_secret='',
                oauth_verifier=''):
    '''
    Set OAuth parameters
    '''
    self._oauth = AppEngineOAuth(key,
                                 secret,
                                 acs_token,
                                 acs_token_secret,
                                 oauth_verifier)


 
  def request_token(self):
    '''
    Get request token, request token secret
    '''
    dic = self._oauth.request_token(self._api_url + '/oauth/request_token')
    return dic


    
  def set_authorize(self,
                    req_token,
                    userId,
                    pw):
    '''
    Verifier request token
    Return request_token, oauth_verifier.
    '''
    res  = self._oauth.set_authorize(self._api_url + '/oauth/authorize',
                                     req_token,
                                     userId,
                                     pw)
    return res 


    
 
  def access_tokens(self,
                    req_token,
                    req_token_secret,
                    oauth_verifier):
    '''
    Exchange request token for access token
    '''
    return self._oauth.access_tokens(self._api_url + '/oauth/access_token',
                                     req_token,
                                     req_token_secret,
                                     oauth_verifier)




  # =========  Private methods  =========  

 
  def _post(self, path, params):
    url = self._api_url + path
    if self._oauth != None:
      params = self._oauth.get_oauth_params(url, params, 'POST')    
    res = urlfetch.fetch(url=url,
                         payload=urllib.urlencode(params),
                         method='POST',
                         headers=self._headers)
    self.last_response = res
    return res.status_code


    
  def _get(self, path, params):
    url = self._api_url + path
    if self._oauth != None:
      params = self._oauth.get_oauth_params(url, params, 'GET')
    url += '?' + urllib.urlencode(params)
    res = urlfetch.fetch(url=url, method='GET', headers=self._headers)
    self.last_response = res
    return res.status_code


