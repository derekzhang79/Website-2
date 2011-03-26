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
from models.link import Link
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
        sidebar = """<h2>It's a team effort.</h2>
        <p>We like the term "team" over, say, "staff", because it's a little more intimate, a little more expressive of the bond we share as we work with software. We like to think Second Bit is as much about the people as it is about the software, and we work hard to stay close and have fun as a team. It's hard to do great work when you're around people you whose company you don't genuinely enjoy, so we've made it a priority to work with only the most awesome people we can find.</p>
        
        <h2>Your picture here?</h2>
        <p>Think you're pretty awesome? Think Second Bit sounds like a lot of fun? We definitely want to <a href="/contact" title="Contact Us">hear from you</a>. We may or may not be hiring at this point (it changes based on our mood at that particular moment), so get in touch. We're pretty fun to work with, we swear.</p>"""
        link = Link(group="special_menu")
        menu = link.get_group()
        template_values = {
            'content' : content,
            'title' : "Team",
            'subheader_title' : "Just let the classiness waft over you",
            'sidebar' : sidebar,
            'people' : person_obj.get_featured(),
            'menu' : menu
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
