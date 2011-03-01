#exceptions/service.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/1/11
#
#Defines exceptions that are raised by Service

class ServiceNotInstantiatedException(Exception):
    """Thrown when a Service object is referenced before it is instantiated."""

    def __str__(self):
        repr("Service not instantiated.")

class ServiceURLTakenException(Exception):
    """Thrown when a Service object is saved with a URL that already has been
    used."""

    def __init__(self, url):
        self.url = url

    def __str__(self):
        repr("The URL \"%s\" has already been used in the datastore." % self.url)

class ServiceNotFoundException(Exception):
    """Thrown when the datastore is searched for a URL that is not found in the
    datastore."""

    def __init__(self, url):
        self.url = url

    def __str__(self):
        repr("There is no service that matches \"%s\" in the database." % self.url)
