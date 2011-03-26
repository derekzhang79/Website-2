#models/service.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/3/11
#
#Defines the datastore interface for services.

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from datastore import ServiceData
from models.project_service import *
from errors.service import *

from google.appengine.api import memcache

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

    projects = []

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

        self.projects = []

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
            memcache.set("models/service/%s" % self.url, self.datastore)
            memcache.delete("models/services/list")
            memcache.delete("models/services/featured")

    def get(self):
        """Populates the current instance of Service with data from the
        datastore. Throws a ServiceNotInstantiatedException if self.url is None.
        Throws a ServiceNotFoundException if self.url doesn't exist in the
        datastore."""

        if self.url is None:
            raise ServiceNotInstantiatedException
        else:
            datastore = memcache.get("models/service/%s" % self.url)
            if datastore is None:
                datastore = ServiceData.all().filter("url =", self.url).get()
                if datastore is not None:
                    memcache.set("models/service/%s" % self.url, datastore)
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
                self.get_projects()
    
    def get_list(self):
        """Returns a Query object for up to 1,000 ServiceData objects."""
        services = memcache.get("models/services/list")
        if services is None:
            services = ServiceData.all().order("-modified_on").fetch(1000)
            memcache.set("models/services/list", services)
        return services

    def get_featured(self):
        """Returns a Query object for up to 1,000 ServiceData objects. Returns
        only ServiceData objects that have featured as True."""
        services = memcache.get("models/services/list")
        if services is None:
            services = ServiceData.all().filter("featured =", True).order("-modified_on").fetch(1000)
            memcache.set("models/services/featured", services)
        return services

    def delete(self):
        """Removes self.datastore from the datastore. Throws a
        ServiceNotInstantiatedException if self.datastore is None."""

        if self.datastore is None:
            raise ServiceeNotInstantiatedException
        else:
            memcache.delete("models/service/%s" % self.datastore.url)
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
            
            self.projects = []

    def get_projects(self):
        """Retrieves all the ProjectData objects associated with this Service,
        and converts them to ProjectService objects, which are returned as a list.
        Throws a ServiceNotInstantiatedException if self.datastore is None."""

        if self.datastore is None:
            raise ServiceNotInstantiatedException
        else:
            projects = memcache.get("models/services/%s/projects" % self.datastore.url)
            if projects is None:
                rel = ProjectService(service=self.datastore)
                rel_data = rel.get_all_matching()
                projects = []
                for relationship in rel_data:
                    projects.append(ProjectService(datastore=relationship))
                memcache.set("models/services/%s/projects" % self.datastore.url, projects)
            self.projects = projects

    def add_project(self, project, content=None):
        """Adds a ProjectServiceData object to the datastore associated with
        the current ServiceData object. Accepts a ProjectData object as an
        argument. Optionally accepts a content argument to explain the
        relationship. Throws a ServiceNotInstantiatedException if self.datastore
        is None."""

        if self.datastore is None:
            raise ServiceNotInstantiatedException
        else:
            relationship = ProjectService(project=project, service=self.datastore, content=content)
            relationship.save()
            memcache.delete("models/services/%s/projects", self.datastore.url)

    def remove_project(self, project):
        """Removes a ProjectServiceData object from the datastore. Accepts a
        ProjectData object as an argument. Throws a
        ServiceNotInstantiatedException if self.datastore is None. Throws a
        ProjectServiceNotFoundException if no datastore records match."""

        if self.datastore is None:
            raise ServiceNotInstantiatedException
        else:
            rel = ProjectService(service=self.datastore, project=project)
            rel_data = rel.get_all_matching()
            if rel_data is None or rel_data == []:
                raise ProjectServiceNotFoundException, {"project":project,
                                                        "service":service}
            else:
                for relationship in rel_data:
                    relationship.delete()
            memcache.delete("models/services/%s/projects", self.datastore.url)
            self.get_projects()
