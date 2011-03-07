import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template

from models.service import Service
from models.project import Project
from models.link import Link

class MainHandler(webapp.RequestHandler):
    def get(self):
        service_model = Service()
        services = service_model.get_featured()
        project_model = Project()
        projects = project_model.get_featured()
        menu_model = Link(group="special_menu")
        menu_links = menu_model.get_group()
        template_values = {
            'services' : services,
            'projects' : projects,
            'menu' : menu_links
        }
        path = os.path.join(os.path.dirname(__file__), 'template/hauk', 'index.html')
        self.response.out.write(template.render(path, template_values))

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
