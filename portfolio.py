import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template

class PortfolioHandler(webapp.RequestHandler):
    def get(self):
        template_values = {
        }
        path = os.path.join(os.path.dirname(__file__), 'template', 'portfolio.html')
        self.response.out.write(template.render(path, template_values))

def main():
    application = webapp.WSGIApplication([('/portfolio', PortfolioHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
