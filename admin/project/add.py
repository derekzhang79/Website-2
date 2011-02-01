import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.api import memcache
from models import *

class AddProjectHandler(webapp.RequestHandler):
  def get(self):
    content = """
    <h2></h2>
    <p>
      <form method="post" enctype="multipart/form-data">
        <label>Name:</label>
        <input type="text" name="name" /><br />
        <label>Type:</label>
        <select name="nature">
          <option value="project">Project</option>
          <option value="product">Product</option>
        </select><br />
        <label>Description:</label>
        <textarea name="description"></textarea><br />
        <label>Short Description:</label>
        <textarea name="short_description"></textarea><br />
        <label>URL:</label>
        <input type="text" name="url" /><br />
        <label>Screenshot:</label>
        <input type="file" name="screenshot" /><br />
        <label>Icon:</label>
        <input type="file" name="icon" /><br />
        <input type="submit" />
      </form>
    </p>"""
    template_values = {
      'title' : 'Add Page',
      'content' : content
    }
    path = os.path.join(os.path.dirname(__file__), '../../', 'template', 'secondary.html')
    self.response.out.write(template.render(path, template_values))
  
  def post(self):
    project_data = ProjectData()
    project_data.nature = self.request.get('nature')
    project_data.name = self.request.get('name')
    project_data.description = self.request.get('description')
    project_data.short_description = self.request.get('short_description')
    project_data.screenshot = self.request.POST('screenshot').value
    project_data.screenshot_mimetype = self.request.POST('screenshot').type
    project_data.icon = self.request.POST('icon').value
    project_data.icon_mimetype = self.request.POST('icon').type
    project_data.url = self.request.get('url')
    project_data.put()
    self.redirect('/admin')

def main():
  application = webapp.WSGIApplication([('/admin/project/add', AddProjectHandler)], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()