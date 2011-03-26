#/handlers/services/images.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/1/11
#
#Displays an image from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.image import Image
from models.service import Service
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app

from datetime import datetime, timedelta

from errors.image import ImageNotFoundException

class ServiceIconHandler(webapp.RequestHandler):
    def get(self, service_url):
        service = Service(url=service_url)
        try:
            service.get()
        except ServiceNotFoundException:
            self.response.out.write("Error, service not found.")
        if service.icon is None:
            self.response.out.write("Error, service has no icon.")
        else:
            image = Image(datastore=service.icon)
            try:
                image.get()
            except ImageNotFoundException:
                self.response.out.write("Error, image not found.")
            else:
                self.response.headers['Content-Type'] = image.mimetype
                self.response.headers['Expires'] = (datetime.today() + timedelta(days=7)).strftime("%a, %d %b %Y %Z")
                self.response.out.write(image.image)

application = webapp.WSGIApplication([
    ('/services/([^/]*)/icon', ServiceIconHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
