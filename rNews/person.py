from common_methods import console_log
from rdflib import URIRef, Literal
from concept import Concept
class Person(Concept):
    given_name = None
    additional_name = None
    family_name = None
    address = None
    honorific_prefix = None
    honorific_suffix = None

    def __init__(self, uri = None, name = None,description = None, image = None, url = None,
                 additional_info_Uri = None, given_name = None, additional_name = None, family_name = None,
                 address = None, honorific_prefix = None, honorific_suffix = None):

        self.given_name = given_name
        self.additional_name = additional_name
        self.family_name = family_name
        self.address = address
        self.honorific_prefix = honorific_prefix
        self.honorific_suffix = honorific_suffix

        Concept.__init__(self, uri, name, description, image, url, additional_info_Uri)


    def get_type(self):
        return 'person'

    def save(self, rNews, graph, subject_URI):
        console_log('--- Inside save() function of Person')
        console_log('subject uri:', self.subject_URI)
        console_log('name:', self.name)
        console_log('description:', self.description)
        console_log('image:', self.image)
        console_log('url:', self.url)
        console_log('additional_info_uri:', self.additional_info_Uri)
        console_log('given_name:', self.given_name)
        console_log('additional_name:', self.additional_name)
        console_log('family_name:', self.family_name)
        console_log('address:', self.address)
        console_log('honorific_prefix:', self.honorific_prefix)
        console_log('honorific_suffix', self.honorific_suffix)
        # if self.name != None:
        #     graph.add((URIRef(rNews[subject_URI]), URIRef(rNews.name), Literal(self.name)))
        #
        # if self.description != None:
        #     graph.add((URIRef(rNews[subject_URI]), URIRef(rNews.description), Literal(self.description)))
        #
        # if self.url != None:
        #     graph.add((URIRef(rNews[subject_URI]), URIRef(rNews.url), Literal(self.url)))
        #
        # if self.image != None:
        #     graph.add((URIRef(rNews[subject_URI]), URIRef(rNews.image), Literal(self.image)))
        #
        # if self.additional_info_Uri != None:
        #     graph.add(
        #         (URIRef(rNews[subject_URI]), URIRef(rNews.additional_info_Uri), Literal(self.additional_info_Uri)))

        Concept.save(self, rNews, graph, subject_URI)

        if self.given_name != None:
            graph.add((URIRef(rNews[subject_URI]), URIRef(rNews.given_name), Literal(self.given_name)))

        if self.additional_name != None:
            graph.add((URIRef(rNews[subject_URI]), URIRef(rNews.additional_name), Literal(self.additional_name)))

        if self.family_name != None:
            graph.add((URIRef(rNews[subject_URI]), URIRef(rNews.family_name), Literal(self.family_name)))

        if self.address != None:
            graph.add((URIRef(rNews[subject_URI]), URIRef(rNews.address), Literal(self.address)))

        if self.honorific_prefix != None:
            graph.add((URIRef(rNews[subject_URI]), URIRef(rNews.honorific_prefix), Literal(self.honorific_prefix)))

        if self.honorific_suffix != None:
            graph.add((URIRef(rNews[subject_URI]), URIRef(rNews.honorific_suffix), Literal(self.honorific_suffix)))


if __name__ == '__main__':
    p = Person('a', 'b', 'c', 'd','e','f','gg', 'hh', 'ii', 'jj', 'kk', 'll')
    console_log(p.honorific_prefix)
    console_log(p.additional_info_Uri)
