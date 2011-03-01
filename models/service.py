#models/service.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/27/11
#
#Defines the datastore interface for services.

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from datastore import ServiceData
from errors.service import *

class Service():
    """Defines datastore interactions for services on the site."""

    #attributes
    title = None
    url = None
    icon = None
    description = None
    excerpt = None
    featured = None
    modified_on = None
    modified_by = None
    datastore = None

    def __init__(self, datastore=None, title=None, icon=None, featured=None, excerpt=None, description=None, url=None):
        """Defines the initialization method for a Service object. Accepts the
        datastore (an instance of a ServiceData object), the title of the
        service, the icon of the service as an ImageData reference, a
        description of the service, an excerpt of the description for displaying
        on the front page, the URL slug of the service, and whether the service
        is featured on the front page as a boolean, all of which are
        optional."""

        #reset all local variables
        self.title = None
        self.url = None
        self.icon = None
        self.description = None
        self.excerpt = None
        self.featured = None
        self.modified_by = None
        self.modified_on = None
        self.datastore = None

        if datastore is not None:
            self.datastore = datastore
            self.title = datastore.title
            self.url = datastore.url
            self.icon = datastore.icon
            self.description = datastore.description
            self.excerpt = datastore.excerpt
            self.featured = datastore.featured
            self.modified_by = datastore.modified_by
            self.modified_on = datastore.modified_on
        else:
            self.datastore = ServiceData()
        if title is not None:
            self.title = title
        if icon is not None:
            self.icon = icon
        if description is not None:
            self.description = description
        if url is not None:
            self.url = url.lower()
        if featured is not None:
            self.featured = featured
        if excerpt is not None:
            self.excerpt = excerpt

    def save(self):
        """Writes the current instance of Service to the datastore as
        ServiceData. Throws a ServiceNotInstantiatedException if self.datastore
        is None. Thorws a ServiceURLTakenException if self.url is not equal to
        self.datastore.url and self.url already exists in the datastore."""

        if self.datastore is None:
            raise ServiceNotInstantiatedException
        else:
            if self.url and self.url != self.datastore.url:
                try:
                    duplicate = Service(url=self.url)
                    duplicate.get()
                except ServiceNotFoundException:
                    pass
                else:
                    raise ServiceURLTakenException, self.url
            self.datastore.title = self.title
            self.datastore.url = self.url
            self.datastore.icon = self.icon
            self.datastore.description = self.description
            self.datastore.excerpt = self.excerpt
            self.datastore.featured = self.featured
            self.datastore.put()

    def get(self):
        """Populates the current instance of Service with data from the
        datastore. Throws a ServiceNotInstantiatedException if self.url is None.
        Throws a ServiceNotFoundException if self.url doesn't exist in the
        datastore."""

        if self.url is None:
            raise ServiceNotInstantiatedException
        else:
            datastore = ServiceData.all().filter("url =", self.url).get()
            if datastore is None:
                raise ServiceNotFoundException, self.url
            else:
                self.datastore = datastore
                self.title = datastore.title
                self.url = datastore.url
                self.icon = datastore.icon
                self.description = datastore.description
                self.excerpt = datastore.excerpt
                self.featured = datastore.featured
                self.modified_by = datastore.modified_by
                self.modified_on = datastore.modified_on


    def get_list(self):
        """Returns a Query object for up to 1,000 ServiceData objects."""

        return ServiceData.all().order("-modified_on").fetch(1000)

    def delete(self):
        """Removes self.datastore from the datastore. Throws a
        ServiceNotInstantiatedException if self.datastore is None."""

        if self.datastore is None:
            raise ServiceeNotInstantiatedException
        else:
            self.datastore.delete()
            self.title = None
            self.url = None
            self.icon = None
            self.description = None
            self.excerpt = None
            self.featured = None
            self.modified_by = None
            self.modified_on = None
            self.datastore = None
