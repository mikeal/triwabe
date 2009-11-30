import httplib2

base_url = "http://backtweets.com/search.json?q="

http = httplib2.Http()

def get_new_tweets(checkurl, last_id=None, key='key'):
    uri = base_url
    uri += checkurl
    if last_id:
        uri += '&since_id='+last_id
    uri+= '&key='+key
    resp, content = http.request(uri, method="GET")
    if resp.status != 200:
        print content
    assert resp.status == 200
    return json.loads(content) 
    
def check_new_tweets(doc, db):
    if 'wp-id' in doc:
        btweets = get_new_tweets("http://www.mikealrogers.com/archives"+str(doc['wp-id']),
                                 doc.get('backtweets',{}).get('tweets',[None])[-1])
    else:
        btweets = get_new_tweets("http://www.mikealrogers.com/posts/"+doc['_id'],
                                 doc.get('backtweets',{}).get('tweets',[None])[-1])

    if len(btweets['tweets']) is not 0:
        btweets['tweets'].reverse()
        if 'backtweets' in doc:
            btweets['tweets'] = ( doc['backtweets']['tweets'] + btweets['tweets'] )
            doc['backtweets'] = btweets
        db.update(doc)

