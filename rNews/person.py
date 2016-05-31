from common_methods import console_log
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
        return 'Person'

    def save(self, rdf_lib):
        pass

if __name__ == '__main__':
    p = Person('a', 'b', 'c', 'd','e','f','gg', 'hh', 'ii', 'jj', 'kk', 'll')
    console_log(p.honorific_prefix)
    console_log(p.additional_info_Uri)
