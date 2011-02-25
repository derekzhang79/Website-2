#/handlers/link/delete.py
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
            self.response.out.write("""<form method="post">
                <p>
                Are you sure you want to delete <a href="%s" title="%s">%s</a>?
                </p>
                <input type="submit" value="Yes" />
            </form>""", (link.url, link.title, link.name))

    def post(self, key=None):
        link = Link()
        if key is not None:
            link.key = key
            link.delete()
            self.response.out.write("<p>Successfully deleted link.</p>")
        else:
            self.redirect("/admin/links")

application = webapp.WSGIApplication([
                                ('/admin/links/delete/(.*)', DeleteLinkHandler)
                                ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
