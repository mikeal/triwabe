@map_function
def posts_by_timestamp(doc):
    if 'type' in doc and doc['type'] == 'blog-post':
        emit(doc['timestamp'], doc)


        
class BlogRoll(ListView):
    def start(self, head, req):
        pass
    def list_row(self, row):
        pass
    def list_end(self):
        pass