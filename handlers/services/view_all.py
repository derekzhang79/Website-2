#/handlers/services/view.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/3/11
#
#Displays a service from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.service import *
from errors.service import *
from models.person import Person
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class ViewServicesHandler(webapp.RequestHandler):
    def get(self):
        service = Service()
        services = service.get_list()
        header = """<style type="text/css">
        ul#services, ul#services li { list-style: none; padding: 0px 0px; }"""
        content = """<ul id="services">"""
        for service in services:
            header += """#services .service-icon-%s { background: url('/services/%s/icon') no-repeat top left; }""" % (service.url, service.url)
            content += """<li class="service-icon-%s">
                    <h3><a href="/services/%s" title="More about %s">%s</a></h3>
                    %s
                </li>""" % (service.url, service.url, service.title, service.title, service.excerpt)
        content += "</ul>"
        header += "</style>"
        sidebar = """<h2>Can't Find What You're Looking For?</h2>
        <p>We can't do <em>everything</em>, and we'll be the first to admit it. Sometimes,
        our clients need a service we don't know how to provide. Still, you
        should <a href="/contact" title="Contact Us">get in touch</a>. We're
        quick learners, and even if we can't help you, we may be able to point
        you to someone who can.</p>"""
        title = "Services"
        person = Person()
        people = person.get_featured()
        template_values = {
            'header' : header,
            'content' : content,
            'title' : title,
            'sidebar' : sidebar,
            'people' : people
        }
        path = os.path.join(os.path.dirname(__file__), '../../template/hauk', 'secondary.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/services/', ViewServicesHandler),
    ('/services', ViewServicesHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
