import pystache
import hashlib

@map_function
def post_and_comments(doc):
    if 'type' in doc:
        if doc['type'] == 'blog-post':
            emit([doc['_id'], {}], doc)
        if doc['type'] == 'blog-comment':
            emit([doc['blog-id'], doc['timestamp']], doc)

post_template = """
<html>
    <head><title>{{title}}</title></head>
    <body>
        <div class="header">
            <div class="header-left"><a href="/">Traceback (most recent call last):</a></div>
            <div class="header-right">&nbsp;Tags:&nbsp;{{{tags}}}</div>
        </div>
        <div class="title">
            <div class="title-text">{{title}}</div>
            <div class="timestamp">{{timestamp}}</div>
            <div class="author">by <a href="/about">Mikeal Rogers</a></div>
        </div>
        <style type="text/css">
        body {
          color:#222222;
          font-family:"Sabon LT Std","Palatino Linotype","Book Antiqua",serif;
          font-size:18px;
          background-color:#E5E5E5;
          padding:0;
          margin:0;
        }
        .header {
          background-color:#FFFFFF;
          width:100%;
          height:30px;
          font-size:15px;
        }
        .header-left {
          float:left;
          width:49%;
          padding-left:8px;
          padding-top:4px;
        }
        .header-right {
          float:left;
          width:49%;
          padding-right:8px;
          padding-top:4px;
          text-align:right;
        }
        .title {
          color:#2E2E2E;
          padding-top:4px;
          text-align:center;
        }
        .post-container {
          width:100%;
          float:left;
          padding-bottom:40px;
        }
        .post-left-border {
          float:left;
          width:7%;
        }
        .post-body-container {
          float:left;
          width:84%;
        }
        .post-body-rounded {
          padding-left:5px;
          padding-right:5px;
          padding-top:2px;
          padding-bottom:2px;
          background-color:#FFFFFF;
        }
        .post-body-rendered {
          padding-left:10px;
          padding-right:10px;
        }
        .post-right-border {
          float:left;
          width:7%;
        }
        .comment {
          padding-top:10px;
          width:100%;
          float:left;
        }
        .comment-rounded {
          padding-left:5px;
          padding-top:5px;
          width:100%;
          background-color:#FFFFFF;
          float:left;
        }
        .comment-author {
          width:15%;
          float:left;
          vertical-align:center;
          text-align:center;
        }
        .comment-text {
          width:85%;
          float:left;
        }
        .comment-header {
          padding-top:10px;
          padding-bottom:10px;
          text-align:center;
        }
        </style>
        <script language="javascript" type="text/javascript" 
                src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js">
        </script>
        <script language="javascript" type="text/javascript" 
                src="/blog/_design/blog/jquery.corner.js">
        </script>
        <script lanuage="javascript" type="text/javascript">
        $().ready(function () {
            $("div.post-body-rounded").corner("30px");
            $("div.comment-rounded").corner("20px");
        });
        </script>
        
        <div class="post-container" class="cbb">
            <div class="post-left-border">{{{spacer-text}}}</div>
            <div class="post-body-container">
                <div class="post-body-rounded">
                    <div class="post-body-rendered">
                        {{{body}}}
                    </div>
                </div>
                <div class="comment-header">Comments</div>
                <div class="comment-container">
"""

comment = """
<div class="comment">
    <div class="comment-rounded">
        <div class="comment-author">
            <img src="http://www.gravatar.com/avatar/{{email-hash}}.jpg" alt="{{name}}"/>
            <div class="author-text">{{{author}}}</div>
        </div>
        <div class="comment-text">{{{body}}}</div>
    </div>
</div>
"""

footer = """
                </div>
            </div>
            <div class="post-right-border">{{{spacer-text}}}</div>
        </div>
    </body>
</html>
"""

spacer_text = '&nbsp;'.join(['&nbsp;' for x in range(10)])

class ShowPost(ListView):
    def start(self, head, req):
        return [], {'headers':{'content-type':'text/html'}}
    def list_row(self, row):
        doc = row['value']
        if self.index is 0:
            tags = ', '.join(['<a href="'+tag+'">'+tag+'</a>' for tag in doc['tags']])
            body = pystache.render(post_template, {'tags':tags, 'title':doc['title'],
                                                   'body':doc['body-rendered'],
                                                   'timestamp':doc['timestamp'],
                                                   'spacer-text':spacer_text,
                                                  })
            return body
        else:
            if type(doc['name']) is not str and type(doc['name']) is not unicode:
                return
            if doc.get('website', None):
                author = '<a href="'+doc['website']+'">'+doc['name']+'</a>'
            else:
                author = doc['name']
            rend = pystache.render(comment, {'name':doc['name'],'body':doc['body-rendered'],
                                             'email-hash':hashlib.md5(doc.get('email','')).hexdigest(),
                                             'website':doc.get('website', False),
                                             'author':author,
                                            })
            return rend
        
    def list_end(self):
        return pystache.render(footer, {"spacer-text":spacer_text})




