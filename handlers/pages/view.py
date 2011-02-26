#/handlers/pages/view.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/25/11
#
#Displays a page from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.page import Page
from errors.page import PageNotFoundException
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class ViewPageHandler(webapp.RequestHandler):
    def get(self, url):
        url = url.strip().strip("/")
        page = Page(url=url)
        try:
            page.get()
        except PageNotFoundException:
            self.response.out.write("404")
        else:
            template_values = {
                'content' : page.content,
                'title' : page.title,
                'sidebar' : page.sidebar
            }
            path = os.path.join(os.path.dirname(__file__), '../../template', 'secondary.html')
            self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/(.*)', ViewPageHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
