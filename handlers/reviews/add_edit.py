#/handlers/review/add_edit.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/10/11
#
#Handles requests to add or edit a review.

import sys, os, logging
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.review import Review
from models.link import Link
from models.project import Project
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class AddEditReviewHandler(webapp.RequestHandler):
    def get(self, url=None):
        if url is None:
            review = Review()
            review.author = ""
            review.publication = ""
            review.reference = ""
            review.url = ""
            review.excerpt = ""
            review.content = ""
            review.project = ""
            projects_string = ""
            review.date = ""
            review.featured = False
            featured = ""
            action = "Add"
            name = ''
        else:
            review = Review(url=url)
            review.get()
            featured = ""
            if review.featured:
                featured = " checked=\"checked\""
            projects_string = ""
            action = "Edit"
            name = " '%s'" % review.url
        project = Project()
        projects = project.get_list()
        for project in projects:
            selected = ""
            if project.key() == review.project.key():
                selected = " selected=\"selected\""
            projects_string += "\n<option value=\"%s\"%s>%s</option>" % (project.key(), selected, project.name)
        content = """<h2>%s Review%s</h2>
        <p>
            <form method="post">
                <label>Author</label>
                <input type="text" name="author" value="%s" /><br />
                <label>Publication</label>
                <input type="text" name="publication" value="%s" /><br />
                <label>Reference</label>
                <input type="text" name="reference" value="%s" /><br />
                <label>URL</label>
                <input type="text" name="url" value="%s" /><br />
                <label>Excerpt</label>
                <textarea name="excerpt">%s</textarea><br />
                <label>Content</label>
                <textarea name="content">%s</textarea><br />
                <label>Project</label>
                <select name="project">%s</select>
                <label>Date</label>
                <input type="text" value="%s" /><br />
                <label>Featured?</label>
                <input type="checkbox" name="featured" value="True"%s /><br />
                <input type="submit">
            </form>
        </p>""" % (action, name, review.author, review.publication, review.reference, review.url, review.excerpt, review.content, projects_string, review.date, featured)
        sidebar = """<h2>Hint!</h2>
            <p>
                <b>Name:</b> The text that is linked, like <a href="#">this</a>.<br />
                <b>Title:</b> The text that appears when the link is hovered
                    over. Like <a href="#" title="This is a title.">this</a>.<br
                    />
                <b>URL:</b> The URL you're linking to.<br />
                <b>Weight:</b> The 'weight' of the link, which determines how
                    the links in the group are ordered. The heavier the link,
                    the lower it is ordered.<br />
                <b>Group:</b> The 'group' the link is part of. Could be
                    'special_menu' or 'project_android2cloud'.
            </p>"""
        template_values = {
            'content' : content,
            'title' : '%s Review%s' % (action, name),
            'sidebar': sidebar
        }
        path = os.path.join(os.path.dirname(__file__), "../../template/hauk", 'secondary.html')
        self.response.out.write(template.render(path, template_values))
            
    def post(self, key=None):
        link = Link()
        if key is not None:
            link.key = key
            link.get()
        link.name = self.request.POST['name']
        link.title = self.request.POST['title']
        link.url = self.request.POST['url']
        link.weight = self.request.POST['weight']
        link.group = self.request.POST['group']
        link.save()
        self.redirect("/admin/links")

application = webapp.WSGIApplication([
                                ('/admin/reviewss/add', AddEditReviewHandler),
                                ('/admin/reviews/edit/(.*)', AddEditReviewHandler),
                                ('/admin/reviews/add/', AddEditReviewHandler)
                                ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
