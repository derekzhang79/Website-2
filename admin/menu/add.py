import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.api import memcache
from models import *

class AddMenuItemHandler(webapp.RequestHandler):
  def get(self):
    content = """
    <h2></h2>
    <p>
      <form method="post">
        <label>Name:</label>
        <input type="text" name="name" /><br />
        <label>Title:</label>
        <input type="text" name="title" /><br />
        <label>URL:</label>
        <input type="text" name="url" /><br />
        <input type="submit" />
      </form>
    </p>"""
    template_values = {
      'title' : 'Add Menu Link',
      'content' : content
    }
    path = os.path.join(os.path.dirname(__file__), '../../', 'template', 'secondary.html')
    self.response.out.write(template.render(path, template_values))
  
  def post(self):
    menu_data = MenuData()
    menu_data.title = self.request.get('title')
    menu_data.name = self.request.get('name')
    menu_data.url = self.request.get('url')
    menu_data.weight = 0;
    menu_data.put()
    self.redirect('/admin')


def main():
  application = webapp.WSGIApplication([('/admin/menu/add', AddMenuItemHandler)], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()