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
            sidebar = "<h2>Reviews of %s</h2>" % review.project.name
            sidebar += "\n\t<ul>"
            reviews = review.get_for_project()
            for other_review in reviews:
                sidebar += "\n\t\t<li><a href=\"/projects/%s/reviews/%s\" title=\"Review of %s from %s\">%s</a></li>" % (review.project.url, review.url, review.project.name, review.publication, review.publication)
            template_values = {
                'content' : review.content,
                'title' : "Review of %s from %s" % (review.project.name, review.publication),
                'sidebar' : sidebar
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
