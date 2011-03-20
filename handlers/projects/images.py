#/handlers/projects/images.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/26/11
#
#Displays an image from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.image import Image
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from errors.image import ImageNotFoundException

class ProjectImageHandler(webapp.RequestHandler):
    def get(self, shortname):
        shortname = shortname.rstrip(".png")
        image = Image(shortname=shortname)
        image.get()
        self.response.headers['Content-Type'] = image.mimetype
        self.response.out.write(image.image)

class ProjectThumbHandler(webapp.RequestHandler):
    def get(self, shortname):
        shortname = shortname.rstrip(".png")
        image = Image(shortname=shortname)
        image.get()
        if image.width > 166:
            height = image.height
        elif image.width < 166:
            width = image.width
            height = image.height
            factor = 2
            while width < 166:
                width = width * factor
                height = height * factor
                factor = factor * factor
        else:
            height = image.height
        thumb = Image(shortname="%s_%sx%s" % (shortname, 166, height))
        try:
            thumb.get()
        except ImageNotFoundException:
            if image.width != 166:
                image.rescale(height=height, width=166, crop=True)
            thumb = image
        self.response.headers['Content-Type'] = thumb.mimetype
        self.response.out.write(thumb.image)

application = webapp.WSGIApplication([
    ('/projects/[^/]*/image/(.*)', ProjectImageHandler),
    ('/projects/[^/]*/thumb/(.*)', ProjectThumbHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
