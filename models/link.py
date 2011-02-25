#models/link.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/25/11
#
#Defines the datastore interface for links.

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from datastore import LinkData

class Link():
    """Defines datastore interactions for links that appear throughout the
    site."""

    #attributes
    name = None
    title = None
    url = None
    weight = None
    modified_by = None
    modified_on = None
    group = None
    datastore = None

    def __init__(self, name=None, datastore=None, title=None, url=None, weight=None, group=None, key=None):
        """Defines the initialization method for a Link object. Accepts the
        datastore (an instance of a LinkData object) the name (the text that is
        linked), the title (the title element of the link), the url, the weight
        (determines order), the group (determines where the link is displayed)
        of the link, and the datastore key for the link, all optional."""

        #reset all local variables
        self.name = None
        self.title = None
        self.url = None
        self.weight = None
        self.modified_by = None
        self.modified_on = None
        self.group = None
        self.datastore = None
        self.key = None

        if datastore is not None:
            self.datastore = datastore
            self.name = datastore.name
            self.title = datastore.title
            self.url = datastore.url
            self.weight = datastore.weight
            self.modified_by = datastore.modified_by
            self.modified_on = datastore.modified_on
            self.group = datastore.group
            self.key = datastore.key()
        else:
            self.datastore = LinkData()
        if name is not None:
            self.name = name
        if title is not None:
            self.title = title
        if url is not None:
            self.url = url
        if weight is not None:
            self.weight = weight
        if group is not None:
            self.group = group
        if key is not None:
            self.key = key

    def save(self):
        """Writes the current instance of Link to the datastore as a LinkData
        object. If Link.datastore is not set, throws a
        LinkNotInstantiatedException."""

        if self.datastore is None:
            raise LinkNotInstantiatedException
        else:
            self.datastore.name = self.name
            self.datastore.title = self.title
            self.datastore.url = self.url
            self.datastore.weight = int(self.weight)
            self.datastore.group = self.group
            self.datastore.put()

    def get(self):
        """Populates the current instance of Link with the data from
        ImageData.get(self.key). Throws a LinkNotFoundException if it can't find
        self.key in the datastore. Throws a LinkNotInstantiatedException if
        self.key is None."""

        if self.key is None:
            raise LinkNotInstantiatedException
        else:
            datastore = LinkData.get(self.key)
            if datastore is None:
                raise LinkNotFoundException, self.key
            else:
                self.datastore = datastore
                self.name = datastore.name
                self.title = datastore.title
                self.url = datastore.url
                self.weight = datastore.weight
                self.modified_by = datastore.modified_by
                self.modified_on = datastore.modified_on
                self.group = datastore.group

    def delete(self):
        """Removes the current instance of Link from the datastore. Throws a
        LinkNotInstantiatedException if self.datastore is None."""

        if self.datastore is None:
            raise LinkNotInstantiatedException
        else:
            self.datastore.delete()
            self.datastore = None
            self.name = None
            self.title = None
            self.url = None
            self.weight = None
            self.modified_by = None
            self.modified_on = None
            self.group = None

    def get_group(self):
        """Returns a Query object of LinkData instances for all the links that
        match self.group, ordered by weight ascending. Throws a
        LinkNotInstantiatedException is self.group is None."""

        if self.group is None:
            raise LinkNotInstantiatedException
        else:
            return LinkData.all().filter("group =", self.group).order("weight").fetch(1000)

    def get_list(self):
        """Returns a Query object for up to 1,000 LinkData objects."""

        return LinkData.all().fetch(1000)
