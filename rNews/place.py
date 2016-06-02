from rdflib import URIRef, Literal
from common_methods import console_log
from concept import Concept
class Place(Concept):
    address = None
    geo_coordinates = None
    feature_code = None

    def __init__(self, uri = None, name = None, description = None, image = None, url = None,
                 additional_info_Uri = None, address = None, geo_coordinates = None, feature_code = None):

        self.address = address
        self.geo_coordinates = geo_coordinates
        self.feature_code = feature_code

        Concept.__init__(self, uri, name, description, image, url, additional_info_Uri)
    def get_type(self):
        return 'place'

    def save(self, rNews, graph, subject_URI):
        console_log('--- Inside save() function of Place ---')
        console_log('subject uri:', self.subject_URI)
        console_log('name:', self.name)
        console_log('description:', self.description)
        console_log('image:', self.image)
        console_log('url:', self.url)
        console_log('additional_info_uri:', self.additional_info_Uri)

        Concept.save(self, rNews, graph, subject_URI)
        if self.geo_coordinates != None:
            graph.add((URIRef(rNews[self.subject_URI]), URIRef(rNews.geo_coordinates), Literal(self.geo_coordinates)))

        if self.feature_code != None:
            graph.add((URIRef(rNews[self.subject_URI]), URIRef(rNews.feature_code), Literal(self.feature_code)))


if __name__ == '__main__':
    p = Place('a', 'b', 'c','gg', 'hh', 'ii', 'jj', 'kk', 'll')
    console_log(p.address)
    console_log(p.additional_info_Uri)
