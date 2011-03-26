#/handlers/projects/view_all.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/22/11
#
#Displays all the projects in the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.project import Project
from models.link import Link
from models.person import Person
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class ViewProjectsHandler(webapp.RequestHandler):
    def get(self):
        project = Project()
        projects = project.get_list()
        person = Person()
        people = person.get_featured()
        header = """<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
        <script type="text/javascript" src="/js/fancybox/fancybox/jquery.fancybox-1.3.4.pack.js"></script>
        <link rel="stylesheet" href="/js/fancybox/fancybox/jquery.fancybox-1.3.4.css" />
        <script type="text/javascript">
            $(document).ready(function() {
                $("a.fancybox").fancybox();
            });
        </script>"""
        content = ""
        for project in projects:
            images = db.get(project.images)
            images_string = ""
            count = 1
            for image in images:
                middle_class = ""
                if count == 2:
                    middle_class = " thumb-middle"
                    count = count + 1
                elif count >= 3:
                    count = 1
                else:
                    count = count + 1
                images_string += """<a href="/projects/%s/image/%s.png" class="fancybox">
                    <img src="/projects/%s/thumb/%s.png" class="portfolio-thumb%s" width="166" />
                </a>""" % (project.url, image.shortname, project.url, image.shortname, middle_class)
            content += """<h2><a href="/projects/%s" title="View %s">%s</a></h2>
            %s
            %s""" % (project.url, project.name, project.name, images_string, project.excerpt)
        sidebar = """<h2>Your Project Here</h2>
        <p>We're looking to do cool stuff all the time. If you have a project or
        an idea but need some help on the tech end, <a href="/contact"
        title="Contact Information for Second Bit">get in touch</a> and we'll
        give you some feedback and a quote.</p>

        <h2>Want to Get Involved?</h2>
        <p>We love getting other people involved in our projects. The more the
        merrier. We put the source code for all the projects we can accept
        contributions for on <a href="http://www.github.com/secondbit"
        title="Second Bit on Github">our Github page</a>, so fork us and send us
        a pull request.</p>"""
        link = Link(group="special_menu")
        menu = link.get_group()
        template_values = {
            'subheader_title' : "Check out some of our work.",
            'title' : "Projects",
            'header': header,
            'content' : content,
            'sidebar' : sidebar,
            'people' : people,
            'menu' : menu
        }
        path = os.path.join(os.path.dirname(__file__), '../../template/hauk', 'secondary.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/projects/', ViewProjectsHandler),
    ('/projects', ViewProjectsHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
