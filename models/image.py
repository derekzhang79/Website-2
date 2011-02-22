#models/image.py
#
#Authors:
#   Paddy Foran <paddy@secondbit.org>
#Last Modified: 2/22/11
#
#Defines the datastore interface for uploaded images.

class Image():
    """Defines datastore interactions for uploaded images."""

    #attributes
    image = None
    original = None
    mimetype = None
    shortname = None
    uploaded_by = None
    uploaded_on = None
    height = None
    width = None
    datastore = None

    def __init__(self, image=None, shortname=None, mimetype=None, original=None, datastore=None, height=None, width=None):
        """Defines the initialization method for an Image object. Accepts the
        image (the raw bytes of the image data), the shortname (used in the 
        URL), the mimetype, the original image (a reference to an ImageData 
        instance, if this is a resizing of an image), a datastore (a reference
        to an ImageData instance), a height, and a width, all optional."""

        #reset all local variables
        self.image = None
        self.original = None
        self.mimetype = None
        self.shortname = None
        self.uploaded_by = None
        self.uploaded_on = None
        self.height = None
        self.width = None
        self.datastore = None

        if datastore is not None:
            self.datastore = datastore
            self.image = datastore.image
            self.original = datastore.original
            self.mimetype = datastore.mimetype
            self.shortname = datastore.shortname
            self.uploaded_by = datastore.uploaded_by
            self.uploaded_on = datastore.uploaded_on
            self.height = datastore.height
            self.width = datastore.width
        if original is not None:
            self.original = original
            self.image = original.image
            self.mimetype = original.mimetype
            self.shortname = original.shortname
        if shortname is not None:
            self.shortname = shortname
        if image is not None:
            self.image = image
        if mimetype is not None:
            self.mimetype = mimetype
        if height is not None:
            self.height = height
        if width is not None:
            self.width = width

    def save(self):
        """Writes the current instance of Image to the datastore as an ImageData
        object. If Image.datastore is set, the referenced ImageData will be
        updated, instead of creating a clone. Throws an
        ImageShortNameInUseException if self.shortname exists in the datastore
        and doesn't match self.datastore.shortname."""

        if self.datastore is None:
            self.datastore = ImageData()
        if self.shortname is not None and self.shortname != self.datastore.shortname:
            duplicate = ImageData.all().filter("shortname =", self.shortname).get()
            if duplicate is not None:
                raise ImageShortNameInUseException, self.shortname
        self.datastore.image = self.image
        self.datastore.original = self.original
        self.datastore.mimetype = self.mimetype
        self.datastore.shortname = self.shortname
        self.datastore.height = self.height
        self.datastore.width = self.width
        self.datastore.put()

    def get(self):
        """Populates the current instance of Image with the data from
        ImageData.get(self.shortname). Throws an ImageNotFoundException if it
        can't find self.shortname in the datastore."""

        if self.shortname is None:
            raise ImageNotFoundException, self.shortname
        else:
            datastore = ImageData.all().filter("shortname =", self.shortname).get()
            if datastore is None:
                raise ImageNotFoundException, self.shortname
            else:
                self.datastore = datastore
                self.image = datastore.image
                self.original = datastore.original
                self.mimetype = datastore.mimetype
                self.shortname = datastore.shortname
                self.uploaded_by = datastore.uploaded_by
                self.uploaded_on = datastore.uploaded_on
                self.height = datastore.height
                self.width = datastore.width
