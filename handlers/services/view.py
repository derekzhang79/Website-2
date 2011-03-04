#/handlers/services/view.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/1/11
#
#Displays a service from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.service import *
from errors.service import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class ViewServiceHandler(webapp.RequestHandler):
    def get(self, url):
        url = url.strip().strip("/")
        service = Service(url=url)
        try:
            service.get()
        except ServiceNotFoundException:
            self.response.out.write("404")
        else:
            header = """<style type="text/css">
            #services .service-icon-%s { background: url('/services/%s/icon') no-repeat top left; }
            ul#services, ul#services li { list-style: none; padding: 0px 0px; }
            </style>""" % (service.url, service.url)
            content = """<ul id="services">
                <li class="service-icon-%s">
                    <h3>%s</h3>
                    %s
                </li>
            </ul>""" % (service.url, service.title, service.description)
            projects = ""
            if service.projects is not None:
                projects += "<ul>"
                for project in service.projects:
                    projects += "\n<li><a href=\"/projects/%s\" title=\"%s\">%s</a></li>" % (project.url, project.title, project.title)
                projects += "\n</ul>"
            if projects != "":
                sidebar = """<h2>Projects</h2>
                <p>We've successfully performed this service in the following
                projects:</p>
                %s""" % projects
            else:
                sidebar = """<h2>Be The First</h2>
                <p>We don't have any projects (that we can talk about, at least)
                that have used this service. Be the first kid on your block to
                get that bragging right!"""
            title = "Services: %s" % service.title
            template_values = {
                'header' : header,
                'content' : content,
                'title' : title,
                'sidebar' : sidebar
            }
            path = os.path.join(os.path.dirname(__file__), '../../template/hauk', 'secondary.html')
            self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/services/(.*)', ViewServiceHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
