from google.appengine.ext import webapp
from google.appengine.api import memcache, images
from models import ImageData, ProjectData, ResizedImageData

class ImageResizeHandler(webapp.RequestHandler):
  def get(self, project_url, image_shortname):
    image_shortname = image_shortname.strip().strip("/")
    project_url = project_url.strip().strip("/")
    project_data = ProjectData().all().filter("url =", project_url).get()
    if project_data is None:
      self.error(404)
    image_data = ImageData().all().filter("shortname =", image_shortname).filter("project =", project_data).get()
    if image_data is None:
      self.error(404)
    else:
      content = """
    <h2></h2>
    <p>
      <form method="post">
        Image: <img src="/projects/%s/images/%s" /><br />
        <label>Width:</label>
        <input type="text" name="width" /><br />
        <label>Height:</label>
        <input type="text" name="height" /><br />
        <input type="submit" />
      </form>
    </p>""" % (project_data.url, image_data.shortname)
    template_values = {
      'title' : 'Resize Image',
      'content' : content
    }
    path = os.path.join(os.path.dirname(__file__), '../../', 'template', 'secondary.html')
    self.response.out.write(template.render(path, template_values))
  
  def post(self, project_url, image_shortname):
    image_shortname = image_shortname.strip().strip("/")
    project_url = project_url.strip().strip("/")
    project_data = ProjectData().all().filter("url =", project_url).get()
    if project_data is None:
      self.error(404)
    image_data = ImageData().all().filter("shortname =", image_shortname).filter("project =", project_data).get()
    if image_data is None:
      self.error(404)
    resized_image = ResizedImageData()
    resized_image.image = image_data
    resized_image.shortname = image_data.shortname
    resized_image.height = self.request.get("height")
    resized_image.width = self.request.get("width")
    resized_image.data = images.resize(image_data.image, resized_image.width, resized_image.height)
      
def main():
    application = webapp.WSGIApplication([('/projects/(.*)/images/(.*)', ImageHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()