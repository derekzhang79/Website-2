#/handlers/images/add_edit.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/22/11
#
#Handles requests to add or edit an image.

from models.image import Image
from models.site import Site
from google.appengine.ext import webapp


class AddEditImageHandler(webapp.RequestHandler):
    def get(self):
        pass

    def post(self):
        pass

application = webapp.WSGIApplication([
                                ('/admin/images/add', AddEditImageHandler),
                                ('/admin/images/edit/*', AddEditImageHandler),
                                ('/admin/images/add/', AddEditImageHandler)
                                ], debug=True)

def main():
    webapp.util.run_wsgi_app(application)

if __name__ == "__main__":
    main()
