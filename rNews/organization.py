from common_methods import console_log
from concept import Concept
class Organization(Concept):
    ticker_symbol = None
    address = None

    def __init__( self, uri = None, name = None,  description = None, image = None, url = None,
                  additional_info_Uri = None, ticker_symbol = None, address = None):

        self.ticker_symbol = ticker_symbol
        self.address = address
        Concept.__init__(self, uri, name, description, image, url, additional_info_Uri)
    def get_type(self):
        return 'Person'

    def save(self, rdf_lib):
        pass

if __name__ == '__main__':
    o = Organization('a', 'b','gg', 'hh', 'ii', 'jj', 'kk', 'll')
    console_log(o.ticker_symbol)
    console_log(o.additional_info_Uri)
