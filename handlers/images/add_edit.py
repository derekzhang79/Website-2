#/handlers/images/add_edit.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/26/11
#
#Handles requests to add or edit an image.

import sys, os, logging
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.image import Image
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class AddEditImageHandler(webapp.RequestHandler):
    def get(self, image=None):
        if image is None:
            img = ""
            shortname = ""
            action = "Add"
            name = ""
        else:
            image_data = Image(shortname=image)
            image_data.get()
            img = '<img src="/image/%s" /><br />' % image_data.shortname
            shortname = image_data.shortname
            action = "Edit"
            name = ' "%s"' % shortname
        content = """<h2>%s Image%s</h2>
            <p>
                <form enctype="multipart/form-data" method="post">
                    %s
                    <label>Image</label>
                    <input type="file" name="image" /><br />
                    <label>Short Name</label>
                    <input type="text" name="shortname" value="%s" /><br />
                    <input type="submit">
                </form>
            </p>""" % (action, name, img, shortname)
        sidebar = """<h2>Hint!</h2>
        <p><b>Image</b>: Choose the image file you want to upload.<br />
        <b>Short Name</b>: Choose the short name for the image. This will be the
        URL for the image, so a shortname of 'logo' will make the image
        accessible at http://www.secondbit.org/images/logo.
        </p>"""
        title = "%s Image%s" % (action, name)
        template_values = {
            'title' : title,
            'content' : content,
            'sidebar' : sidebar
        }
        path = os.path.join(os.path.dirname(__file__), "../../template/hauk", "secondary.html")
        self.response.out.write(template.render(path, template_values))

    def post(self, shortname=None):
        image = Image()
        if shortname is not None:
            image.shortname = shortname
            image.get()
        try:
            uploaded_image = self.request.POST["image"]
        except KeyError:
            pass
        else:
            if uploaded_image is not None and uploaded_image is not "":
                logging.info(JSON.dumps(uploaded_image))
                image.image = uploaded_image.value
                image.mimetype = uploaded_image.type
        image.shortname = self.request.POST["shortname"]
        image.save()
        self.redirect("/%s" % image.shortname)

application = webapp.WSGIApplication([
                                ('/admin/images/add', AddEditImageHandler),
                                ('/admin/images/edit/(.*)', AddEditImageHandler),
                                ('/admin/images/add/', AddEditImageHandler)
                                ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
