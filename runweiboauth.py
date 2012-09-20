
from weibopy.auth import OAuthHandler
from weibopy.api import API
from urllib2 import urlopen, URLError, HTTPError
from json import load
import sys, os
import codecs
from config import *


def WeiboAuthV1():
    auth = OAuthHandler(WEIBO_APP_KEY, WEIBO_APP_SECRET)
    auth_url = auth.get_authorization_url()
    print ''
    print '请在浏览器中访问下面链接，授权给buzz2weibo后，会获得一个授权码。'
    print ''
    print auth_url
    print ''

    while True:
        verifier = raw_input('请输入授权码：').strip()
        try:
            token = auth.get_access_token(verifier)
        except HTTPError:
            print '授权码不正确或者过期，请重新运行本向导'
            sys.exit(1)
        else:
            break

    weibo_token_key = token.key
    weibo_token_secret = token.secret
    
    
    
def main():
    #util.run_wsgi_app(application)
    WeiboAuthV1()


if __name__ == '__main__':
    main()