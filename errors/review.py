#exceptions/page.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/26/11
#
#Defines exceptions that are raised by Page

class PageNotInstantiatedException(Exception):
    """Thrown when a Page object is referenced before it is instantiated."""

    def __str__(self):
        repr("Page not instantiated.")

class PageURLTakenException(Exception):
    """Thrown when a Page object is saved with a URL that already has been
    used."""

    def __init__(self, url):
        self.url = url

    def __str__(self):
        repr("The URL \"%s\" has already been used in the datastore." % self.url)

class PageURLReservedException(Exception):
    """Thrown when a Page object is saved with a URL that matches a reserved
    URL."""

    def __init__(self, url):
        self.url = url

    def __str__(self):
        repr("\"%s\" is a reserved URL by the system, and can't be used." % self.url)

class PageNotFoundException(Exception):
    """Thrown when the datastore is searched for a URL that is not found in the
    datastore."""

    def __init__(self, url):
        self.url = url

    def __str__(self):
        repr("There is no page that matches \"%s\" in the database." % self.url)
