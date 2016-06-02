import urllib
from rdflib import URIRef
import requests
from read_tweets import console_log
from dbp_graph import LODCloud
import datetime
import time
import sys

sys.path.insert(0, './rNews')
from news_item import NewsItem

class GenerateNews:
    """Class will help in querying DBPedia and extracting equivalent URIs for Wikipedia links
    """
    r_news_article = ""
    def create(self, tw):
        self.r_news_article = NewsItem(tw.text, "Twitter", time.strftime('%Y-%m-%d', time.localtime(tw.tweet_date)),
                                       datetime.datetime.today().strftime('%Y-%m-%d'),tw.media, tw.location,
                                       tw.tweet_id)
        url = "http://twitter.com/" + tw.screen_name
        console_log('URL: ', url)
        console_log('headline: ', self.r_news_article.headline)

        self.r_news_article.add_creator(tw.screen_name, tw.description, tw.profile_image_url, url, tw.urls,
                                        tw.author_name, additional_name = None, family_name = None, address = None,
                                        honorific_prefix = None, honorific_suffix = None)
        console_log(self.r_news_article)

    def get_DBPedia_URI(self, wiki_term):
        console_log('--- Inside get_DBPedia_URI() function')
        format = "json"
        query = "SELECT ?uri ?label " \
        + "WHERE { "\
        + "?uri rdfs:label ?label . " \
        + "filter(?label='" + wiki_term + "'@en) . " \
        + "}";

        #console_log( "query: " + query)
        dbp_URL = 'http://dbpedia.org/sparql?' \
        + 'query='  + query \
        + '&format=' + format;
        console_log("dbp_URL: " + dbp_URL)
        return dbp_URL

    def make_request(self, url):

        response_json = requests.get(url).json()
        return response_json;

    def save_article(self):
        self.r_news_article.save()

    def annotate(self, wiki_url_terms, tweet):
        """main function which will receive all wikipedia links and will try to dereference them using dbpedia
        sample JSON
        "results": {
            "distinct": false,
            "ordered": true,
            "bindings": [{
                "uri": {
                    "type": "uri",
                    "value": "http://dbpedia.org/resource/Category:Venezuela"
                },
                "label": {
                    "type": "literal",
                    "xml:lang": "en",
                    "value": "Venezuela"
                }
            }, {
                "uri": {
                    "type": "uri",
                    "value": "http://dbpedia.org/resource/Venezuela"
                },
                "label": {
                    "type": "literal",
                    "xml:lang": "en",
                    "value": "Venezuela"
                }
            }
        }]
        }
        """
        for pair in wiki_url_terms:
            requestURL = self.get_DBPedia_URI(pair[1])
            response_json = self.make_request(requestURL)
            console_log(response_json)
            graph = LODCloud()
            for candidate in response_json['results']['bindings']:
                uri = candidate['uri']['value']
                if uri.startswith("http://dbpedia.org/resource/"):
                    if "Category" not in uri:
                        graph.load_graph(uri)
                        graph.context = tweet
                        graph.term = pair[1]
                        graph.disambiguate()
                        type = graph.getType()
                        console_log('type: ', type)
                        name = pair[1]
                        if len(name) == 0 :
                            name = [None] * 3

                        description = graph.get_abstract(None, URIRef("http://dbpedia.org/ontology/abstract"), "en")
                        if len(description) == 0 :
                            console_log('abstract length is 0...')
                            description =  [(None, None, None)]
                        console_log('abstract for adding to ontology: ', description)

                        image = graph.get(None, URIRef("http://xmlns.com/foaf/0.1/depiction"), None, None)
                        if len(image) == 0 :
                            image = [(None, None, None)]
                            console_log(image)
                        console_log('image  for adding to ontology: ', image)

                        url = graph.get(None, URIRef("http://xmlns.com/foaf/0.1/isPrimaryTopicOf"), None, None)
                        if (len(url) == 0):
                            url =  [(None, None, None)]
                        console_log('url for adding to ontology: ', url)

                        if type == 'Person':
                            given_name = graph.get(None , "http://xmlns.com/foaf/0.1/givenName", None, None)
                            if (len(given_name) == 0):
                                given_name = [(None, None, None)]
                            console_log('given_name  for adding to ontology: ', given_name)

                            family_name = graph.get(None , "http://xmlns.com/foaf/0.1/surname", None, None)
                            if (len(family_name) == 0):
                                family_name =  [(None, None, None)]
                            console_log('family_name for adding to ontology: ', family_name)
                                # token, uri(graph is loaded), name(current word), abstract, image, wiki_url(primary topic)
                            #
                            self.r_news_article.add_person('about', graph.uri, name, description, image[0][2], url[0][2],
                                                           additional_info_Uri= None, given_name = given_name[0][2],
                                                           additional_name= None, family_name = family_name[0][2],
                                                           address=None, honorific_prefix=None, honorific_suffix=None)
                        elif type == 'Place':
                            point = graph.get(None, URIRef("http://www.georss.org/georss/point"), None, None);
                            self.r_news_article.add_place('about', graph.uri, name, description, image[0][2],
                                                           url[0][2], additional_info_Uri=None, address = None,
                                                            geo_coordinates = point, feature_code=None)
                        elif type == 'Organization':
                            self.r_news_article.add_organization('about', graph.uri,  name, description, image[0][2],
                                                           url[0][2], additional_info_Uri=None, ticker_symbol = None,
                                                              address = None)
                        else:
                            self.r_news_article.add_concept('about', graph.uri, name, description, image[0][2],
                                                              url[0][2], additional_info_Uri=None)





if __name__ == '__main__':
    a = {
        'interrupts': 'https://en.wikipedia.org/wiki/Interrupt',
        'stops': 'https://en.wikipedia.org/wiki/Stop',
        'presidential': 'https://en.wikipedia.org/wiki/President',
        'causes': 'https://en.wikipedia.org/wiki/Causes',
        'blackout': 'https://en.wikipedia.org/wiki/Blackout',
        'Venezuela': 'https://en.wikipedia.org/wiki/Venezuela',
        'traffic jams': 'https://en.wikipedia.org/wiki/Traffic_congestion',
        'subway': 'https://en.wikipedia.org/wiki/Subway'
    }

    b = {
        '25': '<https://en.wikipedia.org/wiki/25>',
        'tsunami warning': '<https://en.wikipedia.org/wiki/Tsunami_warning_system>',
        'Quake': '<https://en.wikipedia.org/wiki/Quake>',
        'no': '<https://en.wikipedia.org/wiki/No>',
        'miles': '<https://en.wikipedia.org/wiki/Mile>',
        'east-northeast': '<https://en.wikipedia.org/wiki/Points_of_the_compass>',
        'mag': '<https://en.wikipedia.org/wiki/Mag>',
        'prelim': '<https://en.wikipedia.org/wiki/Preliminary>',
        'struck': '<https://en.wikipedia.org/wiki/Struck>',
        'warning': '<https://en.wikipedia.org/wiki/Warning>'
    }
    tweet = "Venezuela blackout stops subway causes traffic jams and interrupts presidential broadcast"
    a_l = [['Venezuela', u'Venezuela'], ['blackout', u'Blackout'], ['stops', u'Stop'], ['subway', u'Subway'],\
           ['causes', u'Causes'], ['traffic jams', u'Traffic_congestion'], ['interrupts', u'Interrupt'],\
           ['presidential', u'President'], ['broadcast', u'Broadcasting']]
    b_l = [['Venezuela', u'Venezuela']]
    my_list = [a , b]
    myObj = GenerateNews()
    myObj.annotate(b_l, tweet)