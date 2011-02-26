#/handlers/pages/list.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/25/11
#
#Displays a list of pages from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.page import Page
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class ListPagesHandler(webapp.RequestHandler):
    def get(self):
        page = Page()
        pages = page.get_list()
        content = """<h2>Pages</h2>
        <table>
            <tr>
                <th>Title</th>
                <th>URL</th>
                <th>Visibility</th>
                <th>Modified By</th>
                <th>Modified On</th>
                <th>Actions</th>
            </tr>"""
        for page in pages:
            modified_on = page.modified_on.strftime("%m/%d/%y %H:%M")
            visibility = "Private"
            if page.is_public:
                visibility = "Public"
            content += """<tr>
                <td>%s</td>
                <td><a href="/%s">%s</a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td><a href="/admin/pages/edit/%s" title="Edit %s">Edit</a> | <a href="/admin/pages/delete/%s" title="Page %s">Delete</a></td>
            </tr>""" % (page.title, page.url, page.url, visibility, page.modified_by.email(), modified_on, page.url, page.title, page.url, page.title)
        content += "</table>"
        sidebar = """<h2>Page Administration</h2>
        <p>You can edit and delete the pages in the datastore by clicking the
        appropriate link. You can also <a href="/admin/pages/add" title="Add a
        page">add a page</a> to the datastore.</p>"""
        template_values = {
            'content' : content,
            'sidebar' : sidebar,
            'title' : "Pages"
        }
        path = os.path.join(os.path.dirname(__file__), "../../template/hauk", "secondary.html")
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/admin/pages', ListPagesHandler),
    ('/admin/pages/', ListPagesHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
