#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from appsina import AppEngineSina
from google.appengine.ext import webapp


class WidgetTestCase(unittest.TestCase):

    def setUp(self):
        self.name=''
        self.pw=''
        self.app_key=''
        self.app_key_secret=''
        self.appenginesina = AppEngineSina(self.app_key,self.name,self.pw)
        
    def tearDown(self):
        self.appenginesina=dispose()
        self.appenginesina = None

    def base(self):
        print '>>>>>>>>>>>>>> show ststus <<<<<<<<<<<<<<<'
        print self.appenginesina.show_status(97272187)
        print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> update ststus <<<<<<<<<<<<<<<'
        #print 'Sending test:'+str(self.appenginesina.update_status('testing via appsina'))
        print '>>>>>>>>>>>>>> del ststus <<<<<<<<<<<<<<<'
        #print 'destroy test:'+str(self.appenginesina.del_status(97272187))
        print '>>>>>>>>>>>>>> repost ststus <<<<<<<<<<<<<<<'
        #print 'repost test:'+str(self.appenginesina.del_status(97272187,'test agin'))
        print '>>>>>>>>>>>>>> update comment <<<<<<<<<<<<<<<'
        #print 'update comment:'+str(self.appenginesina.update_comment(97272187,'test dfasasd'))
        print '>>>>>>>>>>>>>> del comment <<<<<<<<<<<<<<<'
        #print 'destroy comment:'+str(self.appenginesina.del_comment(86638082))
        print '>>>>>>>>>>>>>> public_timeline <<<<<<<<<<<<<<<'
        print self.appenginesina.public_timeline()
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> friends_timeline <<<<<<<<<<<<<<<'
        print self.appenginesina.friends_timeline()
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> user_timeline <<<<<<<<<<<<<<<'
        print self.appenginesina.user_timeline('kavin')
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> mentions <<<<<<<<<<<<<<<'
        #print self.appenginesina.mentions()
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> comments <<<<<<<<<<<<<<<'
        #print self.appenginesina.comments(count=3)
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> comments_by_me <<<<<<<<<<<<<<<'
        #print self.appenginesina.comments_by_me(page=2)
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> comments_for_status <<<<<<<<<<<<<<<'
        #print self.appenginesina.comments_for_status(96285565)
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> show user <<<<<<<<<<<<<<<'
        #print self.appenginesina.show_user('kavin')
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> show user friends <<<<<<<<<<<<<<<'
        #print self.appenginesina.friends('kavin')
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> show user followers <<<<<<<<<<<<<<<'
        #print self.appenginesina.followers('kavin')
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> DM Timeline <<<<<<<<<<<<<<<'
        #print self.appenginesina.direct_messages(count=3)
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> send DM Timeline <<<<<<<<<<<<<<<'
        #print self.appenginesina.send_direct_messages()
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> sent DM<<<<<<<<<<<<<<<'
        #print 'Sending DM...'+str(self.appenginesina.new_direct_messages('idella','ff'))
        print '>>>>>>>>>>>>>> del DM<<<<<<<<<<<<<<<'
        #print 'destroy DM...'+str(self.appenginesina.destroy_direct_messages(9929774))
        print '>>>>>>>>>>>>>> unfollow user <<<<<<<<<<<<<<<'
        #print 'unfollow user...'+str(self.appenginesina.unfollow_user('idella'))
        print '>>>>>>>>>>>>>> follow user <<<<<<<<<<<<<<<'
        #print 'follow user...'+str(self.appenginesina.follow_user('idella'))
        print '>>>>>>>>>>>>>> isfollow user <<<<<<<<<<<<<<<'
        #print 'isfollow idella?...'+str(self.appenginesina.isfollow_user('idella'))
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> friends_ids <<<<<<<<<<<<<<<'
        #print self.appenginesina.friends_ids('idella')
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> follower_ids <<<<<<<<<<<<<<<'
        #print self.appenginesina.followers_ids('idella')
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> verify credentials <<<<<<<<<<<<<<<'
        #print self.appenginesina.verify_credentials()
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> rate limit status <<<<<<<<<<<<<<<'
        #print self.appenginesina.rate_limit_status()
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> update profile <<<<<<<<<<<<<<<'
        #param={'description':'to know me is to code with me'}
        #print self.appenginesina.update_profile(param)
        print '>>>>>>>>>>>>>> favorites timeline <<<<<<<<<<<<<<<'
        #print self.appenginesina.favorites()
        #print self.appenginesina.getContent()
        print '>>>>>>>>>>>>>> add favorites  <<<<<<<<<<<<<<<'
        #print self.appenginesina.create_favorite(96540870)
        print '>>>>>>>>>>>>>> del favorites  <<<<<<<<<<<<<<<'
        #print self.appenginesina.destroy_favorite(96540870)
        
    def oauth(self):
        print '>>>>>>>>>>>>>> get oauth  <<<<<<<<<<<<<<<'
        
        self.appenginesina.set_oauth(key=self.app_key,
                                     secret=self.app_key_secret)
        # get request token
        dic=self.appenginesina.request_token()

        # set authorize and verifier request token
        # user have to give their username and passwork to verifier the account
        res=self.appenginesina.set_authorize(dic['oauth_token'],
                                             self.name,
                                             self.pw)
        # get access token and access token secret
        req_info = self.appenginesina.access_tokens(dic['oauth_token'],
                                                    dic['oauth_token_secret'],
                                                    res['oauth_verifier'])
        
        print 'oauth_verifier:'+res['oauth_verifier']
        print 'access token:'+req_info['oauth_token']
        print 'access token secret:'+req_info['oauth_token_secret']

        print '>>>>>>>>>>>>>> using oauth  <<<<<<<<<<<<<<<'
        self.appenginesina.set_oauth(key=self.app_key,
                                     secret=self.app_key_secret,
                                     acs_token=req_info['oauth_token'],
                                     acs_token_secret=req_info['oauth_token_secret'],
                                     oauth_verifier=res['oauth_verifier'])
        
        print '>>>>>>>>>>>>>> verify credentials <<<<<<<<<<<<<<<'
        print self.appenginesina.verify_credentials()
        print self.appenginesina.getContent()


def suite():
    suite = unittest.TestSuite()
    suite.addTest(WidgetTestCase("base"))
    suite.addTest(WidgetTestCase("oauth"))
    return suite


if __name__ == "__main__":
    unittest.main(defaultTest = 'suite')
