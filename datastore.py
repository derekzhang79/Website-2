#datastore.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/25/11
#
#Defines the datastore tables and their respective fields.

from google.appengine.ext import db

class ImageData(db.Model):
    image = db.BlobProperty()
    original = db.SelfReferenceProperty(collection_name='sizes', required=False)
    mimetype = db.StringProperty(required=False, multiline=False)
    shortname = db.StringProperty(multiline=False)
    uploaded_by = db.UserProperty(auto_current_user=True)
    uploaded_on = db.DateTimeProperty(auto_now=True)
    height = db.IntegerProperty()
    width = db.IntegerProperty()

class PageData(db.Model):
    title = db.StringProperty(multiline=False)
    content = db.TextProperty()
    sidebar = db.TextProperty()
    url = db.StringProperty(multiline=False)
    is_public = db.BooleanProperty()
    modified_by = db.UserProperty(auto_current_user=True)
    modified_on = db.DateTimeProperty(auto_now=True)

class ProjectData(db.Model):
    nature = db.StringProperty(multiline=False, choices=['product', 'project'])
    name = db.StringProperty(multiline=False)
    description = db.TextProperty()
    excerpt = db.StringProperty(multiline=True)
    screenshot = db.ReferenceProperty(ImageData, collection_name='screenshots')
    icon = db.ReferenceProperty(ImageData, collection_name='icons')
    images = db.ListProperty(db.Key)
    url = db.StringProperty(multiline=False)
    featured = db.BooleanProperty()
    open_source = db.BooleanProperty()
    featured_link = db.ReferenceProperty()
    modified_by = db.UserProperty(auto_current_user=True)
    modified_on = db.DateTimeProperty(auto_now=True)

class LinkData(db.Model):
    name = db.StringProperty(multiline=False)
    title = db.StringProperty(multiline=False, required=False)
    url = db.StringProperty(multiline=False, required=False)
    weight = db.IntegerProperty()
    modified_by = db.UserProperty(auto_current_user=True)
    modified_on = db.DateTimeProperty(auto_now=True)
    group = db.StringProperty(multiline=False)

class ServiceData(db.Model):
    url = db.StringProperty(multiline=False)
    title = db.StringProperty(multiline=False)
    icon = db.ReferenceProperty(ImageData)
    description = db.TextProperty()
    excerpt = db.StringProperty(multiline=True)
    featured = db.BooleanProperty()
    modified_on = db.DateTimeProperty(auto_now=True)
    modified_by = db.UserProperty(auto_current_user=True)

class ProjectServiceData(db.Model):
    project = db.ReferenceProperty(ProjectData, collection_name='services')
    service = db.ReferenceProperty(ServiceData, collection_name='projects')
    content = db.StringProperty(multiline=True)

class UploadData(db.Model):
    upload = db.Blob()
    mimetype = db.StringProperty(required=False, multiline=False)
    shortname = db.StringProperty(multiline=False)
    uploaded_by = db.UserProperty(auto_current_user=True)
    uploaded_on = db.DateTimeProperty(auto_now=True)

class ReviewData(db.Model):
    author = db.StringProperty(multiline=False, required=False)
    publication = db.StringProperty(multiline=False, required=False)
    reference = db.StringProperty(multiline=False, required=False)
    url = db.StringProperty(multiline=False, required=False)
    content = db.TextProperty()
    excerpt = db.StringProperty(multiline=True)
    project = db.ReferenceProperty(ProjectData, collection_name='reviews', required=False)
    date = db.DateTimeProperty()
    featured = db.BooleanProperty()
    modified_by = db.UserProperty(auto_current_user=True)
    modified_on = db.DateTimeProperty(auto_now=True)

class PersonData(db.Model):
    avatar = db.ReferenceProperty(ImageData)
    avatar_thumb = db.ReferenceProperty(ImageData, collection_name="peoplethumbs")
    name = db.StringProperty(multiline=False)
    role = db.StringProperty(multiline=False)
    featured = db.BooleanProperty()
    description = db.TextProperty()
    date_joined = db.DateTimeProperty()
    email = db.StringProperty(multiline=False, required=False)
    homepage = db.StringProperty(multiline=False, required=False)
    url = db.StringProperty(multiline=False)

class SiteData(db.Model):
    about_us_footer = db.StringProperty(multiline=True)
    template = db.StringProperty(multiline=False)
    analytics_string = db.StringProperty(multiline=False)
    logo = db.ReferenceProperty(ImageData)
    name = db.StringProperty(multiline=False)
