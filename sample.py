from nltk.corpus import stopwords
import wikipedia
import read_tweets
debug = 1
word_list = []
#Note for cleaning
# * remove twitter specific words like RT, # etc
# * remove ',', special characters if any. For wiki to work we need correct word without spelling mistake

#tweet = "The New York Times reported that John McCarthy died. He invented the programming langua"
tweet = ["Venezuela blackout stops subway causes traffic jams and interrupts presidential broadcast", \
         #"Rainfall warning ended for Calgary but flooding potential still exists", \
         #"Quake with prelim mag of 7.2 struck Philippines, 25 miles east-northeast of Tagbilaran, Bohoi; no tsunami warning yet", \
        #"HighParkFire UPDATE: Re-Evacuations being announced for Hwy 14, east of Seaman Reservoir" \
    ]

def console_log(var):
    if (debug):
        if type(var) == list:
            for v in var:
                print v
        else:
            print var
#remove stop words
def create_bi_grams(word_list):
    bi_grams = [ [(line[i], line[i+1]) for i in range(0, len(line)-1)] for line in word_list]
    console_log(bi_grams)
    return bi_grams

def remove_stop_words():
    word_list = [ [word  for word in line.split(' ') if word not in stopwords.words('english')] for line in tweet]
    console_log(word_list)
    return word_list

if __name__ == '__main__':
    all_configs = read_tweets.init_config()
    word_list = remove_stop_words()
    bi_grams = list(create_bi_grams(word_list))
    wiki_urls = wikipedia.get_wikipedia_urls(all_configs['url'], all_configs['dest_url'], bi_grams)
    console_log(wiki_urls)