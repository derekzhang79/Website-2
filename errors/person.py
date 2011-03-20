#exceptions/person.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/20/11
#
#Defines exceptions that are raised by Person

class PersonNotInstantiatedException(Exception):
    """Thrown when a Person object is referenced before it is instantiated."""

    def __str__(self):
        repr("Person not instantiated.")

class PersonURLTakenException(Exception):
    """Thrown when a Person object is saved with a URL that already has been
    used."""

    def __init__(self, url):
        self.url = url

    def __str__(self):
        repr("The URL \"%s\" has already been used in the datastore." % self.url)

class PersonNotFoundException(Exception):
    """Thrown when the datastore is searched for a URL that is not found in the
    datastore."""

    def __init__(self, url):
        self.url = url

    def __str__(self):
        repr("There is no person that matches \"%s\" in the database." % self.url)
