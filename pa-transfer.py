# the aim of this script to to transfer content from
# my vox site to my google hosted blog

import sys
from optparse import OptionParser, OptionGroup

from gdata import service
import sys
import gdata
import atom
import feedparser

def AuthenticateSession(username,password):
     blogger_service = service.GDataService(username,password)
     blogger_service.source = 'mulvanynet-BloggerTagger-1.0'
     blogger_service.service = 'blogger'
     blogger_service.server = 'www.blogger.com'
     blogger_service.ProgrammaticLogin()
     return blogger_service

def PrintUserBlogInfo(blogger_service):
     query = service.Query()
     query.feed = '/feeds/default/blogs'
     feed = blogger_service.Get(query.ToUri())
     blog_id = feed.entry[0].GetSelfLink().href.split("/")[-1]
     print feed.title.text
     print blog_id
     for entry in feed.entry:
         print "\t" + entry.title.text,
         print entry.GetSelfLink().href.split("/")[-1]

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

def PrintAllPosts(blogger_service, blog_id):
   feed = blogger_service.GetFeed('/feeds/' + blog_id + '/posts/default')
   print feed
   print feed.title.text
   for entry in feed.entry:
       print "\t" + entry.title.text
       print "\t" + entry.content.text
       print "\t" + entry.updated.text
       try:
           categories = entry.category
           print categories
           for category in categories:
               print category
       except:
           continue

def CreateDraftPost(blogger_service, blog_id, title, content):
 entry = gdata.GDataEntry()
 entry.title = atom.Title('xhtml', title)
 entry.content = atom.Content(content_type='html', text=content)

 control = atom.Control()
 control.draft = atom.Draft(text='yes')
 entry.control = control

def CreatePublicPost(blogger_service, blog_id, title, content):
    entry = gdata.gdataentry()
    print dir(entry)
    entry.title = atom.title('xhtml', title)
    entry.content = atom.content(content_type='html', text=content)
    category = atom.category()
    #print dir(category)
    category2 = atom.category()
    category.scheme = "http://www.blogger.com/atom/ns#"
    category2.scheme = "http://www.blogger.com/atom/ns#"
    category.term = "labelname"
    print category
    category2.term = "labelname2"
    entry.category = [category,category2]
    print entry
    #entry.category.append(category2)
    #entry.categories = [category,category2]
    return blogger_service.post(entry, '/feeds/%s/posts/default' % blog_id)

def createoldpublicpost(blogger_service, blog_id, title, content,
published, updated):
    entry = gdata.gdataentry()
    entry.title = atom.title('xhtml', title)
    entry.published = atom.published(published)
    entry.updated = atom.updated(updated)
    entry.content = atom.content(content_type='html', text=content)
    print entry
    return blogger_service.post(entry, '/feeds/%s/posts/default' % blog_id)


feeds = ["http://partiallyattended.vox.com/library/posts/2007/07/atom-full.xml",
       "http://partiallyattended.vox.com/library/posts/2007/08/atom-full.xml",
       "http://partiallyattended.vox.com/library/posts/2007/08/page/2/atom-full.xml",
       "http://partiallyattended.vox.com/library/posts/2007/09/atom-full.xml",
       "http://partiallyattended.vox.com/library/posts/2007/10/atom-full.xml",
       "http://partiallyattended.vox.com/library/posts/2007/11/atom-full.xml",
       "http://partiallyattended.vox.com/library/posts/2007/12/atom-full.xml",
       "http://partiallyattended.vox.com/library/posts/2008/01/atom-full.xml",
       "http://partiallyattended.vox.com/library/posts/2008/02/atom-full.xml",
       "http://partiallyattended.vox.com/library/posts/2008/02/page/2/atom-full.xml",
       "http://partiallyattended.vox.com/library/posts/2008/03/atom-full.xml",
       "http://partiallyattended.vox.com/library/posts/2008/04/atom-full.xml",
       "http://partiallyattended.vox.com/library/posts/2008/05/atom-full.xml",
       "http://partiallyattended.vox.com/library/posts/2008/06/atom-full.xml",
       "http://partiallyattended.vox.com/library/posts/2008/07/atom-full.xml"]
   

def temp{}:
    
    # get access to blogger version of partially attended
    #blogger_service = AuthenticateSession(username,password)
    #feed = GetBlogFeed(blogger_service)
    #blog_id = GetBlogId(feed)
    
    print 'getting blogger access'
    # get access to blogger version of partially attended
    username = ''
    password = ''
    blogger_service = AuthenticateSession(username,password)
    feed = GetBlogFeed(blogger_service)
    z_blog_id = GetBlogIdZillertal(feed)
    p_blog_id = GetBlogIdPA(feed)
    
    PrintUserBlogInfo(blogger_service)
    
    print 'z', z_blog_id
    print 'p', p_blog_id
    
    entry = d['entries'][0]
    published =  entry['published']
    updated =  entry['updated']
    print published
    title = entry['title']
    print title
    content = entry['content'][0]['value']
    print content
    print 'creating new entry on blogger'
    CreateOldPublicPost(blogger_service,p_blog_id,title,content,published,updated) 

def check_options(options):
    if options.user == None or options.password == None:     
        error = "you need to specify a username and password"
        return error
    else:
        return False

def parse_options():
    usage = "script -u username -p password [-h help]"
    version = "0.0.1"
    parser = OptionParser(usage=usage,version=version)
    parser.add_option("-u","--user",dest="user",help="provide google account username")
    parser.add_option("-p","--password",dest="password",help="provide google account password")
    (options, args) = parser.parse_args()
    error = check_options(options) # check passed options for any errors 
    if error:
        parser.error(error)
    else:
        return options

def main():
    options = parse_options()
    username = options.user
    password = options.password
    print username
    print password
    feed = feeds[0]
    print 'getting vox data'
    d = feedparser.parse(feed)
    entries = d.entries
    entry = entries[0]
    


if __name__ == "__main__":
    main()
