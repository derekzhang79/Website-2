#models/page.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/25/11
#
#Defines the datastore interface for pages.

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from datastore import PageData
from errors.page import *

from google.appengine.api import memcache

reserved_urls = ['projects', 'project', 'products', 'product', 'team', 'image', 'images', 'style', 'js', 'portfolio', 'admin', 'reviews', 'review', 'services', 'service', 'file']

class Page():
    """Defines datastore interactions for basic pages on the site."""

    #attributes
    title = None
    content = None
    sidebar = None
    url = None
    is_public = None
    modified_by = None
    modified_on = None
    datastore = None

    def __init__(self, datastore=None, title=None, content=None, sidebar=None, url=None, is_public=None):
        """Defines the initialization method for a Page object. Accepts the
        datastore (an instance of a PageData object), the title of the page,
        the content of the page as HTML, the sidebar of the page as HTML, the
        URL slug of the page, and is_public (whether the page is accessible to
        non-admins) as a boolean, all of which are optional."""

        #reset all local variables
        self.title = None
        self.content = None
        self.sidebar = None
        self.url = None
        self.is_public = None
        self.modified_by = None
        self.modified_on = None
        self.datastore = None

        if datastore is not None:
            self.datastore = datastore
            self.title = datastore.title
            self.content = datastore.content
            self.sidebar = datastore.sidebar
            self.url = datastore.url
            self.is_public = datastore.is_public
            self.modified_on = datastore.modified_on
            self.modified_by = datastore.modified_by
        else:
            self.datastore = PageData()
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        if sidebar is not None:
            self.sidebar = sidebar
        if url is not None:
            self.url = url.lower()
        if is_public is not None:
            self.is_public = is_public
        if self.title is not None:
            self.title = self.title

    def save(self):
        """Writes the current instance of Page to the datastore as a PageData
        object. If Page.datastore is not set, throws a
        PageNotInstantiatedException. If Page.url is set and is different from
        Page.datastore.url, Page.url will be checked against the datastore for
        uniqueness. If Page.url is not unique, a PageURLTakenException will be
        thrown. If Page.url matches a list of reserved URLs, a
        PageURLReservedException will be thrown."""

        if self.datastore is None:
            raise PageNotInstantiatedException
        else:
            if self.url and self.url != self.datastore.url:
                if self.url in reserved_urls:
                    raise PageURLReservedException, self.url
                else:
                    try:
                        duplicate = Page(url=self.url)
                        duplicate.get()
                    except PageNotFoundException:
                        pass
                    else:
                        raise PageURLTakenException, self.url
            self.datastore.title = self.title
            self.datastore.content = self.content
            self.datastore.url = self.url
            self.datastore.sidebar = self.sidebar
            self.datastore.is_public = self.is_public
            self.datastore.put()
            memcache.set("models/page/%s" % self.datastore.url, self.datastore)
            memcache.delete("models/pages/list")

    def get(self):
        """Populates the current instance of Page with the data from
        PageData.get(url=self.url). Throws a PageNotFoundException if it can't
        find self.url in the datastore. Throws a PageNotInstantiatedException if
        self.url is None."""

        if self.url is None:
            raise PageNotInstantiatedException
        else:
            datastore = memcache.get("models/page/%s" % self.url)
            if datastore is None:
                datastore = PageData.all().filter("url =", self.url).get()
                if datastore is not None:
                    memcache.set("models/page/%s" % self.url, datastore)
            if datastore is None:
                raise PageNotFoundException, self.url
            else:
                self.datastore = datastore
                self.title = datastore.title
                self.content = datastore.content
                self.url = datastore.url
                self.sidebar = datastore.sidebar
                self.is_public = datastore.is_public
                self.modified_on = datastore.modified_on
                self.modified_by = datastore.modified_by

    def get_list(self):
        """Returns a Query object for up to 1,000 PageData objects."""
        pages = memcache.get("models/pages/list")
        if pages is None:
            pages = PageData.all().order("-modified_on").fetch(1000)
            memcache.set("models/pages/list", pages)
        return pages

    def delete(self):
        """Removes self.datastore from the datastore. Throws a
        PageNotInstantiatedException if self.datastore is None."""

        if self.datastore is None:
            raise PageNotInstantiatedException
        else:
            memcache.delete("models/page/%s" % self.datastore.url)
            memcache.delete("models/pages/list")
            self.datastore.delete()
            self.datastore = None
            self.title = None
            self.content = None
            self.url = None
            self.sidebar = None
            self.is_public = None
            self.modified_on = None
            self.modified_by = None
