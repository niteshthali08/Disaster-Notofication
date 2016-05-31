from nltk.corpus import stopwords
import wikipedia
import read_tweets
from read_tweets import console_log
from nltk import word_tokenize
from generate_news import GenerateNews
from wordnet_screening import Wordnet
from tweeter import Tweeter
debug = 1
word_list = []
"""
create article is the main program which will call other modules. Create article is reponsible for following things
* Word Tokenization
* Stop Word Removal
* Calls wordnet to shorten the list of words.
#Note for cleaning
# * remove twitter specific words like RT, # etc
# * remove ',', special characters if any. For wiki to work we need correct word without spelling mistake
"""

#tweet = "The New York Times reported that John McCarthy died. He invented the programming langua"
tweets = ["Venezuela blackout stops subway causes traffic jams and interrupts presidential broadcast", \
         #"Rainfall warning ended for Calgary but flooding potential still exists", \
         #"Quake with prelim magnitude of 7.2 struck Philippines, 25 miles east-northeast of Tagbilaran, Bohoi; no tsunami warning yet", \
        #"HighParkFire UPDATE: Re-Evacuations being announced for Hwy 14, east of Seaman Reservoir" \
    ]

# def console_log(var):
#     print var
#remove stop words
# def create_bi_grams(line):
#     bi_grams = [(line[i], line[i + 1]) for i in range(0, len(line) - 1)]
#     return bi_grams

def remove_stop_words(line):
    #word_list = [ [word  for word in line.split(' ') if word not in stopwords.words('english')] for line in tweet]
    word_list = [word  for word in line if word not in stopwords.words('english')]
    return word_list

if __name__ == '__main__':
    # Run all of this methods on each of the tweets.
    url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageprops&ppprop=disambiguation&\
    redirects&titles="
    dest_url = "https://en.wikipedia.org/wiki/"
    tw = Tweeter()
    tw.get_one_tweet()
    tw.text = "Barak Obama" # hardcoding for time being
    # for now hard code one tweet and proceed
    word_list = remove_stop_words(word_tokenize(tw.text))
    console_log(word_list)
    wn = Wordnet()
    pos_word_list = wn.pos_word_list(word_list)
    bi_grams =wn.get_bi_gram_candidates(pos_word_list)
    #console_log('bi grams: ', bi_grams)
    uni_grams = wn.get_uni_gram_candidates(pos_word_list)
    #console_log('uni grams: ', uni_grams)
    bg_wiki_url_terms = wikipedia.get_wikipedia_urls(url, dest_url, bi_grams)
    console_log('bg wiki terms: ', bg_wiki_url_terms)
    unknown_uni_grams = wikipedia.clean_uni_gram_candidates(uni_grams, bg_wiki_url_terms)
    #console_log('unknown_uni_grams ', unknown_uni_grams)
    ug_wiki_url_terms = wikipedia.get_wikipedia_urls(url, dest_url, unknown_uni_grams)
    console_log('ug wiki terms ', ug_wiki_url_terms)
    all_wiki_url_terms = bg_wiki_url_terms + ug_wiki_url_terms
    myArticle = GenerateNews()
    console_log("tw: ", tw)
    myArticle.create(tw)
    #exit(-1)
    #all_wiki_url_terms = [["Barak Obama", "Barak_Obama"]]
    myArticle.annotate(all_wiki_url_terms, tw.text)
    myArticle.save_article()