#/handlers/projects/view.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/3/11
#
#Displays a page from the datastore when called

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.project import Project
from errors.project import ProjectNotFoundException
from models.link import Link
from models.review import Review
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class ViewProjectHandler(webapp.RequestHandler):
    def get(self, url):
        url = url.strip().strip("/")
        project = Project(url=url)
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
            review = Review(project=project.datastore.key())
            reviews = review.get_for_project()
            reviews_string = ""
            if len(reviews) > 0:
                reviews_string += "<h2><a href=\"/projects/%s/reviews\" style=\"color: #555;\" title=\"View All Reviews\">Reviews</a></h2>\n" % project.url
            for review in reviews:
                byline = ""
                if review.author:
                    byline = review.author
                if review.publication and review.author:
                    byline = "%s of %s" % (review.author, review.publication)
                if review.reference:
                    byline = "<a href=\"%s\" title=\"View Source\">%s</a>" % (review.reference, byline)
                reviews_string += """<p>"%s"<br />
                <em class="reviewer">- %s</em><br />
                <a href="/projects/%s/reviews/%s" title="See the full review.">See the full review</a>
                </p>""" % (review.excerpt, byline, project.url, review.url)
            sidebar = """%s
            %s""" % (links_string, reviews_string)
            services = ""
            if project.services is not None and project.services != []:
                services += "<ul>"
                for service in project.services:
                    services += "\n<li><a href=\"/services/%s\" title=\"%s\">%s</a></li>" % (service.service.url, service.service.title, service.service.title)
                services += "\n</ul>"
                sidebar += """<h2>Services</h2>
                <p>This project used the following services that we offer:</p>
                %s""" % services
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
