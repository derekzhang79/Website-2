#/handlers/reviews/view.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/18/11
#
#Displays a review from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.review import Review
from models.person import Person
from models.link import Link
from errors.review import ReviewNotFoundException
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

class ViewReviewHandler(webapp.RequestHandler):
    def get(self, project, url):
        url = url.strip().strip("/")
        review = Review(url=url)
        try:
            review.get()
        except ReviewNotFoundException:
            self.response.out.write("404")
        else:
            content = "<h2>Review of %s from %s</h2>\n" % (review.project.name, review.publication)
            sidebar = "<h2>Reviews of %s</h2>" % review.project.name
            sidebar += "\n\t<ul>"
            reviews = review.get_for_project()
            for other_review in reviews:
                sidebar += "\n\t\t<li><a href=\"/projects/%s/reviews/%s\" title=\"Review of %s from %s\">%s</a></li>" % (other_review.project.url, other_review.url, other_review.project.name, other_review.publication, other_review.publication)
            link = Link(group="special_menu")
            menu = link.get_group()
            person = Person()
            people = person.get_featured()
            template_values = {
                'content' : "%s%s" % (content, review.content),
                'subheader_title' : "Look at the nice things people are saying",
                'sidebar' : sidebar,
                'menu' : menu,
                'people' : people,
                'title' : 'Review of %s from %s' % (review.publication, review.project.name)
            }
            path = os.path.join(os.path.dirname(__file__), '../../template/hauk', 'secondary.html')
            self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/projects/([^/]*)/reviews/(.*)', ViewReviewHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
