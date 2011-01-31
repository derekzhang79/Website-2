import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.api import memcache
from models import *

class EditReviewHandler(webapp.RequestHandler):
  def get(self, review_id=None):
    review_data = ReviewData.all().filter("id =", review_id).get()
    projects = ProjectData.all().order("name ASC").fetch(1000)
    project_options = ""
    for project in projects:
      is_selected = ""
      if project.id == review_data.project.id:
        is_selected = " selected=\"selected\""
      project_options += "<option value=\"%s\"%s>%s</option>\n" % (project.url, project.name, is_selected)
    content = """
    <h2></h2>
    <p>
      <form method="post">
        <label>Author:</label>
        <input type="text" name="author" value="%s" /><br />
        <label>Publication:</label>
        <input type="text" name="publication" value="%s" /><br />
        <label>Location:</label>
        <input type="text" name="location" value="%s" /><br />
        <label>Excerpt:</label>
        <textarea name="excerpt">%s</textarea><br />
        <label>Project:</label>
        <select name="project">
          %s
        </select>
        <input type="submit" />
      </form>
    </p>""" % (review_data.author, review_data.publication, review_data.location, review_data.excerpt, project_options)
    template_values = {
      'title' : 'Edit Review of %s', review_data.project.name,
      'content' : content
    }
    path = os.path.join(os.path.dirname(__file__), '../../', 'template', 'secondary.html')
    self.response.out.write(template.render(path, template_values))
  
  def post(self, review_id=None):
    review_data = ReviewData().all().filter('id =', review_id).get()
    review_data.author = self.request.get('author')
    review_data.publication = self.request.get('publication')
    review_data.location = self.request.get('location')
    review_data.excerpt = self.request.get('excerpt')
    review_data.project = ProjectData.all().filter("url =", self.request.get(project)).get()
    review_data.put()
    self.redirect('/admin')

def main():
  application = webapp.WSGIApplication([('/admin/review/edit', EditReviewHandler),
                                        ('/admin/review/edit/(.*)', EditReviewHandler)], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()