#exceptions/project.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/26/11
#
#Defines exceptions that are raised by Project

class ProjectNotInstantiatedException(Exception):
    """Thrown when a Project object is referenced before it is instantiated."""

    def __str__(self):
        repr("Project not instantiated.")

class ProjectURLTakenException(Exception):
    """Thrown when a Project object is saved with a URL that already has been
    used."""

    def __init__(self, url):
        self.url = url

    def __str__(self):
        repr("The URL \"%s\" has already been used in the datastore." % url)

class ProjectNotFoundException(Exception):
    """Thrown when the datastore is searched for a project URL that is not found in the
    datastore."""

    def __init__(self, url):
        self.url = url

    def __str__(self):
        repr("There is no project that matches \"%s\" in the database." % url)
