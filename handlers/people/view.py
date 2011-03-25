#/handlers/people/view.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/20/11
#
#Displays a person from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.person import Person
from errors.person import PersonNotFoundException
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from datetime import datetime

class ViewPersonHandler(webapp.RequestHandler):
    def get(self, url):
        url = url.strip().strip("/")
        person = Person(url=url)
        try:
            person.get()
        except PersonNotFoundException:
            self.response.out.write("404")
        else:
            joined = person.date_joined.strftime("%m/%d/%y")
            sidebar = """<h2>Quick Info</h2>
            <p><em>Title:</em> %s</p>
            <p><em>Joined Second Bit:</em> %s</p>
            <p><em>Website:</em> <a href="%s" title="%s' Homepage">%s</a></p>
            <p><em>Email:</em> %s</p>""" % (person.role, joined, person.homepage, person.name, person.homepage, person.email)
            content = """<h2>Meet %s</h2>
            <img src="/image/%s" style="float: left; padding-right: 10px;
            padding-bottom: 10px;" />%s""" % (person.name, person.avatar.shortname, person.description)

            template_values = {
                'content' : content,
                'title' : "Team: %s" % person.name,
                'sidebar' : sidebar,
                'people' : person.get_featured()
            }
            path = os.path.join(os.path.dirname(__file__), '../../template/hauk', 'secondary.html')
            self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/team/(.*)', ViewPersonHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
