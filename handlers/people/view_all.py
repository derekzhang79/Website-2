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
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from datetime import datetime

class ViewTeamHandler(webapp.RequestHandler):
    def get(self):
        person_obj = Person()
        people = person_obj.get_list()
        content = ""
        for person in people:
            joined = person.date_joined.strftime("%m/%d/%y")
            description = person.description.split("</p>")
            if len(description) > 1:
                description = description[0] + "</p>" + description[1] + "</p>"
            else:
                description = description[0] + "</p>"
            content += """<h2 style="clear: both;"><a href="/team/%s"
            title="Meet %s">%s</a></h2>
            <p><img src="/image/%s" style="float: left; padding-right: 10px;
            padding-bottom: 10px; clear: both;" />%s</p>""" % (person.url, person.name, person.name, person.avatar.shortname, description)
        sidebar = "<h2>Sidebar</h2><p>of doom!</p>"
        template_values = {
            'content' : content,
            'title' : "Team",
            'subheader_title' : "Just let the classiness waft over you",
            'sidebar' : sidebar,
            'people' : person_obj.get_featured()
        }
        path = os.path.join(os.path.dirname(__file__), '../../template/hauk', 'secondary.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/team/', ViewTeamHandler),
    ('/team', ViewTeamHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
