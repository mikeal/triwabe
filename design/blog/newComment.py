from datetime import datetime

import markdown2
import json
import uuid

import os

@update_function
def new_blog_post(doc, request):
    doc = json.loads(request['body'])
    doc['_id'] = str(uuid.uuid1()).replace('-','')
    doc['type'] = 'blog-comment'
    doc['body-rendered'] = markdown2.markdown(doc['body-raw'], safe_mode=False)
    if 'timestamp' not in doc:
        doc['timestamp'] = datetime.now().isoformat()
    return doc, doc['_id']