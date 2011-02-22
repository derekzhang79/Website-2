from google.appengine.ext import webapp
from google.appengine.api import memcache, images
from models import ImageData, ProjectData, ResizedImageData

class ImageHandler(webapp.RequestHandler):
    def get(self, project, url):
      project = project.strip().strip("/")
      project_data = ProjectData.all().filter("url =", project).get()
      if project_data is None:
        self.error(404)
      url = url.strip().strip("/")
      image = ImageData.all().filter("shortname =", url).filter("project =", project_data).get()
      if image is not None:
        self.response.headers['Content-Type'] = image.mimetype
        self.response.out.write(image.image)
      else:
        self.error(404)

class ResizedImageHandler(webapp.RequestHandler):
  def get(self, image_shortname, width, height):
    image_data = ResizedImageData().all().filter("shortname =", image_shortname).filter("height =", height).filter("width =", width).get()
    if image_data is None:
      self.error(404)
    else:
      self.response.headers['Content-Type'] = "image/png"
      self.response.out.write(image_data.data)
      
def main():
    application = webapp.WSGIApplication([('/projects/(.*)/images/(.*)', ImageHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()