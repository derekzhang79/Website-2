import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.api import memcache
from models import *

class EditMenuItemHandler(webapp.RequestHandler):
  def get(self, menu_id=None):
    if menu_id == None:
      self.redirect('/admin/menu/reorder')
    menu_item = MenuData.all().filter('id =', menu_id).get()
    if menu_item == None:
      self.redirect('/admin')
    content = """
    <h2></h2>
    <p>
      <form method="post">
      <label>Name:</label>
      <input type="text" name="name" value="%s" /><br />
      <label>Title:</label>
      <input type="text" name="title" value="%s" /><br />
      <label>URL:</label>
      <input type="text" name="url" value="%s" /><br />
      <input type="submit" />
    </p>""" % (menu_item.name, menu_item.title, menu_item.url)
    template_values = {
      'title' : 'Add Menu Link',
      'content' : content
    }
    path = os.path.join(os.path.dirname(__file__), '../../', 'template', 'secondary.html')
    self.response.out.write(template.render(path, template_values))
  
  def post(self, menu_id=None):
    menu_data = MenuData.all().filter('id =', menu_id).get()
    menu_data.title = self.request.get('title')
    menu_data.name = self.request.get('name')
    menu_data.url = self.request.get('url')
    menu_data.weight = 0;
    menu_data.put()
    self.redirect('/admin')

class ReorderMenuHandler(webapp.RequestHandler):
  def get(self):
    menu_items = MenuData.all().order("weight DESC").fetch(1000)
    menu_links = ""
    for menu_item in menu_items:
      menu_links += "\n<div style=\"reorder_menu_item\" id=\"%s\"><a href=\"%s\" title=\"%s\" target=\"_blank\">%s</a></div>" % (menu_item.id, menu_item.url, menu_item.title, menu_item.name)
    content = """
    <h2></h2>
    <p>
    %s
      <form method="post">
        <input type="text" name="menu_items" style="display:none;" /><br />
        <input type="submit" />
      </form>
    </p>""" % menu
    template_values = {
      'title' : "Reorder Menu",
      'content' : content
    }
    path = os.path.join(os.path.dirname(__file__), '../../', 'template', 'secondary.html')
    self.response.out.write(template.render(path, template_values))
    
  def post(self):
    menu_order = self.request.get('menu_items').split(",")
    weight = len(menu_order) + 1
    for item in menu_order:
      menu_item = MenuData.all().filter("id =", item).get()
      menu_item.weight = weight;
      weight --;
      menu_item.put()
    self.redirect('/')

def main():
  application = webapp.WSGIApplication([('/admin/menu/edit', EditMenuItemHandler),
                                        ('/admin/menu/edit/(.*)', EditMenuItemHandler),
                                        ('/admin/menu/reorder', ReorderMenuHandler)],
                                        debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()