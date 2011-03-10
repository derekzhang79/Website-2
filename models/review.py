#models/review.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/10/11
#
#Defines the datastore interface for reviews.

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from datastore import ReviewData
#from errors.page import *

class Review():
    """Defines datastore interactions for reviews on the site."""

    #attributes
    author = None
    publication = None
    reference = None
    url = None
    excerpt = None
    project = None
    date = None
    featured = None
    modified_by = None
    modified_on = None
    datastore = None

    def __init__(self, datastore=None, author=None, publication=None, reference=None, url=None, excerpt=None, project=None, date=None, featured=None):
        """Defines the initialization method for a Page object. Accepts the
        datastore (an instance of a PageData object), the title of the page,
        the content of the page as HTML, the sidebar of the page as HTML, the
        URL slug of the page, and is_public (whether the page is accessible to
        non-admins) as a boolean, all of which are optional."""

        #reset all local variables
    	self.author = None
    	self.publication = None
    	self.reference = None
    	self.url = None
    	self.excerpt = None
    	self.project = None
    	self.date = None
    	self.featured = None
    	self.modified_by = None
    	self.modified_on = None
    	self.datastore = None


        if datastore is not None:
     	    self.author = datastore.author
    	    self.publication = datastore.publication
    	    self.reference = datastore.reference
    	    self.url = datastore.url
    	    self.excerpt = datastore.excerpt
    	    self.project = datastore.project
    	    self.date = datastore.date
            self.featured = datastore.featured
            self.modified_by = datastore.modified_by
            self.modified_on = datastore.modified_on
            self.datastore = datastore
        else:
            self.datastore = ReviewData()
        if author is not None:
            self.author = author
        if publication is not None:
            self.publication = publication
        if reference is not None:
            self.reference = reference
        if url is not None:
            self.url = url.lower().strip("/").strip()
        if excerpt is not None:
            self.excerpt = excerpt
        if project is not None:
            self.project = project
        if date is not None:
            self.date = date
        if featured is not None:
            self.featured = featured

    def save(self):
        """Writes the current instance of Page to the datastore as a PageData
        object. If Page.datastore is not set, throws a
        PageNotInstantiatedException. If Page.url is set and is different from
        Page.datastore.url, Page.url will be checked against the datastore for
        uniqueness. If Page.url is not unique, a PageURLTakenException will be
        thrown. If Page.url matches a list of reserved URLs, a
        PageURLReservedException will be thrown."""

        if self.datastore is None:
            raise ReviewNotInstantiatedException
        else:
            if self.url and self.url != self.datastore.url:
                try:
                    duplicate = Page(url=self.url)
                    duplicate.get()
                except PageNotFoundException:
                    pass
                else:
                    raise PageURLTakenException, self.url
            else:
                raise PageNotInstantiatedException
            self.datastore.author = self.author
            self.datastore.publication = self.publication
            self.datastore.reference = self.reference
            self.datastore.url = self.url
            self.datastore.excerpt = self.excerpt
            self.datastore.project = self.project
            self.datastore.date = self.date
            self.datastore.featured = self.featured
            self.datastore.put()

    def get(self):
        """Populates the current instance of Page with the data from
        PageData.get(url=self.url). Throws a PageNotFoundException if it can't
        find self.url in the datastore. Throws a PageNotInstantiatedException if
        self.url is None."""

        if self.url is None:
            raise ReviewNotInstantiatedException
        else:
            datastore = ReviewData.all().filter("url =", self.url).get()
            if datastore is None:
                raise ReviewNotFoundException, self.url
            else:
                self.datastore = datastore
                self.author = datastore.author
                self.publication = datastore.publication
                self.url = datastore.url
                self.reference = datastore.reference
                self.excerpt = datastore.excerpt
                self.project = datastore.project
                self.date = datastore.date
                self.featured = datastore.featured
                self.modified_on = datastore.modified_on
                self.modified_by = datastore.modified_by

    def get_list(self):
        """Returns a Query object for up to 1,000 PageData objects."""

        return ReviewData.all().order("-modified_on").fetch(1000)

    def get_for_project(self):
        """Returns a Query object for up to 1,000 ReviewData objects that share
        a ProjectData value with self.project."""
        
        if self.project is None:
            raise ReviewNotInstantiatedException
        return ReviewData.all().filter("project =", self.project).order("-date").fetch(1000)

    def delete(self):
        """Removes self.datastore from the datastore. Throws a
        PageNotInstantiatedException if self.datastore is None."""

        if self.datastore is None:
            raise ReviewNotInstantiatedException
        else:
            self.datastore.delete()
            self.datastore = None
            self.author = None
            self.publication = None
            self.url = None
            self.reference = None
            self.excerpt = None
            self.project = None
            self.date = None
            self.featured = None
            self.modified_on = None
            self.modified_by = None
