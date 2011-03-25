#/handlers/images/list.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/26/11
#
#Displays a list of images from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.image import Image
from models.person import Person
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class ListImagesHandler(webapp.RequestHandler):
    def get(self):
        image = Image()
        images = image.get_list()
        content = """<h2>Images</h2>
        <table>
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
            original = 'N/A'
            if image.original is not None:
                original = "<a href=\"/images/%s\">%s</a>" % (image.original.shortname, image.original.shortname)
            uploaded_on  = image.uploaded_on.strftime("%m/%d/%y %H:%M")
            content += """<tr>
                <td><a href="/image/%s" title="View %s">%s</a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td><a href="/admin/images/edit/%s" title="Edit %s">Edit</a> |
                <a href="/admin/images/resize/%s" title="Resize %s">Resize</a> | <a href="/admin/images/delete/%s" title="Delete %s">Delete</a></td>
            </tr>""" % (image.shortname, image.shortname, image.shortname, image.width, image.height, original, image.mimetype, image.uploaded_by.email(), uploaded_on, image.shortname, image.shortname, image.shortname, image.shortname, image.shortname, image.shortname)
        content += "</table>"
        sidebar = """<h2>Image Administration</h2>
        <p>You can edit, delete, and resize the images in the datastore by
        clicking the appropriate link. You can also <a href="/admin/images/add"
        title="Upload an image">upload an image</a> to the datastore.</p>"""
        person = Person()
        people = person.get_featured()
        template_values = {
            'content' : content,
            'sidebar' : sidebar,
            'title' : 'Images',
            'people': people
        }
        path = os.path.join(os.path.dirname(__file__), "../../template/hauk", 'secondary.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/admin/images', ListImagesHandler),
    ('/admin/images/', ListImagesHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
