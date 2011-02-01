from google.appengine.ext import webapp
from google.appengine.api import memcache
from models import ImageData

class UploadHandler(webapp.RequestHandler):
    def get(self, url):
        url = url.strip().strip("/")
        upload = UploadData.all().filter("shortname =", url).get()
        if upload is not None:
          self.response.headers['Content-Type'] = upload.mimetype
          self.response.out.write(upload.upload)
        else:
          self.error(404)

def main():
    application = webapp.WSGIApplication([('/uploads/(.*)', UploadHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()