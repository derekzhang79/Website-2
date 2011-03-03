#exceptions/project_service.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/3/11
#
#Defines exceptions that are raised by ProjectService

class ProjectServiceNotInstantiatedException(Exception):
    """Thrown when a ProjectService object is referenced before it is instantiated."""

    def __str__(self):
        repr("ProjectService not instantiated.")

class ProjectServiceNotFoundException(Exception):
    """Thrown when the datastore is searched for a key or combination of project
    and service that is not found."""

    def __init__(self, var):
        self.var = var

    def __str__(self):
        repr("There is no ProjectService that matches \"%s\" in the database." % self.var)
