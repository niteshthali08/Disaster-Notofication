from rdflib import URIRef, Literal
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
        return 'concept'

    def save(self, rNews, graph, subject_URI ):

        if self.name != None:
            graph.add((URIRef(rNews[subject_URI]), URIRef(rNews.name), Literal(self.name)))

        if self.description != None:
            graph.add((URIRef(rNews[subject_URI]), URIRef(rNews.description), Literal(self.description)))

        if self.url != None:
            graph.add((URIRef(rNews[subject_URI]), URIRef(rNews.url), Literal(self.url)))

        if self.image != None:
            graph.add((URIRef(rNews[subject_URI]), URIRef(rNews.image), Literal(self.image)))

        if self.additional_info_Uri != None:
            graph.add((URIRef(rNews[subject_URI]), URIRef(rNews.additional_info_Uri), Literal(self.additional_info_Uri)))