#/handlers/reviews/list.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/25/11
#
#Displays a list of reviews from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.review import Review
from models.link import Link
from models.person import Person
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class ListReviewsHandler(webapp.RequestHandler):
    def get(self):
        review = Review()
        reviews = review.get_list()
        content = """<h2>Reviews</h2>
        <table>
        <tr>
            <th>Review</th>
            <th>Author</th>
            <th>Project</th>
            <th>Date</th>
            <th>Modified By</th>
            <th>Modified On</th>
            <th>Actions</th>
        </tr>"""
        for review in reviews:
            modified_on = review.modified_on.strftime("%m/%d/%y %H:%M")
            date = review.date.strftime("%m/%d/%y")
            project = "<a href=\"/projects/%s\" title=\"View '%s'\">%s</a>" % (review.project.url, review.project.name, review.project.name)
            content += """<tr>
                <td><a title="%s" href="/projects/%s/reviews/%s">%s</a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td><a href="/admin/reviews/edit/%s" title="Edit %s">Edit</a> | <a href="/admin/reviews/delete/%s" title="Delete %s">Delete</a></td>
            </tr>""" % (review.publication, review.project.url, review.url, review.publication, review.author, project, date, review.modified_by.email(), modified_on, review.url, review.publication, review.url, review.publication)
        content += "</table>"
        sidebar = """<h2>Review Administration</h2>
        <p>You can edit, delete, and reorder the reviews in the datastore by
        clicking the appropriate link. You can also <a href="/admin/reviews/add"
        title="Add a review">add a review</a> to the datastore.</p>"""
        person = Person()
        people = person.get_featured()
        link = Link(group="special_menu")
        menu = link.get_group()
        template_values = {
            'content' : content,
            'sidebar' : sidebar,
            'title' : "Reviews",
            'menu' : menu,
            'people' : people
        }
        path = os.path.join(os.path.dirname(__file__), "../../template/hauk", 'secondary.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/admin/reviews', ListReviewsHandler),
    ('/admin/reviews/', ListReviewsHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
