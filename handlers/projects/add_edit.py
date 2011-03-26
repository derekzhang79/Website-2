#/handlers/projects/add_edit.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/3/11
#
#Handles requests to add or edit a project.

import sys, os, logging
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.project import Project
from models.link import Link
from models.image import Image
from models.service import Service
from models.person import Person
from errors.project import *
from errors.image import *
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class AddEditProjectHandler(webapp.RequestHandler):
    def get(self, url=None):
        if url is None:
            project = Project()
            project.nature = ""
            project.name = ""
            project.description = ""
            project.excerpt = ""
            project.screenshot = ""
            project.icon = ""
            project.images = []
            project.url = ""
            project.featured = ""
            project.open_source = ""
            project.featured_link = ""
            action = "Add"
            name = ""
            is_product = ""
            is_project = ""
        else:
            project = Project(url=url)
            try:
                project.get()
            except ProjectNotFoundException:
                self.redirect("/admin/projects")
            action = "Edit"
            name = ' "%s"' % project.name
            if project.featured:
                project.featured = " checked=\"checked\""
            if project.open_source:
                project.open_source = " checked=\"checked\""
            is_project = " selected=\"selected\""
            is_product = " selected=\"selected\""
            if project.nature == "product":
                is_project = ""
            else:
                is_product = ""
        image = Image()
        images = image.get_list()
        screenshot_string = ""
        icon_string = ""
        images_string = ""
        for tmp_image in images:
            screenshot_selected = ""
            icon_selected = ""
            images_selected = ""
            if project.screenshot != "":
                if tmp_image.shortname == project.screenshot.shortname:
                    screenshot_selected = " selected=\"selected\""
            if project.icon != "":
                if tmp_image.shortname == project.icon.shortname:
                    icon_selected = " selected=\"selected\""
            if tmp_image.key() in project.images:
                images_selected = " selected=\"selected\""
            screenshot_string += "\n<option value=\"%s\"%s>%s</option>" % (tmp_image.shortname, screenshot_selected, tmp_image.shortname)
            icon_string += "\n<option value=\"%s\"%s>%s</option>" % (tmp_image.shortname, icon_selected, tmp_image.shortname)
            images_string += "\n<option value=\"%s\"%s>%s</option>" % (tmp_image.key(), images_selected, tmp_image.shortname)
        link = Link(group="special_projects_featured")
        links = link.get_group()
        links_string = ""
        count = 0
        for tmp_link in links:
            selected = ""
            if project.featured_link == tmp_link:
                selected = " selected=\"selected\""
            links_string += "\n<input type=\"radio\" name=\"featured_link\" value=\"%s\"%s> <a href=\"%s\" title=\"%s\">%s</a>" % (tmp_link.key(), selected, tmp_link.url, tmp_link.title, tmp_link.name)
            count += 1
            if count >= 4:
                links_string += "<br />"
                count = 0
        services = Service().get_list()
        services_string = ""
        if services is not None:
            services_string += """<label>Services</label>
            <select name="services" multiple="multiple">"""
            service_list = []
            for project_service in project.services:
                service_list.append(project_service.service.key())
            for service in services:
                selected = ""
                servicekey = service.key()
                if servicekey in service_list:
                    selected = " selected=\"selected\""
                services_string += "\n<option value=\"%s\"%s>%s</option>" % (servicekey, selected, service.title)
            services_string += "</select><br />"
        content = """<h2>%s Project%s</h2>
            <p>
                <form method="post">
                    <label>Name</label>
                    <input type="text" name="name" value="%s" /><br />
                    <label>URL</label>
                    <input type="text" name="url" value="%s" /><br />
                    <label>Nature</label>
                    <select name="nature">
                        <option value="project"%s>Project</option>
                        <option value="product"%s>Product</option>
                    </select><br />
                    <label>Description</label>
                    <textarea name="description">%s</textarea><br />
                    <label>Excerpt</label>
                    <textarea name="excerpt">%s</textarea><br />
                    <label>Screenshot</label>
                    <select name="screenshot">%s
                    </select><a href="/admin/images/add" title="Add New">Add New</a><br />
                    <label>Icon</label>
                    <select name="icon">%s
                    </select><a href="/admin/images/add" title="Add New">Add New</a><br />
                    <label>Images</label>
                    <select name="images" multiple="multiple">%s
                    </select><a href="/admin/images/add" title="Add New">Add New</a><br />
                    <label>Featured?</label>
                    <input type="checkbox" name="featured" value="True"%s /><br />
                    <label>Featured Link</label>
                    %s<br /><a href="/admin/links/add?group=special_featured_projects" title="Add New">Add New</a><br />
                    <label>Open Source</label>
                    <input type="checkbox" name="open_source" value="True"%s /><br />
                    %s
                    <input type="submit">
                </form>
            <p>""" % (action, name, project.name, project.url, is_project, is_product, project.description, project.excerpt, screenshot_string, icon_string, images_string, project.featured, links_string, project.open_source, services_string)
        sidebar = """<h2>Hints!</h2>
        <p>
            <b>Name</b>: The name of the project.<br />
            <b>URL</b>: The slug for the project.
            http://www.secondbit.org/projects/android2cloud's  slug is
            'android2cloud'.<br />
            <b>Nature</b>: Whether the project is a project (client work, open
            source things, etc.) or a product (something we 'sell').<br />
            <b>Description</b>: A description of the project. The long story.<br
            />
            <b>Excerpt</b>: A quick description of the project for the front
            page. Shouldn't be more than a tweet.<br />
            <b>Screenshot</b>: Select the image to use as a screenshot, or click
            the link to add a new image to use as a screenshot (your progress on
            this page won't be saved!)<br />
            <b>Icon</b>: Select the image to use as an icon, or click the link
            to add a new image to use as an icon (your progress on this page
            won't be saved!)<br />
            <b>Featured?</b>: Is the project part of the rotating slideshow on
            the homapge?<br />
            <b>Open Source?</b>: Is the project published under an open source
            license?
        </p>"""
        title = "%s Project%s" % (action, name)
        link = Link(group="special_menu")
        menu = link.get_group()
        person = Person()
        people = person.get_featured()
        template_values = {
            'content' : content,
            'title' : title,
            'sidebar' : sidebar,
            'people' : people,
            'menu' : menu
        }
        path = os.path.join(os.path.dirname(__file__), '../../template/hauk', 'secondary.html')
        self.response.out.write(template.render(path, template_values))

    def post(self, url=None):
        #page = Page()
        project = Project()
        if url is not None:
            project.url = url
            project.get()
        try:
            project.nature = self.request.POST['nature']
        except KeyError:
            pass
        try:
            project.name = self.request.POST['name']
        except KeyError:
            pass
        try:
            project.description = self.request.POST['description']
        except KeyError:
            pass
        try:
            project.excerpt = self.request.POST['excerpt']
        except KeyError:
            pass
        try:
            project.url = self.request.POST['url']
        except KeyError:
            pass
        try:
            featured = self.request.POST['featured']
        except KeyError:
            featured = "False"
        if featured == "True":
            project.featured = True
        else:
            project.featured = False
        try:
            open_source = self.request.POST['open_source']
        except KeyError:
            open_source = "False"
        if open_source == "True":
            project.open_source = True
        else:
            project.open_source = False
        try:
            screenshot = Image(shortname=self.request.POST['screenshot'])
        except KeyError:
            pass
        try:
            screenshot.get()
        except ImageNotFoundError:
            pass
        else:
            if screenshot.width > 314 or screenshot.height > 160:
                screenshot.rescale(width=314, height=160, crop=True)
            project.screenshot = screenshot.datastore
        try:
            icon = Image(shortname=self.request.POST['icon'])
        except KeyError:
            pass
        try:
            icon.get()
        except ImageNotFoundError:
            pass
        else:
            project.icon = icon.datastore
        images = self.request.get_all('images')
        count = 0
        for image in images:
            images[count] = db.Key(image)
            count += 1
        project.images = images
        try:
            featured_link = self.request.POST['featured_link']
        except KeyError:
            pass
        else:
            project.featured_link = db.Key(featured_link)
        project.save()
        services = self.request.get_all('services')
        service_list = []
        for project_service in project.services:
            service_list.append(project_service.service.key())
        for service in services:
            servicekey = db.Key(service)
            if servicekey not in service_list:
                project.add_service(servicekey)
            else:
                occurrences = range(0, service_list.count(servicekey))
                for instance in occurrences:
                    service_list.remove(servicekey)
        for deselected_service in service_list:
            project.remove_service(deselected_service)
        self.redirect("/projects/%s" % project.url)

application = webapp.WSGIApplication([
                                ('/admin/projects/add', AddEditProjectHandler),
                                ('/admin/projects/edit/(.*)', AddEditProjectHandler),
                                ('/admin/projects/add/', AddEditProjectHandler)
                                ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
