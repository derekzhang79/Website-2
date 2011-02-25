#/handlers/link/add_edit.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/25/11
#
#Handles requests to add or edit a link.

import sys, os, logging
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.link import Link
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class AddEditLinkHandler(webapp.RequestHandler):
    def get(self, key=None):
        if key is None:
            link = Link()
            link.name = ""
            link.title = ""
            link.url = ""
            link.weight = ""
            link.group = ""
        else:
            link = Link(key=key)
            link.get()
        self.response.out.write("""
            <form method="post">
                <label>Name</label>
                <input type="text" name="name" value="%s" /><br />
                <label>Title</label>
                <input type="text" name="title" value="%s" /><br />
                <label>URL</label>
                <input type="text" name="url" value="%s" /><br />
                <label>Weight</label>
                <input type="text" name="weight" value="%s" /><br />
                <label>Group</label>
                <input type="text" name="group" value="%s" /><br />
                <input type="submit">
            </form>""" % (link.name, link.title, link.url, link.weight, link.group))

    def post(self, key=None):
        link = Link()
        if key is not None:
            link.key = key
            link.get()
        link.name = self.request.POST['name']
        link.title = self.request.POST['title']
        link.url = self.request.POST['url']
        link.weight = self.request.POST['weight']
        link.group = self.request.POST['group']
        link.save()

application = webapp.WSGIApplication([
                                ('/admin/links/add', AddEditLinkHandler),
                                ('/admin/links/edit/(.*)', AddEditLinkHandler),
                                ('/admin/links/add/', AddEditLinkHandler)
                                ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
