#exceptions/image.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/26/11
#
#Defines exceptions that are raised by Image

class ImageNotInstantiatedException(Exception):
    """Thrown when a Image object is referenced before it is instantiated."""

    def __str__(self):
        repr("Image not instantiated.")

class ImageNotFoundException(Exception):
    """Thrown when the datastore is searched for an image shortname that is not
    found in the datastore."""

    def __init__(self, url):
        self.url = url

    def __str__(self):
        repr("There is no image that matches \"%s\" in the database." % self.url)
