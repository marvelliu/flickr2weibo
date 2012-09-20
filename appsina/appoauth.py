#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# AppEngine-OAuth
# http://code.google.com/p/appsina/
#
# Base on AppEngine-OAuth:
# ttp://0-oo.net/sbox/python-box/appengine-oauth
#
# Modified by Kavin Gray.
# Support Oauth version 1.0a
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

'''OAuth utility for applications on Google App Engine'''

__author__ = 'grayseason@gmail.com'
__version__ = '0.0.1'
 
 
import hmac
import urllib,urllib2
from google.appengine.api import urlfetch
from hashlib import sha1
from random import getrandbits
from time import time
from django.utils import simplejson 
 
class AppEngineOAuth(object):
 
  def __init__(self,
               key,
               secret,
               acs_token='',
               acs_token_secret='',
               oauth_verifier=''):
    
    self._key = key
    self._secret = secret
    self._token = acs_token
    self._token_secret = acs_token_secret
    self._oauth_verifier = oauth_verifier
 
    # Be understandable which type token is (request or access)
    if acs_token == '':
      self._token_type = None
    else:
      self._token_type = 'access'


 
  def request_token(self, req_token_url):
    '''
    Return request_token, request_token_secret
    '''
    # Get request token
    params = self.get_oauth_params(req_token_url, {})
    res = urlfetch.fetch(url=req_token_url + '?' + urllib.urlencode(params),
                         method='GET')
    self.last_response = res
    if res.status_code != 200:
      raise Exception('OAuth Request Token Error: ' + res.content)
    # Response content is request_token
    dic = self._qs2dict(res.content)
    self._token = dic['oauth_token']
    self._token_secret = dic['oauth_token_secret']
    self._token_type = 'request'
    
    return dic


    
  def set_authorize(self,
                    au_token_url ,
                    req_token,
                    userId ,
                    pw ):
    '''
    Verifier request token
    Return request_token, oauth_verifier.
    '''    
    # Get request token
    self._oauth_callback = urllib2.quote('json')
    self._token = req_token
    au_params={'oauth_token':self._token,
               'oauth_callback':self._oauth_callback,
               'userId': userId,
               'passwd': pw } 
    res = urlfetch.fetch(url=au_token_url + '?' + urllib.urlencode(au_params),
                         method='GET')
    self.last_response = res
    if res.status_code != 200:
      raise Exception('OAuth Request Token Error: ' + res.content)
    # Response content is request_token and oauth_verifier
    respon=simplejson.loads(res.content)
    self._oauth_verifier=respon['oauth_verifier']
 
    return respon
 
 
  def access_tokens(self,
                    acs_token_url,
                    req_token,
                    req_token_secret ,
                    oauth_verifier):
    # Get access token
    self._token = req_token
    self._token_secret = req_token_secret
    self._token_type = 'request'
    acs_params = urllib.urlencode(self.get_oauth_params(acs_token_url, {}))  
    res = urlfetch.fetch(url=acs_token_url + '?' + acs_params,
                         method='GET')
    self.last_response = res
    if res.status_code != 200:
      raise Exception('OAuth Access Token Error: ' + res.content)
    # Response content is access_token
    access_dic = self._qs2dict(res.content)
    self._token = access_dic['oauth_token']
    self._token_secret = access_dic['oauth_token_secret']
    self._token_type = 'access'
 
    return access_dic
 
 
  def get_oauth_params(self, url, params, method='GET'):
    oauth_params = {'oauth_consumer_key': self._key,
                    'oauth_signature_method': 'HMAC-SHA1',
                    'oauth_timestamp': int(time()),
                    'oauth_nonce': str(getrandbits(64)),
                    #'oauth_version': '1.0',
                    }
    if self._token_type != None:
      oauth_params['oauth_token'] = self._token
      oauth_params['oauth_verifier'] = self._oauth_verifier
 
    # Add other params
    params.update(oauth_params)
 
    # Sort and concat
    s = ''
    for k in sorted(params):
      s += self._quote(k) + '=' + self._quote(params[k]) + '&'
    msg = method + '&' + self._quote(url) + '&' + self._quote(s[:-1])
 
    # Maybe token_secret is empty
    key = self._secret + '&' + self._token_secret
 
    digest = hmac.new(key, msg, sha1).digest()
    params['oauth_signature'] = digest.encode('base64')[:-1]

    return params
 
 
  def _quote(self, s):
    return urllib.quote(str(s), '~')
 
 
  def _qs2dict(self, s):
    dic = {}  
    for param in s.split('&'):
      (key, value) = param.split('=')
      dic[key] = value
    return dic
