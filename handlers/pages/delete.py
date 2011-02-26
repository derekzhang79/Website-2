#/handlers/pages/delete.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/25/11
#
#Handles requests to delete a page.

import sys, os, logging
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.page import Page
from errors.page import PageNotFoundException
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class DeletePageHandler(webapp.RequestHandler):
    def get(self, url=None):
        if url is None:
            self.redirect("/admin/pages")
        else:
            page = Page(url=url)
            page.get()
            content = """<h2>Deleting Page "%s"</h2>
                <p>Are you sure you want to delete the page "%s"?
                    <form method="post">
                        <input type="submit" value="Yes" />
                    </form>
                </p>""" % (page.title, page.title)
            sidebar = """<h2>Careful!</h2>
                <p>Once you delete this page, it's gone forever! Make sure you
                want to do this. If in doubt, just mark the page as private, and
                only admins will be able to see it. You can do this in <a
                href="/admin/pages/edit/%s" title="Edit %s">the page's edit
                page</a>.</p>""" % (page.url, page.title)
            template_values = {
                'title' : 'Delete Page "%"' % page.title,
                'content' : content,
                'sidebar' : sidebar
            }
            path = os.path.join(os.path.dirname(__file__), '../../template/hauk', 'secondary.html')
            self.response.out.write(template.render(path, template_values))

    def post(self, url=None):
        page = Page()
        if url is not None:
            page.url = url
            try:
                page.get()
            except PageNotFoundException:
                self.redirect("/admin/pages")
            else:
                page.delete()
                self.redirect("/admin/pages")
        else:
            self.redirect("/admin/pages")

application = webapp.WSGIApplication([
                                ('/admin/pages/delete/(.*)', DeletePageHandler)
                                ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
