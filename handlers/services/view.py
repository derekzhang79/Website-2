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
            #services .%s { background: url('/services/%s/icon') no-repeat top left; }
            </style>""" % (service.url, service.url)
            content = """<ul id="services">
                <li class="%s onethird">
                    <h3>%s</h3>
                    %s
                </li>
            </ul>""" % (service.url, service.title, service.description)
            sidebar = """<h2>Don't know what to put here</h2>
            <p>What should I put here?</p>"""
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
