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
        return 'Person'

    def save(self, rdf_lib):
        pass

if __name__ == '__main__':
    p = Place('a', 'b', 'c','gg', 'hh', 'ii', 'jj', 'kk', 'll')
    console_log(p.address)
    console_log(p.additional_info_Uri)
