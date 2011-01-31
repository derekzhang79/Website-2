import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.api import memcache
from models import *

class AddReviewHandler(webapp.RequestHandler):
  def get(self):
    projects = ProjectData.all().order("name ASC").fetch(1000)
    project_options = ""
    for project in projects:
      project_options += "<option value=\"%s\">%s</option>\n" % (project.url, project.name)
    content = """
    <h2></h2>
    <p>
      <form method="post">
        <label>Author:</label>
        <input type="text" name="author" /><br />
        <label>Publication:</label>
        <input type="text" name="publication" /><br />
        <label>Location:</label>
        <input type="text" name="location" /><br />
        <label>Excerpt:</label>
        <textarea name="excerpt"></textarea><br />
        <label>Project:</label>
        <select name="project">
          %s
        </select>
        <input type="submit" />
      </form>
    </p>""" % project_options
    template_values = {
      'title' : 'Add Review',
      'content' : content
    }
    path = os.path.join(os.path.dirname(__file__), '../../', 'template', 'secondary.html')
    self.response.out.write(template.render(path, template_values))
  
  def post(self):
    review_data = ReviewData()
    review_data.author = self.request.get('author')
    review_data.publication = self.request.get('publication')
    review_data.location = self.request.get('location')
    review_data.excerpt = self.request.get('excerpt')
    review_data.project = ProjectData.all().filter("url =", self.request.get(project)).get()
    review_data.put()
    self.redirect('/admin')

def main():
  application = webapp.WSGIApplication([('/admin/review/add', AddReviewHandler)], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()