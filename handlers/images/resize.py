#/handlers/images/resize.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/26/11
#
#Displays a form to resize an image in the datastore, and calls the method 
#to resize the image

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.image import Image
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class ResizeImageHandler(webapp.RequestHandler):
    def get(self, shortname):
        image = Image(shortname=shortname)
        image.get()
        content = """<h2>Resize Image "%s"</h2>
            <p>
                <form method="post">
                    <img src="/image/%s" /><br />
                    <label>Width</label>
                    <input type="text" value="%s" name="width" /><br />
                    <label>Height</label>
                    <input type="text" value="%s" name="height" /><br />
                    <input type="submit" />
                </form>
            </p>""" % (image.shortname, image.shortname, image.width, image.height)
        sidebar = "<h2>Hints!</h2>
        <p><b>Width</b>: The <i>maximum</i> width you'd like the resized image
        to be.<br />
        <b>Height</b>: The <i>maximum</i> height you'd like the resized image to
        be.<br />
        <br />
        <i>Note: The image will preserve its aspect ratio, and not stretch or
        crop. It will use whichever will result in a <u>smaller</u> image, of
        the height and width. A new <u>copy</u> of the image will be created as
        shortname_widthxheight, using the values you enter.</i></p>"""
        template_values = {
            'content' : content,
            'title' : 'Resize Image "%s"' % image.shortname,
            'sidebar' : sidebar
        }
        path = os.path.join(os.path.dirname(__file__), '../../template/hauk', 'secondary.html')
        self.response.out.write(template.render(path, template_values))

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
