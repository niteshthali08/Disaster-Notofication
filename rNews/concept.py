class Concept:

    subject_URI = None
    name = None
    description = None #from http://schema.org/Thing
    image = None
    url = None
    additional_info_Uri = None

    def __init__(self,  uri = None, name = None, description = None,  image = None, url = None,
    additional_info_Uri = None ):

        self.subject_URI = uri
        self.name = name
        self.description = description
        self.image = image
        self.url = url
        self.additional_info_Uri = additional_info_Uri

    def get_type(self):
        return 'Concept'

    def save(self, rdf_lib):
        pass