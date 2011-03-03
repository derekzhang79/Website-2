#/handlers/services/view.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/1/11
#
#Displays a service from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.service import Service
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
            sidebar = """<h2>Projects</h2>
            <p>We've successfully performed this service in the following
            projects:</p>
            <ul>
                <li><a href="/projects/tangles"
                title="Tangl.es">Tangl.es</a></li>
                <li><a href="/projects/test" title="Test Project">Test
                Project</a></li>
            </ul>"""
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
