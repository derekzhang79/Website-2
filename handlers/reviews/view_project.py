#/handlers/reviews/view_project.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/18/11
#
#Displays a review from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.review import Review
from models.project import Project
from models.link import Link
from models.person import Person
from errors.project import ProjectNotFoundException
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

class ViewProjectReviewsHandler(webapp.RequestHandler):
    def get(self, project_url):
        project = Project(url=project_url)
        try:
            project.get()
        except ProjectNotFoundException:
            self.response.out.write("404")
        else:
            review = Review(project=project.datastore)
            content = ""
            reviews = review.get_for_project()
            for review in reviews:
                content += "\n\t\t<h2><a href=\"/projects/%s/reviews/%s\" title=\"Review of %s from %s\">%s</a></h2>" % (review.project.url, review.url, review.project.name, review.publication, review.publication)
                content += "\n\t\t<p>%s</p>" % review.excerpt
            sidebar = """<h2>Your review here.</h2>
            <p>Have you written about %s? We'd like to see what you've written, and possibly even feature it on this page. We love to hear feedback from our users and reviewers, and we're pretty proud when someone writes nice stuff about us. Send us an email at reviews@secondbit.org with a link to your review, and we'll consider putting it up here.</p>""" % review.project.name
            person = Person()
            people = person.get_featured()
            link = Link(group="special_menu")
            menu = link.get_group()
            template_values = {
                'content' : content,
                'title' : "Reviews of %s" % review.project.name,
                'subheader_title' : "Look at the nice things people are saying",
                'sidebar' : sidebar,
                'menu' : menu,
                'people' : people
            }
            path = os.path.join(os.path.dirname(__file__), '../../template/hauk', 'secondary.html')
            self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/projects/([^/]*)/reviews/', ViewProjectReviewsHandler),
    ('/projects/([^/]*)/reviews', ViewProjectReviewsHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
