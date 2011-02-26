#/handlers/pages/add_edit.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/25/11
#
#Handles requests to add or edit a page.

import sys, os, logging
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.page import Page
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class AddEditPageHandler(webapp.RequestHandler):
    def get(self, url=None):
        if url is None:
            page = Page()
            page.title = ""
            page.content = ""
            page.sidebar = ""
            page.url = ""
            public = ""
        else:
            page = Page(url=url)
            page.get()
            if page.is_public:
                public = " checked=\"checked\""
            else:
                public = ""
        self.response.out.write("""
            <form method="post">
                <label>Title</label>
                <input type="text" name="title" value="%s" /><br />
                <label>URL</label>
                <input type="text" name="url" value="%s" /><br />
                <label>Public?</label>
                <input type="checkbox" name="is_public" value="True"%s /><br />
                <label>Content</label>
                <textarea name="content">%s</textarea>
                <label>Sidebar</label>
                <textarea name="sidebar">%s</textarea>
                <input type="submit">
            </form>""" % (page.title, page.url, public, page.content, page.sidebar))

    def post(self, url=None):
        page = Page()
        if url is not None:
            page.url = url
            page.get()
        page.title = self.request.POST['title']
        page.content = self.request.POST['content']
        page.sidebar = self.request.POST['sidebar']
        page.url = self.request.POST['url']
        public = self.request.POST['is_public']
        if public == "True":
            page.is_public = True
        else:
            page.is_public = False
        page.save()

application = webapp.WSGIApplication([
                                ('/admin/pages/add', AddEditPageHandler),
                                ('/admin/pages/edit/(.*)', AddEditPageHandler),
                                ('/admin/pages/add/', AddEditPageHandler)
                                ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
