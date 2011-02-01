import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.api import memcache
from models import *

class UploadFileHandler(webapp.RequestHandler):
  def get(self):
    content = """
    <h2></h2>
    <p>
      <form method="post" enctype="multipart/form-data">
        <label>Shortname:</label>
        <input type="text" name="shortname" /><br />
        <label>File:</label>
        <input type="file" name="upload" /><br />
        <input type="submit" />
      </form>
    </p>"""
    template_values = {
      'title' : 'Upload File',
      'content' : content
    }
    path = os.path.join(os.path.dirname(__file__), '../../', 'template', 'secondary.html')
    self.response.out.write(template.render(path, template_values))
  
  def post(self):
    upload_data = UploadData()
    upload_data.upload = self.request.POST('upload').data
    upload_data.mimetype = self.request.POST('upload').type
    upload_data.shortname = self.request.get('shortname')
    upload_data.put()
    self.redirect('/admin')


def main():
  application = webapp.WSGIApplication([('/admin/files/add', UploadFileHandler)], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()