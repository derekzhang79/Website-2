#/handlers/projects/view.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/26/11
#
#Displays a page from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.project import Project
from errors.project import ProjectNotFoundException
from models.link import Link
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class ViewProjectHandler(webapp.RequestHandler):
    def get(self, url):
        url = url.strip().strip("/")
        project = Project(url=url)
        link = Link(group="project_%s" % project.url)
        links = link.get_group()
        try:
            project.get()
        except ProjectNotFoundException:
            self.response.out.write("404")
        else:
            template_values = {
                'name' : project.name,
                'links' : links,
                'images' : project.images,
                'description' : project.description
            }
            path = os.path.join(os.path.dirname(__file__), '../../template/hauk', 'portfolio.html')
            self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/projects/(.*)', ViewProjectHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
