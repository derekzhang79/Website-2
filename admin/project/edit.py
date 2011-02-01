import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.api import memcache
from models import *

class EditProjectHandler(webapp.RequestHandler):
  def get(self, url=None):
    if url == None:
      self.redirect('/admin/project/add')
    project_data = ProjectData().all().filter("url =", url).get()
    is_project = ""
    is_product = ""
    if project_data.nature == "project":
      is_project = " selected=\"selected\""
    else:
      is_product = " selected=\"selected\""
    content = """
    <h2></h2>
    <p>
      <form method="post" enctype="multipart/form-data">
        <label>Name:</label>
        <input type="text" name="name" value="%s" /><br />
        <label>Type:</label>
        <select name="nature">
          <option value="project"%s>Project</option>
          <option value="product"%s>Product</option>
        </select><br />
        <label>Description:</label>
        <textarea name="description">%s</textarea><br />
        <label>Short Description:</label>
        <textarea name="short_description">%s</textarea><br />
        <label>URL:</label>
        <input type="text" name="url" value="%s" /><br />
        <label>Screenshot:</label>
        <input type="file" name="screenshot" /><br />
        Current: <img src="/projects/%s/screenshot.png"><br />
        <label>Icon:</label>
        <input type="file" name="icon" /><br />
        Current: <img src="/projects/%s/icon.png"><br />
        <input type="submit" />
      </form>
    </p>""" % (project_data.name, is_project, is_product, project_data.description, project_data.short_description, project_data.url, project_data.url, project_data.url)
    template_values = {
      'title' : 'Edit Project: %s' % project_data.name,
      'content' : content
    }
    path = os.path.join(os.path.dirname(__file__), '../../', 'template', 'secondary.html')
    self.response.out.write(template.render(path, template_values))
  
  def post(self, url):
    project_data = ProjectData().all().filter("url =", url).get()
    if self.request.get('nature'):
      project_data.nature = self.request.get('nature')
    if self.request.get('name'):
      project_data.name = self.request.get('name')
    if self.request.get('description'):
      project_data.description = self.request.get('description')
    if self.request.get('short_description'):
      project_data.short_description = self.request.get('short_description')
    if self.request.POST('screenshot'):
      project_data.screenshot = self.request.POST('screenshot').data
      project_data.screenshot_mimetype = self.request.POST('screenshot').type
    if self.request.POST('icon'):
      project_data.icon = self.request.POST('icon').data
      project_data.icon_mimetype = self.request.POST('icon').type
    if self.request.get('url'):
      project_data.url = self.request.get('url')
    project_data.put()
    self.redirect('/admin')

def main():
  application = webapp.WSGIApplication([('/admin/project/edit', EditProjectHandler),
                                        ('/admin/project/edit/(.*)', EditProjectHandler)], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()