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
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class ListLinksHandler(webapp.RequestHandler):
    def get(self):
        link = Link()
        links = link.get_list()
        content = """<table>
        <tr>
            <th>Link</th>
            <th>Weight</th>
            <th>Group</th>
            <th>Modified By</th>
            <th>Modified On</th>
            <th>Actions</th>
        </tr>"""
        for link in links:
            modified_on = link.modified_on.strftime("%m/%d/%y %H:%M")
            content += """<h2>Links</h2>
            <tr>
                <td><a title="%s" href="%s">%s</a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td><a href="/admin/links/edit/%s" title="Edit %s">Edit</a> | <a href="/admin/links/reorder/%s" title="Reorder %s">Reorder</a> | <a href="/admin/links/delete/%s" title="Delete %s">Delete</a></td>
            </tr>""" % (link.title, link.url, link.name, link.weight, link.group, link.modified_by.email(), modified_on, link.key(), link.name, link.group, link.group, link.key(), link.name)
        content += "</table>"
        sidebar = """<h2>Link Administration</h2>
        <p>You can edit, delete, and reorder the links in the datastore by
        clicking the appropriate link. You can also <a href="/admin/links/add"
        title="Add a link">add a link</a> to the datastore.</p>"""
        template_values = {
            'content' : content,
            'sidebar' : sidebar,
            'title' : "Links"
        }
        path = os.path.join(os.path.dirname(__file__), "../../template/hauk", 'secondary.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/admin/links', ListLinksHandler),
    ('/admin/links/', ListLinksHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
