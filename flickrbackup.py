#!/usr/bin/python
import sys
import urllib2
import os
import flickrapi
from flickrapi import FlickrAPI
from flickrapi.tokencache import LockingTokenCache

ignore_sets=['childhood','2005','2006','2007','2008','2009','2010','ibmtc']
api_key = '5f419edc936dcdd3df18dab18f465984'
api_secret = 'a0d20c0286f7194d'

#userid='liuwenmao@ymail.com'
#userid='marvelliu'
userid='49635055@N02'
#flickr = flickrapi.FlickrAPI(api_key)

download_fold = "download"


def find_local_image(url, set_title, photo_title):
    global download_fold

#    if not os.path.exists(download_fold):
#        os.mkdir(outnewpath)
    outnewpath = download_fold+"/"+set_title
    if not os.path.exists(outnewpath):
        os.makedirs(outnewpath)

    ext = os.path.splitext(url)[1]
    filename = outnewpath +"/"+photo_title+ext
    
    if os.path.isfile(filename):
        return 1
    else:
        return -1

def download_image(url, set_title, photo_title):
    global download_fold

#    if not os.path.exists(download_fold):
#        os.mkdir(outnewpath)
    outnewpath = download_fold+"/"+set_title
    if not os.path.exists(outnewpath):
        os.makedirs(outnewpath)

    ext = os.path.splitext(url)[1]
    filename = outnewpath +"/"+photo_title+ext
    
    print url +"\t->\t" +filename
    
    re = urllib2.Request(url)
    rs = urllib2.urlopen(re).read()    
    open(filename, 'wb').write(rs)
    

def main(argv):
    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    (token, frob) = flickr.get_token_part_one(perms='write')
    if not token: raw_input("Press ENTER after you authorized this program")
    flickr.get_token_part_two((token, frob))
    
    flickr.token_cache = LockingTokenCache(api_key)
    
    #photos = flickr.photos_search(user_id=userid, per_page='10')
    #print photos
    sets = flickr.photosets_getList(user_id=userid)
    
    for set in sets.findall('photosets/photoset'):
        set_title = set.find('title').text
        set_description = set.find('description').text
        set_id = set.attrib['id']
        set_primary = set.attrib['primary']
        set_secret = set.attrib['secret']
        set_server = set.attrib['server']
        set_photos = set.attrib['photos']
        print "set title: %s\t description: %s\tid:%s, secret:%s" %(set_title, set_description, set_id, set_secret)
        
        if ignore_sets.count(set_title)>0:
            print "ignore"
            continue
    
        #for photo in flickr.walk_set(photoset_id=id):
        for photo in flickr.walk_set(photoset_id=set_id, per_page='10'):
            photo_id = photo.attrib['id']
            photo_title = photo.attrib['title']
            photo_secret = photo.attrib['secret']
            
            source = "/"+photo_title+".jpg"
            print "\ttitle: %s\t id:%s\t secret:%s\t" %(photo_title, photo_id, photo_secret),
            if find_local_image(source, set_title, photo_title) >0 :
                print ""
                continue
            data = flickr.flickr_call(method='flickr.photos.getSizes',  photo_id=photo_id, format='rest')
            sizes = flickr.parse_etree(data)
            for size in sizes.findall('sizes/size'):
                if size.attrib['label'] == 'Original':
                    source = size.attrib['source']
                    download_image(source, set_title, photo_title);
            #break
        #break
    
    
if __name__ == "__main__": sys.exit(main(sys.argv))    
