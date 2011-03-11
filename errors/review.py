#exceptions/review.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 3/10/11
#
#Defines exceptions that are raised by Review

class ReviewNotInstantiatedException(Exception):
    """Thrown when a Review object is referenced before it is instantiated."""

    def __str__(self):
        repr("Review not instantiated.")

class ReviewURLTakenException(Exception):
    """Thrown when a Review object is saved with a URL that already has been
    used."""

    def __init__(self, url):
        self.url = url

    def __str__(self):
        repr("The URL \"%s\" has already been used in the datastore." % self.url)

class ReviewNotFoundException(Exception):
    """Thrown when the datastore is searched for a URL that is not found in the
    datastore."""

    def __init__(self, url):
        self.url = url

    def __str__(self):
        repr("There is no review that matches \"%s\" in the database." % self.url)
