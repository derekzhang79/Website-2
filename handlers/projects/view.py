#/handlers/projects/view.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/26/11
#
#Displays a page from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.project import Project
from errors.project import ProjectNotFoundException
from models.link import Link
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class ViewProjectHandler(webapp.RequestHandler):
    def get(self, url):
        url = url.strip().strip("/")
        project = Project(url=url)
        link = Link(group="project_%s" % project.url)
        links = link.get_group()
        try:
            project.get()
        except ProjectNotFoundException:
            self.response.out.write("404")
        else:
            header = """<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
            <script type="text/javascript" src="/js/fancybox/fancybox/jquery.fancybox-1.3.4.pack.js"></script>
            <link rel="stylesheet" href="/js/fancybox/fancybox/jquery.fancybox-1.3.4.css" />
            <script type="text/javascript">
                $(document).ready(function() {
                    $("a.fancybox").fancybox();
                });
            </script>"""
            link = Link(group="project_%s" % project.url)
            links = link.get_group()
            links_string = """<h2>Project Links</h2>
            <ul>"""
            for link in links:
                links_string += """<li>
                    <a href="%s" title="%s">%s</a>
                </li>
                """ % (link.url, link.title, link.name)
            sidebar = """%s
            <h2>Reviews</h2>
            <p>"Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed
                diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam
                erat vot lutpat."<br />
                <em class="reviewer">- Person's Name</em>
            </p>""" % links_string
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
            content = """<h2>%s</h2>
            %s
            %s""" % (project.name, images_string, project.description)
            template_values = {
                'subheader_title' : "Check out some of our work.",
                'title' : project.name,
                'header': header,
                'content' : content,
                'sidebar' : sidebar
            }
            path = os.path.join(os.path.dirname(__file__), '../../template/hauk', 'secondary.html')
            self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/projects/(.*)', ViewProjectHandler)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
