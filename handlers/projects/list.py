#/handlers/projects/list.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/26/11
#
#Displays a list of projects from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.project import Project
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class ListProjectsHandler(webapp.RequestHandler):
    def get(self):
        project = Project()
        projects = project.get_list()
        content = """<h2>Projects</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>Nature</th>
                <th>Featured</th>
                <th>Open Source</th>
                <th>Modified By</th>
                <th>Modified On</th>
                <th>Actions</th>
            </tr>"""
        for project in projects:
            modified_on = project.modified_on.strftime("%m/%d/%y %H:%M")
            featured = "No"
            if project.featured:
                featured = "Yes"
            open_source = "No"
            if project.open_source:
                open_source = "Yes"
            content += """<tr>
                <td><a href="/projects/%s">%s</a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td><a href="/admin/projects/edit/%s" title="Edit %s">Edit</a> | <a href="/admin/projects/delete/%s" title="Delete %s">Delete</a></td>
            </tr>""" % (project.url, project.name, project.nature, featured, open_source, project.modified_by.email(), modified_on, project.url, project.name, project.url, project.name)
        content += "</table>"
        sidebar = """<h2>Project Administration</h2>
        <p>You can edit and delete the projects in the datastore by clicking the
        appropriate link. You can also <a href="/admin/projects/add" title="Add a
        project">add a project</a> to the datastore.</p>"""
        template_values = {
            'content' : content,
            'sidebar' : sidebar,
            'title' : "Projects"
        }
        path = os.path.join(os.path.dirname(__file__), "../../template/hauk", "secondary.html")
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/admin/projects', ListProjectsHandler),
    ('/admin/projects/', ListProjectsHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
