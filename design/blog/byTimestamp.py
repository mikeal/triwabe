@map_function
def posts_by_timestamp(doc):
    if 'type' in doc and doc['type'] == 'blog-post':
        emit(doc['timestamp'], doc)