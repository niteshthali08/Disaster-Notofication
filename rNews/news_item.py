from rdflib import Namespace, Graph, Literal, URIRef
from person import Person
from concept import Concept
from place import Place
from organization import Organization
from common_methods import console_log
class NewsItem:
    subject_URI = None

    headline = None
    provider = None
    creator = None # tweet owner
    date_created = None
    date_published = None
    about = []
    mentions = []
    in_language = 'en'
    identifier = None
    location = None
    thumbnail_Url = None

    def __init__(self, headline = None, provider = None, date_created = None, \
    date_published = None,  thumbnail_Url = None , location = None, identifier = None ):

        self.headline = headline # text
        self.provider = provider # Twitter
        self.date_created = date_created # today's date
        self.date_published = date_published #tweet_date
        #self.about = about
        #self.mentions = mentions
        #self. in_language = in_language
        self.thumbnail_Url = thumbnail_Url
        self.location = location
        self.identifier = identifier
        console_log()
        self.subject_URI = str(identifier)

    def add_creator(self, name = None, description = None, image = None, url = None,
                 additional_info_Uri = None, given_name = None, additional_name = None, family_name = None,
                 address = None, honorific_prefix = None, honorific_suffix = None ):

        self.creator = Person (url, name, description, image, url, additional_info_Uri, given_name, additional_name,
                         family_name, address, honorific_prefix, honorific_suffix )

    def add_person(self, target, uri = None, name = None,description = None, image = None, url = None,
                 additional_info_Uri = None, given_name = None, additional_name = None, family_name = None,
                 address = None, honorific_prefix = None, honorific_suffix = None):


        person = Person (uri, name,description, image, url,additional_info_Uri, given_name, additional_name,
                         family_name, address, honorific_prefix, honorific_suffix )
        if target == 'about':
            self.about.append(person)
        elif target == 'mentions':
            self.mentions.append(person)

    def add_place(self, target, uri, name, description, image, url, additional_info_Uri, address = None,
                  geo_coordinates = None, feature_code = None):
        place = Place(uri, name, description, image, url, additional_info_Uri, address, geo_coordinates, feature_code, )

        if target == 'about':
            self.about.append(place)
        elif target == 'mentions':
            self.mentions.append(place)

    def add_organization(self, target, uri = None, name = None,  description = None, image = None, url = None,
                  additional_info_Uri = None, ticker_symbol = None, address = None):

        organization = Organization(uri, name,  description, image, url,
                  additional_info_Uri, ticker_symbol, address,)

        if target == 'about':
            self.about.append(organization)
        elif target == 'mentions':
            self.mentions.append(organization)

    def add_concept(self, target, uri = None, name = None, description = None,  image = None, url = None,
    additional_info_Uri = None ):
        concept = Concept(uri, name, description,  image, url,additional_info_Uri )

        if target == 'about':
            self.about.append(concept)
        elif target == 'mentions':
            self.mentions.append(concept)

    def save(self):
        console_log('--- Inside rNews() function of Newsitem() ---')
        console_log('subject URI: ', self.subject_URI)
        graph = Graph()

        rNews  = Namespace("http://iptc.org/std/rNews/2011-10-07#")
        console_log( 'Namespace', rNews['nitesh'])

        if self.headline != None:
            graph.add((URIRef( rNews[self.subject_URI] ), URIRef(rNews.headline), Literal(self.headline)))

        if self.provider != None:
            graph.add((URIRef(rNews[self.subject_URI]), URIRef(rNews.provider), Literal(self.provider)))

        if self.date_created != None:
            graph.add((URIRef(rNews[self.subject_URI]), URIRef(rNews.dateCreated), Literal(self.date_created)))

        if self.date_published != None:
            graph.add((URIRef(rNews[self.subject_URI]), URIRef(rNews.datePublished), Literal(self.date_published)))

        if self.in_language != None:
            graph.add((URIRef(rNews[self.subject_URI]), URIRef(rNews.inLanguage), Literal(self.in_language)))

        if self.identifier != None:
            graph.add((URIRef(rNews[self.subject_URI]), URIRef(rNews.identifier), Literal(self.identifier)))

        if self.thumbnail_Url != None:
            graph.add((URIRef(rNews[self.subject_URI]), URIRef(rNews.thumbnailUrl), Literal(self.thumbnail_Url)))

        if self.location != None:
            graph.add((URIRef(rNews[self.subject_URI]), URIRef(rNews.dateline), Literal(self.location)))

        if self.creator != None:
            #Rcreator =  ->resource($this->creator->subjectURI, "rNews:person");
            self.creator.save(rNews, graph, "person")
            graph.add((rNews[self.subject_URI], URIRef(rNews.creator), URIRef(rNews.person)))

        for obj in self.about:
            type = obj.get_type()
            if type == 'concept':
                console_log('**** Found a Concept, adding to the Graph **** ')
                obj.save(rNews, graph, "concept")
                graph.add((rNews[self.subject_URI], URIRef(rNews.about), URIRef(rNews.concept)))

            elif type == 'person':
                console_log('**** Found a Person, adding to the Graph **** ')
                obj.save(rNews, graph, "person")
                graph.add((rNews[self.subject_URI], URIRef(rNews.about), URIRef(rNews.person)))

            elif type == 'place':
                console_log('**** Found a Place, adding to the Graph **** ')
                obj.save(rNews, graph, "place")
                graph.add((rNews[self.subject_URI], URIRef(rNews.about), URIRef(rNews.place)))

            elif type == 'organization':
                console_log('**** Found a Organization, adding to the Graph **** ')
                obj.save(rNews, graph, "organization")
                graph.add((rNews[self.subject_URI], URIRef(rNews.about), URIRef(rNews.organization)))



        console_log('Serializing', graph.serialize(format="nt"))