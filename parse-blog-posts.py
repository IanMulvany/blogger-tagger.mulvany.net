#!/usr/bin/python
"""
parse-blogs.py

get the contents of a blog and parse it for the presence of predefined tags

"""

import sys
from optparse import OptionParser, OptionGroup
import cPickle
from BeautifulSoup import BeautifulSoup 
import re
from gdata import service
import sys
import gdata
import atom
import feedparser

def GetBlogFeed(blogger_service):
    query = service.Query()
    query.feed = "/feeds/default/blogs"
    feed = blogger_service.Get(query.ToUri())
    return feed

def GetBlogIdZillertal(feed):
    blog_id = feed.entry[0].GetSelfLink().href.split("/")[-1]
    return blog_id

def GetBlogIdPA(feed):
    blog_id = feed.entry[1].GetSelfLink().href.split("/")[-1]
    return blog_id

def AuthenticateSession(username,password):
    blogger_service = service.GDataService(username,password)
    blogger_service.source = 'mulvanynet-BloggerTagger-1.0'
    blogger_service.service = 'blogger'
    blogger_service.server = 'www.blogger.com'
    blogger_service.ProgrammaticLogin()
    return blogger_service

def get_feed_data(feed,feed_file):
    # ask the server to tell us the status of the feed
    # based on etag
    d = retrieve_data(feed_file)
    return d

def gen_local_filename_from_feedname(dirname,feed):
    feed_bits = feed.replace("/",'')
    feed_bits2 = feed_bits.replace(":",'')
    # fileroot = feed_bits[-2]
    filename = dirname + feed_bits2 + ".pkl"
    return filename

def retrieve_data(filename):
    # if the file exists unpickle and return the pickled object
    f = open(filename,'r')
    ob = cPickle.load(f)
    f.close
    # otherwise return an empty object
    return ob 
    
# feeds = ["http://partiallyattended.vox.com/library/posts/2007/07/atom-full.xml",
#        "http://partiallyattended.vox.com/library/posts/2007/08/atom-full.xml",
#        "http://partiallyattended.vox.com/library/posts/2007/08/page/2/atom-full.xml",
#        "http://partiallyattended.vox.com/library/posts/2007/09/atom-full.xml",
#        "http://partiallyattended.vox.com/library/posts/2007/10/atom-full.xml",
#        "http://partiallyattended.vox.com/library/posts/2007/11/atom-full.xml",
#        "http://partiallyattended.vox.com/library/posts/2007/12/atom-full.xml",
#        "http://partiallyattended.vox.com/library/posts/2008/01/atom-full.xml",
#        "http://partiallyattended.vox.com/library/posts/2008/02/atom-full.xml",
#        "http://partiallyattended.vox.com/library/posts/2008/02/page/2/atom-full.xml",
#        "http://partiallyattended.vox.com/library/posts/2008/03/atom-full.xml",
#        "http://partiallyattended.vox.com/library/posts/2008/04/atom-full.xml",
#        "http://partiallyattended.vox.com/library/posts/2008/05/atom-full.xml",
#        "http://partiallyattended.vox.com/library/posts/2008/06/atom-full.xml",
#        "http://partiallyattended.vox.com/library/posts/2008/07/atom-full.xml"]


feeds = ["http://partiallyattended.vox.com/library/posts/2008/06/atom-full.xml"]
dirname = "/Users/ian/Documents/p/partiallyattended/posts/"

def unpackLocalFeeds(dirname,feeds):
    for feed in feeds:
        filename = gen_local_filename_from_feedname(dirname,feed)
        data = retrieve_data(filename)
        print data
        

ontology = ['netsci','netsci08','wedding','mac','climbing','bouldering','ireland',
                    'germany','london','nature','npg','science','cambridge','munich','barcamp','barcamb',
                        'avatar','mac','osx','python','perl','travel','weight','network','lhc','web','blog','food','dinner','restaurant',
                        'picture','iphone','flickr','twitter','math','mathematics','facebook','rss','ikea','cool','presentation','talk','book','books','blogging']

