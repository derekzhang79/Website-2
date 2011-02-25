#/handlers/images/list.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/25/11
#
#Displays a list of images from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.image import Image
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class ListImagesHandler(webapp.RequestHandler):
    def get(self):
        image = Image()
        images = image.get_list()
        content = """<table>
        <tr>
            <th>Name</th>
            <th>Width</th>
            <th>Height</th>
            <th>Original</th>
            <th>Mimetype</th>
            <th>Uploader</th>
            <th>Uploaded On</th>
            <th>Actions</th>
        </tr>"""
        for image in images:
            content += """<tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td><a href="/image/%s">%s</a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td><a href="/admin/images/edit/%s" title="Edit %s">Edit</a> | <a href="/admin/images/delete/%s" title="Delete %s">Delete</a></td>
            </tr>""" % (image.shortname, image.width, image.height, image.original.shortname, image.original.shortname, image.mimetype, image.uploaded_by.email(), image.uploaded_on, image.shortname, image.shortname, image.shortname, image.shortname)
        self.response.out.write(content)

application = webapp.WSGIApplication([
    ('/admin/images', ListImagesHandler),
    ('/admin/images/', ListImagesHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
