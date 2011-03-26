#/handlers/services/list.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/8/11
#
#Displays a list of services from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.service import Service
from models.link import Link
from models.person import Person
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class ListServicesHandler(webapp.RequestHandler):
    def get(self):
        service = Service()
        services = service.get_list()
        content = """<h2>Services</h2>
        <table>
            <tr>
                <th>Title</th>
                <th>Icon</th>
                <th>Featured</th>
                <th>Modified By</th>
                <th>Modified On</th>
                <th>Actions</th>
            </tr>"""
        for service in services:
            modified_on = service.modified_on.strftime("%m/%d/%y %H:%M")
            featured = "No"
            if service.featured:
                featured = "Yes"
            content += """<tr>
                <td><a href="/services/%s">%s</a></td>
                <td><a href="/image/%s" title="Icon">%s</a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td><a href="/admin/services/edit/%s" title="Edit %s">Edit</a> | <a href="/admin/services/delete/%s" title="Delete %s">Delete</a></td>
            </tr>""" % (service.url, service.title, service.icon.shortname, service.icon.shortname, featured, service.modified_by.email(), modified_on, service.url, service.title, service.url, service.title)
        content += "</table>"
        sidebar = """<h2>Service Administration</h2>
        <p>You can edit and delete the services in the datastore by clicking the
        appropriate link. You can also <a href="/admin/servicess/add" title="Add a
        service">add a service</a> to the datastore.</p>"""
        person = Person()
        people = person.get_featured()
        link = Link(group="special_menu")
        menu = link.get_group()
        template_values = {
            'content' : content,
            'sidebar' : sidebar,
            'title' : "Services",
            'menu' : menu,
            'people' : people
        }
        path = os.path.join(os.path.dirname(__file__), "../../template/hauk", "secondary.html")
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/admin/services', ListServicesHandler),
    ('/admin/services/', ListServicesHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
