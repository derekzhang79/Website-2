import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.api import memcache
from models import *

class EditPageHandler(webapp.RequestHandler):
  def get(self, url=None):
    if url == None:
      self.redirect('/admin/page/add')
    page_data = PageData.all().filter("url =", url).get()
    content = """
    <h2></h2>
    <p>
      <form method="post">
        <label>Title:</label>
        <input type="text" name="title" value="%s" /><br />
        <label>Content:</label>
        <textarea name="content">%s</textarea><br />
        <label>Sidebar:</label>
        <textarea name="sidebar">%s</textarea><br />
        <label>URL:</label>
        <input type="text" name="url" value="%s" /><br />
        <input type="submit" />
      </form>
    </p>""" % (page_data.title, page_data.content, page_data.sidebar, page_data.url)
    template_values = {
      'title' : 'Edit Page: %s' % page_data.title,
      'content' : content
    }
    path = os.path.join(os.path.dirname(__file__), '../../', 'template', 'secondary.html')
    self.response.out.write(template.render(path, template_values))
  
  def post(self, url=None):
    page_data = PageData().all().filter("url =", url).get()
    page_data.title = self.request.get('title')
    page_data.content = self.request.get('content')
    page_data.sidebar = self.request.get('sidebar')
    page_data.url = self.request.get('url')
    page_data.put()
    self.redirect('/admin')

def main():
  application = webapp.WSGIApplication([('/admin/page/edit', EditPageHandler),
                                        ('/admin/page/edit/(.*)', EditPageHandler)], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()