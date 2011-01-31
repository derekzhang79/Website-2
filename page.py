import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.api import memcache
from models import PageData

class PageHandler(webapp.RequestHandler):
    def get(self, url):
        url = url.strip().strip("/")
        page = memcache.get("/page/%s" % url)
        if page is None:
          page = PageData.all().filter("url =", url).get()
        if page is not None:
          template_values = {
            'title' : page.title,
            'content' : page.content,
            'sidebar' : page.sidebar
          }
          path = os.path.join(os.path.dirname(__file__), 'template', 'secondary.html')
          self.response.out.write(template.render(path, template_values))
        else:
          self.redirect("/404")

def main():
    application = webapp.WSGIApplication([('/(.*)', PageHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()