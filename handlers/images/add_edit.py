#/handlers/images/add_edit.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/22/11
#
#Handles requests to add or edit an image.

import sys, os, logging
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.image import Image
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class AddEditImageHandler(webapp.RequestHandler):
    def get(self, image=None):
        if image is None:
            img = ""
            shortname = ""
        else:
            image_data = Image(shortname=image)
            image_data.get()
            img = '<img src="/images/%s" />' % image_data.shortname
            shortname = image_data.shortname
        self.response.out.write("""
            <form enctype="multipart/form-data" method="post">
                %s
                <label>Image</label>
                <input type="file" name="image" /><br />
                <label>Short Name</label>
                <input type="text" name="shortname" value="%s" /><br />
                <input type="submit">
            </form>""" % (img, shortname))

    def post(self, shortname=None):
        image = Image()
        if shortname is not None:
            image.shortname = shortname
            image.get()
        image.image = self.request.POST["image"].value
        image.mimetype = self.request.POST["image"].type
        image.shortname = self.request.POST["shortname"]
        image.save()

application = webapp.WSGIApplication([
                                ('/admin/images/add', AddEditImageHandler),
                                ('/admin/images/edit/(.*)', AddEditImageHandler),
                                ('/admin/images/add/', AddEditImageHandler)
                                ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
