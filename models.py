#!/usr/bin/env python

from google.appengine.ext import db

class PageData(db.Model):
  title = db.StringProperty(multiline=False)
  content = db.TextProperty()
  sidebar = db.TextProperty()
  url = db.StringProperty(multiline=False)
  modified_by = db.UserProperty(auto_current_user=True)
  modified_on = db.DateTimeProperty(auto_now=True)

class ProjectData(db.Model):
  nature = db.StringProperty(multiline=False, choices=['product', 'project'])
  name = db.StringProperty(multiline=False)
  description = db.TextProperty()
  short_description = db.StringProperty(multiline=True)
  screenshot = db.Blob()
  icon = db.Blob()
  url = db.StringProperty(multiline=False)
  modified_by = db.UserProperty(auto_current_user=True)
  modified_on = db.DateTimeProperty(auto_now=True)

class ImageData(db.Model):
  image = db.Blob()
  shortname = db.StringProperty(multiline=False)
  project = db.ReferenceProperty(ProjectData, collection_name='images')
  uploaded_by = db.UserProperty(auto_current_user=True)

class UploadData(db.Model):
  upload = db.Blob()
  shortname = db.StringProperty(multiline=False)
  uploaded_by = db.UserProperty(auto_current_user=True)
  uploaded_on = db.DateTimeProperty(auto_now=True)

class ReviewData(db.Model):
  author = db.StringProperty(multiline=False, required=False)
  publication = db.StringProperty(multiline=False, required=False)
  location = db.StringProperty(multiline=False, required=False)
  excerpt = db.StringProperty(multiline=True)
  project = db.ReferenceProperty(ProjectData, collection_name='reviews', required=False)
  modified_by = db.UserProperty(auto_current_user=True)
  modified_on = db.DateTimeProperty(auto_now=True)

class MenuData(db.Model):
  name = db.StringProperty(multiline=False)
  title = db.StringProperty(multiline=False, required=False)
  url = db.StringProperty(multiline=False, required=False)
  weight = db.IntegerProperty()
  modified_by = db.UserProperty(auto_current_user=True)
  modified_on = db.DateTimeProperty(auto_now=True)