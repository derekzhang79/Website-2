import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.api import memcache
from models import *

class UploadImageHandler(webapp.RequestHandler):
  def get(self):
    projects = ProjectData.all().order("name ASC").fetch(1000)
    project_options = ""
    for project in projects:
      project_options += "<option value=\"%s\">%s</option>\n" % (project.url, project.name)
    content = """
    <h2></h2>
    <p>
      <form method="post" enctype="multipart/form-data">
        <label>Shortname:</label>
        <input type="text" name="shortname" /><br />
        <label>Project:</label>
        <select name="project">
          %s
        </select><br />
        <label>File:</label>
        <input type="file" name="image" /><br />
        <input type="submit" />
      </form>
    </p>""" % project_options
    template_values = {
      'title' : 'Upload Image',
      'content' : content
    }
    path = os.path.join(os.path.dirname(__file__), '../../', 'template', 'secondary.html')
    self.response.out.write(template.render(path, template_values))
  
  def post(self):
    image_data = ImageData()
    image_data.image = self.request.get('image')
    image_data.shortname = self.request.get('shortname')
    image_data.project = self.request.get('project')
    image_data.put()
    self.redirect('/admin')


def main():
  application = webapp.WSGIApplication([('/admin/images/add', UploadImageHandler)], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()