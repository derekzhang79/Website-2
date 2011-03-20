#/handlers/people/add_edit.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/20/11
#
#Handles requests to add or edit a person.

import sys, os, logging
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from datetime import datetime

from models.person import Person
from models.image import Image
from errors.person import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class AddEditPersonHandler(webapp.RequestHandler):
    def get(self, url=None):
        if url is None:
            person = Person()
            person.avatar = ""
            person.name = ""
            person.role = ""
            person.featured = False
            person.description = ""
            person.date_joined = ""
            person.email = ""
            person.homepage = ""
            person.url = ""
            action = "Add"
            name = 'Person'
            avatar = ""
        else:
            person = Person(url=url)
            person.get()
            action = "Edit"
            name = person.name
            avatar = "<img src=\"/image/%s\" alt=\"Avatar\" />" % person.avatar.shortname
            person.date_joined = person.date_joined.strftime("%m/%d/%Y %H:%M")
        image = Image()
        images = image.get_list()
        images_string = "<select name=\"avatar\">"
        for image in images:
            selected = ""
            if person.avatar != "" and image.key() == person.avatar.key():
                selected = " selected=\"selected\""
            images_string += "\n<option value=\"%s\"%s>%s</option>" % (image.key(), selected, image.shortname)
        images_string += "</select>"
        if person.featured:
            featured = "checked=\"checked\""
        else:
            featured = ""
        content = """<h2>%s %s</h2>
        <p>
            <form method="post">
                <label>Avatar</label>
                %s<br />
                %s<br />
                <label>Name</label>
                <input type="text" name="name" value="%s" /><br />
                <label>Role</label>
                <input type="text" name="role" value="%s" /><br />
                <label>Featured?</label>
                <input type="checkbox" name="featured" value="True"%s /><br />
                <label>URL</label>
                <input type="text" name="url" value="%s" /><br />
                <label>Description</label>
                <textarea name="description">%s</textarea><br />
                <label>Date Joined</label>
                <input type="text" value="%s" name="date_joined" /><br />
                <label>Email</label>
                <input type="text" value="%s" name="email" /><br />
                <label>Homepage</label>
                <input type="text" value="%s" name="homepage" /><br />
                <input type="submit">
            </form>
        </p>""" % (action, name, images_string, avatar, person.name, person.role, featured, person.url, person.description, person.date_joined, person.email, person.homepage)
        sidebar = """<h2>Hint!</h2>
            <p>
                <b>Name:</b> The text that is linked, like <a href="#">this</a>.<br />
                <b>Title:</b> The text that appears when the link is hovered
                    over. Like <a href="#" title="This is a title.">this</a>.<br
                    />
                <b>URL:</b> The URL you're linking to.<br />
                <b>Weight:</b> The 'weight' of the link, which determines how
                    the links in the group are ordered. The heavier the link,
                    the lower it is ordered.<br />
                <b>Group:</b> The 'group' the link is part of. Could be
                    'special_menu' or 'project_android2cloud'.
            </p>"""
        template_values = {
            'content' : content,
            'title' : '%s %s' % (action, name),
            'sidebar': sidebar
        }
        path = os.path.join(os.path.dirname(__file__), "../../template/hauk", 'secondary.html')
        self.response.out.write(template.render(path, template_values))
            
    def post(self, url=None):
        person = Person()
        if url is not None:
            person.url = url
            person.get()
        person.avatar = self.request.get('avatar')
        person.featured = self.request.get('featured') == "True"
        person.url = self.request.get('url')
        person.date_joined = datetime.strptime(self.request.get('date_joined'), "%m/%d/%Y %H:%M")
        person.name = self.request.get('name')
        person.role = self.request.get('role')
        person.description = self.request.get('description')
        person.email = self.request.get('email')
        person.homepage = self.request.get('homepage')
        person.save()
        self.redirect("/team/%s" % person.url)

application = webapp.WSGIApplication([
                                ('/admin/people/add', AddEditPersonHandler),
                                ('/admin/people/edit/(.*)', AddEditPersonHandler),
                                ('/admin/people/add/', AddEditPersonHandler)
                                ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
