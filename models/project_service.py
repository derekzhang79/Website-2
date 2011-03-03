#models/project_service.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/3/11
#
#Defines the datastore interface for the HABTM relationship between Projects and Services.

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from datastore import ProjectServiceData

class ProjectService():
    """Defines datastore interactions for the Has-And-Belongs-To-Many
    relationship betweent Projects and Services."""

    #attributes
    project = None
    service = None
    content = None
    datastore = None
    key = None

    def __init__(self, datastore=None, project=None, service=None, content=None, key=None):
        """Defines the initialization method for a ProjectService object. Accepts the
        datastore (an instance of a ProjectServiceData object), the project (an
        instance of a ProjectData object), the service (an instance of a
        ServiceData object), the content (a Text description of how the Service
        was used in the Project), and the datastore key for the relationship, all optional."""

        #reset all local variables
        self.project = None
        self.service = None
        self.content = None
        self.datastore = None
        self.key = None

        if datastore is not None:
            self.datastore = datastore
            self.project = Project(datastore=datastore.project)
            self.service = Service(datastore=datastore.service)
            self.content = datastore.content
            self.key = datastore.key()
        else:
            self.datastore = ProjectServiceData()
        if project is not None:
            self.project = Project(datastore=project)
        if service is not None:
            self.service = Service(datastore=service)
        if content is not None:
            self.content = content
        if key is not None:
            self.key = key

    def save(self):
        """Writes the current instance of ProjectService to the datastore as a
        ProjectServiceData object. If ProjectService.datastore is not set, throws a
        ProjectServiceNotInstantiatedException."""

        if self.datastore is None:
            raise ProjectServiceNotInstantiatedException
        else:
            self.datastore.project = self.project.datastore
            self.datastore.service = self.service.datastore
            self.datastore.content = self.content
            self.datastore.put()

    def get(self):
        """Populates the current instance of ProjectService with the data from
        ProjectServiceData.get(self.key). Throws a ProjectServiceNotFoundException
        if it can't find self.key in the datastore. Throws a
        ProjectServiceNotInstantiatedException if self.key is None."""

        if self.key is None:
            raise ProjectServiceNotInstantiatedException
        else:
            datastore = ProjectServiceData.get(self.key)
            if datastore is None:
                raise ProjectServiceNotFoundException, self.key
            else:
                self.datastore = datastore
                self.project = Project(datastore=datastore.project)
                self.service = Service(datastore=datastore.service)
                self.content = datastore.content

    def delete(self):
        """Removes the current instance of ProjectService from the datastore. Throws a
        ProjectServiceNotInstantiatedException if self.datastore is None."""

        if self.datastore is None:
            raise ProjectServiceNotInstantiatedException
        else:
            self.datastore.delete()
            self.datastore = None
            self.project = None
            self.service = None
            self.content = None
