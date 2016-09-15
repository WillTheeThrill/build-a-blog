import os
import webapp2
import jinja2

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)
    def render_str(self,template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))
class ContentPost(db.Model):
    title = db.StringProperty(required =True)
    posts = db.TextProperty(required= True)
    created = db.DateTimeProperty(auto_now_add = True)
class MainPage(MainHandler):
    def loadPages(self,title="",posts="",error=""):
        self.render("interface.html",title=title,posts=posts,error=error)
    def get(self):
        self.loadPages()
    def post(self):
        title = self.request.get("title")
        posts = self.request.get("posts")

        if title and posts:
            a = ContentPost(title=title,posts=posts)
            a.put()
            contents = db.GqlQuery("SELECT * FROM ContentPost Order By created DESC")
            self.redirect("/blog")
        else:
            error="Please enter both a title and post"
            self.loadPages(title,posts,error)
class MainBlog(MainHandler):
    def loadPages(self,title="",posts=""):
        contents = db.GqlQuery("SELECT * FROM ContentPost Order By created DESC LIMIT 6")
        self.render("blog.html",title=title,posts=posts,contents=contents)
    def get(self):
        self.loadPages()
    def post(self):
        self.loadPages()
class ViewPostHandler(MainHandler):
    def loadPages(self,title="",posts=""):
        self.render("blog.html",title=title,posts=posts)
    def get(self, id):
    #    url_id = ContentPost.get_by_id(5556931766779904 )
        response = ContentPost.get_by_id(int(id))
        entrytitle = response.title
        entrypost = response.posts
        self.render("blogpost.html",title=entrytitle,posts=entrypost)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog',MainBlog),
    webapp2.Route('/blogpost/<id:\d+>', ViewPostHandler)
], debug=True)
