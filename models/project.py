#models/project.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/26/11
#
#Defines the datastore interface for project.

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from datastore import ProjectData
from errors.project import *

class Project():
    """Defines datastore interactions for projects on the site."""

    #attributes
    nature = None
    name = None
    description = None
    excerpt = None
    screenshot = None
    icon = None
    images = None
    url = None
    featured = None
    open_source = None
    featured_link = None
    modified_by = None
    modified_on = None
    datastore = None

    def __init__(self, datastore=None, nature=None, name=None, description=None, excerpt=None, screenshot=None, icon=None, images=None, url=None, featured=None, open_source=None, featured_link=None):
        """Defines the initialization method for a Project object. Accepts a
        datastore reference, a nature (project or product), a name, a
        description, an excerpt, a screenshot (reference to an ImageData
        object), an icon (reference to an ImageData object), images (a list of
        ImageData objects), a url slug, whether it's featured or not, whether
        it's open source or not, and a featured link (reference to a LinkData
        object). All arguments are optional."""

        #reset all local variables
        self.nature = None
        self.name = None
        self.description = None
        self.excerpt = None
        self.screenshot = None
        self.icon = None
        self.images = None
        self.url = None
        self.featured = None
        self.open_source = None
        self.featured_link = None
        self.modified_on = None
        self.modified_by = None
        self.datastore = None

        if datastore is not None:
            self.datastore = datastore
            self.nature = datastore.nature
            self.name = datastore.name
            self.description = datastore.description
            self.excerpt = datastore.excerpt
            self.screenshot = datastore.screenshot
            self.icon = datastore.icon
            self.images = datastore.images
            self.url = datastore.url
            self.featured = datastore.featured
            self.open_source = datastore.open_source
            self.featured_link = datastore.featured_link
            self.modified_on = datastore.modified_on
            self.modified_by = datastore.modified_by
        else:
            self.datastore = ProjectData()
        if nature is not None:
            self.nature = nature
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if excerpt is not None:
            self.excerpt = excerpt
        if screenshot is not None:
            self.screenshot = screenshot
        if icon is not None:
            self.icon = icon
        if images is not None:
            self.images = images
        if url is not None:
            self.url = url
        if featured is not None:
            self.featured = featured
        if open_source is not None:
            self.open_source = open_source
        if featured_link is not None:
            self.featured_link = featured_link

    def save(self):
        """Writes the current instance of Project to the datastore. If
        self.datastore is None, throws a ProjectNotInstantiatedException. If
        self.url is set and is not equal to self.datastore.url, checks to see if
        the url is in use. If it is, throws a ProjectURLTakenException."""

        if self.datastore is None:
            raise ProjectNotInstantiatedException
        else:
            if self.url and self.url != self.datastore.url:
                try:
                    duplicate = Project(url=self.url)
                    duplicate.get()
                except ProjectNotFoundException:
                    pass
                else:
                    raise ProjectURLTakenException, self.url
        self.datastore.nature = self.nature
        self.datastore.name = self.name
        self.datastore.description = self.description
        self.datastore.excerpt = self.excerpt
        self.datastore.screenshot = self.screenshot
        self.datastore.icon = self.icon
        self.datastore.images = self.images
        self.datastore.url = self.url
        self.datastore.featured = self.featured
        self.datastore.open_source = self.open_source
        self.datastore.featured_link = self.featured_link
        self.datastore.put()

    def get(self):
        """Populates the current instance of Project with the data from
        ProjectData.get(url=self.url). Throws a ProjectNotFoundException if it can't
        find self.url in the datastore. Throws a ProjectNotInstantiatedException if
        self.url is None."""

        if self.url is None:
            raise ProjectNotInstantiatedException
        else:
            datastore = ProjectData.all().filter("url =", self.url).get()
            if datastore is None:
                raise ProjectNotFoundException, self.url
            else:
                self.datastore = datastore
                self.nature = datastore.nature
                self.name = datastore.name
                self.description = datastore.description
                self.excerpt = datastore.excerpt
                self.screenshot = datastore.screenshot
                self.icon = datastore.icon
                self.images = datastore.images
                self.url = datastore.url
                self.featured = datastore.featured
                self.open_source = datastore.open_source
                self.featured_link = datastore.featured_link
                self.modified_on = datastore.modified_on
                self.modified_by = datastore.modified_by


    def get_list(self):
        """Returns a Query object for up to 1,000 ProjectData objects."""

        return ProjectData.all().fetch(1000)

    def delete(self):
        """Removes self.datastore from the datastore. Throws a
        ProjectNotInstantiatedException if self.datastore is None."""

        if self.datastore is None:
            raise ProjectNotInstantiatedException
        else:
            self.datastore.delete()
            self.datastore = None
            self.url = None
            self.nature = None
            self.name = None
            self.description = None
            self.excerpt = None
            self.screenshot = None
            self.icon = None
            self.images = None
            self.featured = None
            self.open_source = None
            self.featured_link = None
            self.modified_on = None
            self.modified_by = None