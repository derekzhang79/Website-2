#/handlers/services/add_edit.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/3/11
#
#Handles requests to add or edit a service.

import sys, os, logging
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.service import Service
from models.project import Project
from models.image import Image
from errors.service import *
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class AddEditServiceHandler(webapp.RequestHandler):
    def get(self, url=None):
        if url is None:
            service = Service()
            service.title = ""
            service.url = ""
            icon = ""
            service.description = ""
            service.excerpt = ""
            featured = ""
            action = "Add"
            name = ""
        else:
            service = Service(url=url)
            try:
                service.get()
            except ServiceNotFoundException:
                self.redirect("/admin/services")
            action = "Edit"
            name = ' "%s"' % service.title
            if service.featured:
                featured = " checked=\"checked\""
            else:
                featured = ""
            if service.icon is not None:
                icon = "<img src=\"/services/%s/icon\" alt=\"%s's icon\" /><br />" % (service.url, service.title)
        image = Image()
        images = image.get_list()
        image_string = ""
        for tmp_image in images:
            icon_selected = ""
            if service.icon and tmp_image.shortname == service.icon.shortname:
                icon_selected = " selected=\"selected\""
            image_string += "<option value=\"%s\"%s>%s</option>\n" % (tmp_image.key(), icon_selected, tmp_image.shortname)
        projects = Project().get_list()
        projects_string = ""
        if projects is not None:
            projects_string += """<label>Projects</label>
            <select name="projects" multiple="multiple">"""
            project_list = []
            for project_service in service.projects:
                project_list.append(project_service.project.key())
            for project in projects:
                selected = ""
                projectkey = project.key()
                if projectkey in project_list:
                    selected = " selected=\"selected\""
                projects_string += "\n<option value=\"%s\"%s>%s</option>" % (projectkey, selected, project.name)
            projects_string += "</select><br />"
        content = """<h2>%s Service%s</h2>
            <p>
                <form method="post">
                    <label>Title</label>
                    <input type="text" name="title" value="%s" /><br />
                    <label>URL</label>
                    <input type="text" name="url" value="%s" /><br />
                    <label>Featured?</label>
                    <input type="checkbox" name="featured" value="True"%s /><br />
                    <label>Description</label>
                    <textarea name="description">%s</textarea><br />
                    <label>Excerpt</label>
                    <textarea name="excerpt">%s</textarea><br />
                    <label>Icon</label>
                    <select name="icon">
                        %s
                    </select><a href="/admin/images/add" title"Upload New
                    Icon">Add new image</a><br />
                    %s
                    %s
                    <input type="submit">
                </form>
            <p>""" % (action, name, service.title, service.url, featured, service.description, service.excerpt, image_string, icon, projects_string)
        sidebar = """<h2>Hints!</h2>
        <p>
            <b>Title</b>: The name of the service.<br />
            <b>URL</b>: The slug for the page. http://www.secondbit.org/services/android's
                slug is 'android'.<br />
            <b>Featured?</b>: Should this service be listed on the home page?<br />
            <b>Description</b>: A longer explanation, in HTML, of the service
            being offered. This is the novel-length.<br />
            <b>Excerpt</b>: A quick paragraph or two on what the service is, in
            a nutshell. This is the tweet-length.<br />
            <b>Icon</b>: The image displayed next to this service on the home
            page.<br />
            <br />
            <i>The Description and Excerpt fields should be contained within
            &lt;p&gt; tags. <b>Warning</b>: If you use the link to upload a 
            new icon, your progress on this page will not be saved.</i>
            <br />
        </p>"""
        title = "%s Service%s" % (action, name)
        template_values = {
            'content' : content,
            'title' : title,
            'sidebar' : sidebar
        }
        path = os.path.join(os.path.dirname(__file__), '../../template/hauk', 'secondary.html')
        self.response.out.write(template.render(path, template_values))

    def post(self, url=None):
        service = Service()
        if url is not None:
            service.url = url
            service.get()
        service.title = self.request.POST['title']
        service.description = self.request.POST['description']
        service.excerpt = self.request.POST['excerpt']
        service.url = self.request.POST['url']
        service.icon = db.Key(self.request.POST['icon'])
        try:
            featured = self.request.POST['featured']
        except KeyError:
            featured = "False"
        if featured == "True":
            service.featured = True
        else:
            service.featured = False
        service.save()
        projects = self.request.get_all("projects")
        project_list = []
        for project_service in service.projects:
            project_list.append(project_service.project.key())
        for project in projects:
            projectkey = db.Key(project)
            if projectkey not in project_list:
                service.add_project(db.Key(project))
            else:
                occurrences = range(0, project_list.count(projectkey))
                logging.info(occurrences)
                for instance in occurrences:
                    project_list.remove(projectkey)
        for deselected_project in project_list:
            logging.info(deselected_project)
            service.remove_project(deselected_project)
        self.redirect("/services/%s" % service.url)

application = webapp.WSGIApplication([
                                ('/admin/services/add', AddEditServiceHandler),
                                ('/admin/services/edit/(.*)', AddEditServiceHandler),
                                ('/admin/services/add/', AddEditServiceHandler)
                                ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
