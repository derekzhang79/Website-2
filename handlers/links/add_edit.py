#/handlers/link/add_edit.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/25/11
#
#Handles requests to add or edit a link.

import sys, os, logging
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.link import Link
from models.person import Person
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class AddEditLinkHandler(webapp.RequestHandler):
    def get(self, key=None):
        if key is None:
            link = Link()
            link.name = ""
            link.title = ""
            link.url = ""
            link.weight = ""
            link.group = ""
            action = "Add"
            name = ''
        else:
            link = Link(key=key)
            link.get()
            action = "Edit"
            name = " '%s'" % link.name
        content = """
            <form method="post">
                <label>Name</label>
                <input type="text" name="name" value="%s" /><br />
                <label>Title</label>
                <input type="text" name="title" value="%s" /><br />
                <label>URL</label>
                <input type="text" name="url" value="%s" /><br />
                <label>Weight</label>
                <input type="text" name="weight" value="%s" /><br />
                <label>Group</label>
                <input type="text" name="group" value="%s" /><br />
                <input type="submit">
            </form>""" % (link.name, link.title, link.url, link.weight, link.group)
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
        person = Person()
        people = person.get_featured()
        link = Link(group="special_menu")
        menu = link.get_group()
        template_values = {
            'content' : '<h2>%s Link%s</h2><div>%s</div>' % (action, name, content),
            'title' : '%s Link%s' % (action, name),
            'sidebar': sidebar,
            'people' : people,
            'menu' : menu
        }
        path = os.path.join(os.path.dirname(__file__), "../../template/hauk", 'secondary.html')
        self.response.out.write(template.render(path, template_values))
            
    def post(self, key=None):
        link = Link()
        if key is not None:
            link.key = key
            link.get()
        link.name = self.request.POST['name']
        link.title = self.request.POST['title']
        link.url = self.request.POST['url']
        link.weight = self.request.POST['weight']
        link.group = self.request.POST['group']
        link.save()
        self.redirect("/admin/links")

application = webapp.WSGIApplication([
                                ('/admin/links/add', AddEditLinkHandler),
                                ('/admin/links/edit/(.*)', AddEditLinkHandler),
                                ('/admin/links/add/', AddEditLinkHandler)
                                ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
