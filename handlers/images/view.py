#/handlers/images/view.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/22/11
#
#Displays an image from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.image import Image
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from datetime import datetime, timedelta

class ViewImageHandler(webapp.RequestHandler):
    def get(self, shortname):
        image = Image(shortname=shortname)
        image.get()
        self.response.headers['Content-Type'] = image.mimetype
        self.response.headers['Expires'] = (datetime.today() + timedelta(days=7)).strftime("%a, %d %b %Y %Z")
        self.response.out.write(image.image)

application = webapp.WSGIApplication([
    ('/image/(.*)', ViewImageHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
