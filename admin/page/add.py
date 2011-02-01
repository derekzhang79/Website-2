import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.api import memcache
from models import *

class AddPageHandler(webapp.RequestHandler):
  def get(self):
    content = """
    <h2></h2>
    <p>
      <form method="post">
        <label>Title:</label>
        <input type="text" name="title" /><br />
        <label>Content:</label>
        <textarea name="content"></textarea><br />
        <label>Sidebar:</label>
        <textarea name="sidebar"></textarea><br />
        <label>URL:</label>
        <input type="text" name="url" /><br />
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
    page_data = PageData()
    page_data.title = self.request.get('title')
    page_data.content = self.request.get('content')
    page_data.sidebar = self.request.get('sidebar')
    page_data.url = self.request.get('url')
    page_data.put()
    self.redirect('/admin')

def main():
  application = webapp.WSGIApplication([('/admin/page/add', AddPageHandler)], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()