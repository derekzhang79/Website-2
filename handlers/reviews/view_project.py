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
            template_values = {
                'content' : content,
                'title' : "Look at the nice things people are saying",
                'sidebar' : "<h2>This is a sidebar and shit.</h2><p>Srsly.</p>"
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
