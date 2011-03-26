#models/person.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/20/11
#
#Defines the datastore interface for people.

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from google.appengine.ext import db
from google.appengine.api import memcache
from datastore import PersonData
from errors.person import *
from models.image import Image

class Person():
    """Defines datastore interactions for people on the site."""

    #attributes
    avatar = None
    name = None
    role = None
    featured = None
    description = None
    date_joined = None
    email = None
    homepage = None
    url = None
    datastore = None

    def __init__(self, datastore=None, avatar=None, name=None, role=None, featured=None, description=None, date_joined=None, email=None, homepage=None, url=None):
        """Defines the initialization method for a Page object. Accepts the
        datastore (an instance of a PageData object), the title of the page,
        the content of the page as HTML, the sidebar of the page as HTML, the
        URL slug of the page, and is_public (whether the page is accessible to
        non-admins) as a boolean, all of which are optional."""

        #reset all local variables
        self.avatar = None
        self.name = None
        self.role = None
        self.featured = None
        self.description = None
        self.date_joined = None
        self.email = None
        self.homepage = None
        self.url = None
        self.datastore = None

        if datastore is not None:
            self.avatar = datastore.avatar
            self.name = datastore.name
            self.role = datastore.role
            self.featured = datastore.featured
            self.description = datastore.description
            self.date_joined = datastore.date_joined
            self.email = datastore.email
            self.homepage = datastore.homepage
            self.url = datastore.url
            self.datastore = datastore
        else:
            self.datastore = PersonData()
        if url is not None:
            self.url = url.lower().strip("/").strip()
        if featured is not None:
            self.featured = featured
        if avatar is not None:
            self.avatar = avatar
        if name is not None:
            self.name = name
        if role is not None:
            self.role = role
        if description is not None:
            self.description = description
        if date_joined is not None:
            self.date_joined = date_joined
        if email is not None:
            self.email = email
        if homepage is not None:
            self.homepage = homepage

    def save(self):
        """Writes the current instance of Page to the datastore as a PageData
        object. If Page.datastore is not set, throws a
        PageNotInstantiatedException. If Page.url is set and is different from
        Page.datastore.url, Page.url will be checked against the datastore for
        uniqueness. If Page.url is not unique, a PageURLTakenException will be
        thrown. If Page.url matches a list of reserved URLs, a
        PageURLReservedException will be thrown."""

        if self.datastore is None:
            raise PersonNotInstantiatedException
        else:
            if self.url and self.url != self.datastore.url:
                try:
                    duplicate = Person(url=self.url)
                    duplicate.get()
                except PersonNotFoundException:
                    pass
                else:
                    raise PersonURLTakenException, self.url
            elif not self.url:
                raise PersonNotInstantiatedException
            avatar = Image(datastore=db.get(db.Key(self.avatar)))
            if avatar.width != 150:
                self.datastore.avatar = avatar.rescale(width=150, crop=False)
            if self.datastore.avatar_thumb is None or self.datastore.avatar_thumb.original is None or avatar.datastore.key() != self.datastore.avatar_thumb.original.key():
                self.datastore.avatar_thumb = Image(datastore=self.datastore.avatar).rescale(width=34, height=34, crop=True)
            self.datastore.featured = self.featured
            self.datastore.role = self.role
            self.datastore.url = self.url
            self.datastore.name = self.name
            self.datastore.description = self.description
            self.datastore.date_joined = self.date_joined
            self.datastore.email = self.email
            self.datastore.homepage = self.homepage
            self.datastore.put()
            memcache.set("models/person/%s" % self.datastore.url, self.datastore)
            memcache.delete("models/people/list")
            memcache.delete("models/people/featured")

    def get(self):
        """Populates the current instance of Page with the data from
        PageData.get(url=self.url). Throws a PageNotFoundException if it can't
        find self.url in the datastore. Throws a PageNotInstantiatedException if
        self.url is None."""

        if self.url is None:
            raise PersonNotInstantiatedException
        else:
            datastore = memcache.get("models/person/%s" % self.url)
            if datastore is None:
                datastore = PersonData.all().filter("url =", self.url).get()
                if datastore is not None:
                    memcache.set("models/person/%s" % self.url, datastore)
            if datastore is None:
                raise PersonNotFoundException, self.url
            else:
                self.datastore = datastore
                self.avatar = datastore.avatar
                self.avatar_thumb = datastore.avatar_thumb
                self.featured = datastore.featured
                self.url = datastore.url
                self.role = datastore.role
                self.description = datastore.description
                self.name = datastore.name
                self.email = datastore.email
                self.date_joined = datastore.date_joined
                self.homepage = datastore.homepage

    def get_list(self):
        """Returns a Query object for up to 1,000 PersonData objects."""
        people = memcache.get("models/people/list")
        if people is None:
            people = PersonData.all().order("date_joined").fetch(1000)
            memcache.set("models/people/list", people)
        return people

    def get_featured(self):
        """Returns a Query object for up to 1,000 ReviewData objects that share
        a ProjectData value with self.project."""
        people = memcache.get("models/people/featured")
        if people is None:
            people = PersonData.all().filter("featured =", True).order("date_joined").fetch(1000)
            memcache.set("models/people/featured", people)
        return people

    def delete(self):
        """Removes self.datastore from the datastore. Throws a
        PageNotInstantiatedException if self.datastore is None."""

        if self.datastore is None:
            raise ReviewNotInstantiatedException
        else:
            memcache.delete("models/person/%s" % self.datastore.url)
            memcache.delete("models/people/list")
            memcache.delete("models/people/featured")
            self.datastore.delete()
            self.datastore = None
            self.avatar = None
            self.avatar_thumb = None
            self.email = None
            self.url = None
            self.role = None
            self.homepage = None
            self.description = None
            self.name = None
            self.date_joined = None
            self.featured = None
