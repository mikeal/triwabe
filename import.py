import feedparser
import httplib2
from datetime import datetime
import json
feed_url = "http://www.mikealrogers.com/feed"

http = httplib2.Http()

def import_comments(url, blogid=None):
    feed = feedparser.parse(url)
    for post in feed.entries:
        p = {'blog-id':blogid,
             'body-raw':post.content[0]['value'][3:].replace('<p>','\n').replace('</p>','\n'),
             'timestamp':datetime(*post.date_parsed[:-2]).isoformat(),
             'name':post['author'],
             }
        if '[...]' not in post.content[0]['value'][3:].replace('<p>','\n').replace('</p>','\n'):
            resp, content = http.request('http://localhost:5984/blog/_design/blog/_update/newComment', 
                                          method='POST', body=json.dumps(p))
            print content

def importer(url):
    feed = feedparser.parse(url)
    for post in feed.entries:
        p = {'title':post['title'], 
             'body-raw':post.content[0]['value'][3:].replace('<p>','\n').replace('</p>','\n'),
             'timestamp':datetime(*post.date_parsed[:-2]).isoformat(),
             'wp-id':post.id.split('/?p=')[-1], 'tags':[x['term'] for x in post.tags]}
        
        resp, content = http.request('http://localhost:5984/blog/_design/blog/_update/newPost', 
                                     method='POST', body=json.dumps(p))
        print content
        import_comments(post.wfw_commentrss, content)
        
if __name__ == '__main__':
    importer(feed_url)