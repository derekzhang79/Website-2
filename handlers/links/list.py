#/handlers/links/list.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/25/11
#
#Displays a list of links from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.link import Link
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class ListLinksHandler(webapp.RequestHandler):
    def get(self):
        link = Link()
        links = link.get_list()
        content = """<table>
        <tr>
            <th>Name</th>
            <th>Title</th>
            <th>URL</th>
            <th>Weight</th>
            <th>Group</th>
            <th>Modified By</th>
            <th>Modified On</th>
            <th>Actions</th>
        </tr>"""
        for link in links:
            content += """<tr>
                <td>%s</td>
                <td>%s</td>
                <td><a href="%s">%s</a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td><a href="/admin/links/edit/%s" title="Edit %s">Edit</a> | <a href="/admin/links/reorder/%s" title="Reorder %s">Reorder</a> | <a href="/admin/links/delete/%s" title="Delete %s">Delete</a></td>
            </tr>""" % (link.name, link.title, link.url, link.url, link.weight, link.group, link.modified_by.email(), link.modified_on, link.key(), link.name, link.group, link.group, link.key, link.name)
        self.response.out.write(content)

application = webapp.WSGIApplication([
    ('/admin/links', ListLinksHandler),
    ('/admin/links/', ListLinksHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