def ParsePostForTags(post):
    pattern = "(tags:)([0-9a-z,\s\.]*)"
    tag_string =  re.compile(pattern).findall(post)
    try:
        #print tag_string
        #print tag_string[0][1]
        tags = tag_string[0][1].split(',')
        #print tags
    except:
        tags = []
    return tags

def CheckPostAgainstPersonalOntology(post,title,ontology):
    match_tags = []
    for tag in ontology:            
        if searchContent.find(tag) > -1 or ltitle.find(tag) >-1:
            if tag not in match_tags:
                match_tags.append(tag)
    return match_tags

def CreatePublicPost(blogger_service, p_blog_id, title, content, tags, published, updated):
    entry = gdata.GDataEntry()
    #entry.published = atom.Published(published)
    #entry.updated = atom.Updated(updated)
    entry.title = atom.Title('xhtml', title)
    entry.content = atom.Content(content_type='html', text=content)
    labels = []
    if len(tags) > 0:
        for tag in tags:
            cat = atom.Category()
            cat = atom.Category()
            cat.scheme = "http://www.blogger.com/atom/ns#"
            cat.term = tag
            labels.append(cat)
        #entry.category = labels
    print entry
    return blogger_service.Post(entry, '/feeds/%s/posts/default' % p_blog_id)

def upload_feeds(feeds):
    for feed in feeds:
        # get the local filename
        filename = gen_local_filename_from_feedname(dirname,feed)
        # get the data from either a file or the server dependent on status
        d = get_feed_data(feed,filename)
        entries = d.entries
        for entry in entries:
            title = entry['title']
            published =  entry['published']
            updated =  entry['updated']
            content = entry['content'][0]['value']
    
            #print title
            #print published
            #print updated
            
            nobrContent = content.replace('<br />','')
            nobrnonewlineContent = nobrContent.replace('\n','')
            NobrNonewlineNobarContent = nobrnonewlineContent.replace('|','')
            soup = BeautifulSoup(NobrNonewlineNobarContent)
            links = soup.findAll('a')
            voxLinks = links[-2:]
            for link in voxLinks:
                link.extract()
            #print soup
            # print NobrNonewlineNobarContent
            # print NobrNonewlineNobarContent.encode('ascii','replace')
            # now we have a cleaned up content, we could post this to blogger, but I would like
            # to extract the tags now
            uContent = unicode(soup)
            searchContent = uContent.lower()
            ltitle = title.lower()
            o_tags = CheckPostAgainstPersonalOntology(searchContent,ltitle,ontology)
            e_tags = ParsePostForTags(searchContent)
            a_tags = []
            for tag in o_tags:
                if tag not in e_tags:
                    e_tags.append(tag)
            #print title
            #print e_tags
            #if len(match_tags) > 0:
            #    print title
            #    print match_tags
            #    print ''
            #print title
            
            uContent1 = uContent.replace('&lt;','<')
            uContent2 = uContent1.replace('&gt;','>')
            
            
            print 'creating new entry on blogger: ', title


def tmp()
    print 'getting blogger access'
    # get access to blogger version of partially attended
    username = 'username'
    password = 'password'
    blogger_service = AuthenticateSession(username,password)
    feed = GetBlogFeed(blogger_service)
    # z_blog_id = GetBlogIdZillertal(feed)
    # p_blog_id = GetBlogIdPA(feed)
    # print z_blog_id
    # print p_blog_id
    #2170806040461107001 is the id of partially attended.
    
    p_blog_id = '2170806040461107001'
    z_blog_id = '3839011616568869093'
    
    title = 'test'
    published = ''
    updated = ''
    uContent2 = 'this is a test piece of content'
    e_tags = []
    CreatePublicPost(blogger_service, p_blog_id, title, uContent2, e_tags, published, updated)
        
def main():
    feeds = ["http://partiallyattended.vox.com/library/posts/2008/06/atom-full.xml"]
    dirname = "/Users/ian/Documents/p/partiallyattended/posts/"
    unpackLocalFeeds(dirname,feeds)
    
    
if __name__ == "__main__":
    main()
        
    
if __name__ == "__main__":
    main()

