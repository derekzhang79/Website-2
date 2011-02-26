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
from errors.page import PageNotFoundException
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
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
            action = "Add"
            name = ""
        else:
            page = Page(url=url)
            try:
                page.get()
            except PageNotFoundException:
                self.redirect("/admin/pages")
            action = "Edit"
            name = ' "%s"' % page.title
            if page.is_public:
                public = " checked=\"checked\""
            else:
                public = ""
        content = """<h2>%s Page%s</h2>
            <p>
                <form method="post">
                    <label>Title</label>
                    <input type="text" name="title" value="%s" /><br />
                    <label>URL</label>
                    <input type="text" name="url" value="%s" /><br />
                    <label>Public?</label>
                    <input type="checkbox" name="is_public" value="True"%s /><br />
                    <label>Content</label>
                    <textarea name="content">%s</textarea><br />
                    <label>Sidebar</label>
                    <textarea name="sidebar">%s</textarea><br />
                    <input type="submit">
                </form>
            <p>""" % (action, name, page.title, page.url, public, page.content, page.sidebar)
        sidebar = """<h2>Hints!</h2>
        <p>
            <b>Title</b>: The name of the page.<br />
            <b>URL</b>: The slug for the page. http://www.secondbit.org/about's
                slug is 'about'.<br />
            <b>Public?</b>: Should this page be public? If not, only admins who
            are logged in will be able to view it.<br />
            <b>Content</b>: The HTML that is rendered in the left column.<br />
            <b>Sidebar</b>: The HTML that is rendered in the right column (this
                is in the sidebar).<br />
            <br />
            <i>The content and sidebar inputs should each begin with
            "&lt;h2&gt;Section Title&lt;/h2&gt;" and be followed by
            "&lt;p&gt;This is the text...&lt;/p&gt;" to avoid rendering issues,
            plugging in the desired section title and text.</i>
        </p>"""
        title = "%s Page%s" % (action, name)
        template_values = {
            'content' : content,
            'title' : title,
            'sidebar' : sidebar
        }
        path = os.path.join(os.path.dirname(__file__), '../../template/hauk', 'secondary.html')
        self.response.out.write(template.render(path, template_values))

    def post(self, url=None):
        page = Page()
        if url is not None:
            page.url = url
            page.get()
        page.title = self.request.POST['title']
        page.content = self.request.POST['content']
        page.sidebar = self.request.POST['sidebar']
        page.url = self.request.POST['url']
        try:
            public = self.request.POST['is_public']
        except KeyError:
            public = "False"
        if public == "True":
            page.is_public = True
        else:
            page.is_public = False
        page.save()
        self.redirect("/%s" % page.url)

application = webapp.WSGIApplication([
                                ('/admin/pages/add', AddEditPageHandler),
                                ('/admin/pages/edit/(.*)', AddEditPageHandler),
                                ('/admin/pages/add/', AddEditPageHandler)
                                ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
