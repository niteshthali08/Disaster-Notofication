from rdflib import Graph, URIRef, Literal
from nltk.corpus import stopwords
#from create_article import remove_stop_words
import sys
import wordnet_screening
from read_tweets import console_log
from nltk.stem import PorterStemmer

class LODCloud():
    uri = None # on which parse method is called
    g = None # loaded graph is stored here
    term = None # current word from tweet
    context = None # context is text of the tweet

    def create_triplets(self):
        "Pass"
    def load_graph(self, uri):
        try:
            console_log("--- Inside load_graph() function ---")
            console_log("UIR for loading graph: ", uri)
            g = Graph()
            g.parse(source = uri)
            self.uri = uri
            self.g = g
        except:
            console_log("*** Unexpected error while parsing Graph *** \n")
            console_log(sys.exc_info())
            raise

    def get(self, sub, pred, obj, lang):
        """
        This will search DBpedia and return triples matching params
        :param sub: subject
        :param pred: predicate
        :param obj: object
        :param lang: languagge
        :return: returns list containing [sub, pred, obj] which matches the search criteria set by params
        """
        console_log("--- Inside get() function ---")
        result = [(s, p, o) for s, p, o in self.g.triples( (sub, pred, obj))  ]
        return result

    def getType(self):
        """
        Function will search dbpedia based on the predicate "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        to determine the type of the subject
        :return: type of the subject
        """
        console_log('--- Inside getType() function --- ')
        type = "concept"
        type_triples = self.get(None, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), None, None)
        for triple in type_triples:
            if triple[2].decode().lower() == "http://schema.org/Person".lower():
                type = "Person"
                return type

            if triple[2].decode().lower() == "http://dbpedia.org/ontology/Place".lower():
                type = "Place"
                return type

            if triple[2].decode().lower() == "http://schema.org/Organization".lower():
                type = "Organization"
                return type

    def stem_and_clean(self, text):
        console_log('--- Inside stem and clean ---')
        words = [word for word in text.split(' ') if word not in stopwords.words('english')]
        stemmer = PorterStemmer()
        result = [stemmer.stem(word) for word in words ]
        return result

    def get_abstract(self, sub, pred, lan):
        console_log("--- Inside get_abstract() --- ")
        console_log("sub:", sub)
        console_log("pred:", pred)
        obj = self.g.objects(sub, pred)
        for ln in obj:
            if ln.language == 'en':
                return ln
    def get_relevance(self, abstract):
        console_log('--- Inside get_relevance() function --- ')
        result = set(self.stem_and_clean(abstract)).intersection(self.stem_and_clean(self.context))
        return len(result)

    def disambiguate(self):
        console_log("--- Inside disambiguate() function ---")
        abstract = self.get(None, URIRef("http://dbpedia.org/ontology/abstract"), None, 'en');
        disambiguate = self.get(None, URIRef("http://dbpedia.org/ontology/wikiPageDisambiguates"), None, \
                                None);
        console_log("abstract len", str(len(abstract)))
        console_log("disambiguate len", str(len(disambiguate)) )
        if (len(abstract) == 0 and len(disambiguate) > 0):
            """resolve ambiguity"""
            best  = ["", -1]
            for candidate in disambiguate:
                try:
                    uri = candidate[2].replace('resource', 'page')
                    console_log('uri for load: ', uri)
                    self.load_graph(uri.decode())
                    abstract = self.get_abstract(URIRef(candidate[2]), \
                                    URIRef("http://dbpedia.org/ontology/abstract"), 'en')
                    console_log('abstract now:', abstract)
                    matches = 0
                    if abstract != None:
                        matches = self.get_relevance(abstract)
                        console_log('*** matches', matches)
                    if matches > best[1] :
                        best[1] = matches
                        best[0] = uri.decode()
                        console_log('*** Best so far: ', best[0])
                except:
                    console_log("*** Unexpected error while performing disambiguation **** \n:")
                    console_log(sys.exc_info())
            console_log('Final Best: ', best[0])
            self.load_graph(best[0])

if __name__ == '__main__':
    tweet = "Venezuela blackout stops subway causes traffic jams and interrupts presidential broadcast"
    uri = 'http://dbpedia.org/resource/Subway'
    lod = LODCloud()
    lod.load_graph(uri)
    lod.context = tweet
    lod.disambiguate()
