import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template

class DashboardHandler(webapp.RequestHandler):
    def get(self, url=None):
        template_values = {
          'title' : 'Admin Dashboard'
        }
        path = os.path.join(os.path.dirname(__file__), '../', 'template', 'secondary.html')
        self.response.out.write(template.render(path, template_values))

def main():
    application = webapp.WSGIApplication([('/admin', DashboardHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()