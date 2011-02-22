#/handlers/images/resize.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/22/11
#
#Displays a form to resize an image in the datastore, and calls the method 
#to resize the image

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.image import Image
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class ResizeImageHandler(webapp.RequestHandler):
    def get(self, shortname):
        image = Image(shortname=shortname)
        image.get()
        self.response.out.write("""
            <form method="post">
                <img src="/image/%s" /><br />
                <label>Width</label>
                <input type="text" value="%s" name="width" /><br />
                <label>Height</label>
                <input type="text" value="%s" name="height" /><br />
                <input type="submit" />
            </form>""" % (image.shortname, image.width, image.height))

    def post(self, shortname):
        image = Image(shortname=shortname)
        image.get()
        height = int(self.request.get("height"))
        width = int(self.request.get("width"))
        image.resize(height=height, width=width)
        self.redirect("/image/%s" % image.shortname)

application = webapp.WSGIApplication([
    ('/admin/images/resize/(.*)', ResizeImageHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
