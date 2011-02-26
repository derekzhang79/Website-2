#/handlers/links/delete.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/25/11
#
#Handles requests to delete a link.

import sys, os, logging
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.link import Link
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class DeleteLinkHandler(webapp.RequestHandler):
    def get(self, key=None):
        if key is None:
            self.redirect("/admin/links")
        else:
            link = Link(key=key)
            link.get()
            content = """<form method="post">
                <p>
                Are you sure you want to delete <a href="%s" title="%s">%s</a>?
                </p>
                <input type="submit" value="Yes" />
            </form>""" % (link.url, link.title, link.name)
            sidebar = """<h2>Warning</h2>
            <p>When a link is deleted, it is gone for good. Make sure you want
            to do this.</p>"""
            template_values = {
                'content' : content,
                'title' : 'Delete Link "%s"', % link.name
                'sidebar' : sidebar
            }
            path = os.path.join(os.path.dirname(__file__), '../../template/hauk', 'secondary.html')
            self.response.out.write(template.render(path, template_values))

    def post(self, key=None):
        link = Link()
        if key is not None:
            link.key = key
            link.get()
            link.delete()
        self.redirect("/admin/links")

application = webapp.WSGIApplication([
                                ('/admin/links/delete/(.*)', DeleteLinkHandler)
                                ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
