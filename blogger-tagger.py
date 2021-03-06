#!/usr/bin/pyton
""""
blogger-tagger 

"""


import sys
from optparse import OptionParser, OptionGroup


from gdata import service
import sys
import gdata
import atom

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
        print "\t" + entry.title.text

def GetBlogFeed(blogger_service):
    query = service.Query()
    query.feed = "/feeds/default/blogs"
    feed = blogger_service.Get(query.ToUri())
    return feed

def GetBlogId(feed):
    blog_id = feed.entry[0].GetSelfLink().href.split("/")[-1]
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

def CreatePublicPost(blogger_service, blog_id, title, content):
    entry = gdata.GDataEntry()
    print dir(entry)
    entry.title = atom.Title('xhtml', title)
    entry.content = atom.Content(content_type='html', text=content)
    category = atom.Category()
    #print dir(category)
    category2 = atom.Category()
    category.scheme = "http://www.blogger.com/atom/ns#"
    category2.scheme = "http://www.blogger.com/atom/ns#"
    category.term = "labelname"
    print category
    category2.term = "labelname2"
    entry.category = [category,category2]
    print entry
    #entry.category.append(category2)
    #entry.categories = [category,category2]
    return blogger_service.Post(entry, '/feeds/%s/posts/default' % blog_id)

def createoldpublicpost(blogger_service, blog_id, title, content, published, updated):
    entry = gdata.gdataentry()
    entry.title = atom.title('xhtml', title)
    entry.published = atom.published(published)
    entry.updated = atom.updated(updated)
    entry.content = atom.content(content_type='html', text=content)
    print entry
    return blogger_service.post(entry, '/feeds/%s/posts/default' % blog_id)
    
def CreateDraftPost(blogger_service, blog_id, title, content):
    entry = gdata.GDataEntry()
    entry.title = atom.Title('xhtml', title)
    entry.content = atom.Content(content_type='html', text=content)
    control = atom.Control()
    control.draft = atom.Draft(text='yes')
    entry.control = control
    
    

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
    #blogger_service = AuthenticateSession(username,password)
    #feed = GetBlogFeed(blogger_service)
    #blog_id = GetBlogId(feed)
    #PrintAllPosts(blogger_service,blog_id)
    #blogEntry = CreatePublicPost(blogger_service, blog_id, title='I have another answer', content='Eureka! It is 42!')
      
if __name__ == "__main__":
    main()

