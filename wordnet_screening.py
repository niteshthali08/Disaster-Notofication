from nltk.corpus import wordnet
from read_tweets import console_log

class Wordnet:
        def is_empty(self, result):
            if result[0] == None and \
                            result[1] == None and \
                            result[2] == None and \
                            result[3] == None : \
                return True
            else:
                return False

        def is_numeric(self, word):
            try:
                int(word)
                return True
            except:
                return False
        def is_pos_present(self, pos):
            if pos == None:
                return False
            return True

        def is_bi_gram_valid(self, l1, l2):
            """valid bi_grams are
            empty - empty,
            empty - (noun/adjective)
            (noun/adjective) - empty,
            adj - noun,
            noun - noun
            """
            if (self.is_empty(l1)):
                if (self.is_empty(l2) or self.is_pos_present(l2[2]) or self.is_pos_present(l2[3])):
                    return True

            if (self.is_empty(l2)):
                if (self.is_pos_present(l1[2]) or self.is_pos_present(l1[3])):
                    return True
            if (self.is_pos_present(l1[2]) and self.is_pos_present(l2[3])):
                return True

            if (self.is_pos_present(l1[3]) and self.is_pos_present(l2[3])):
                return True

            return False

        def pos_word_list(self, word_list):
            console_log('--- Inside reduce_word_list() function ----')
            enriched_words = []
            for word in word_list:
                if len(word) > 2 :
                    result = self.determine_word_type(word)
                    if self.is_empty(result):
                        result = self.determine_word_type(word[: len(word)-1])
                    enriched_words.append([word, result])
            return enriched_words


        def determine_word_type(self, word):
            console_log('--- Inside determine_word_type() function ----')
            result = [None] * 4 # numeric, verb, adjective, noun

            if self.is_numeric(word):
                result[0] = "numeric"
            else:
                syns = wordnet.synsets(word)
                pos = [syn.pos() for syn in syns]
                pos = set(pos)
                for p in pos:
                    if p == 'v':
                        result[1] = "verb"
                    elif p == 'a':
                        result[2] = "adjectve"
                    elif p == 'n':
                        result[3] = "noun"

            return result

        def get_bi_gram_candidates(self, pos_word_list):
            bi_grams = []
            for i in range(0, len(pos_word_list) - 1):
                if self.is_bi_gram_valid(pos_word_list[i][1], pos_word_list[i + 1][1]):
                    bi_grams.append(pos_word_list[i][0] + " " + pos_word_list[i+1][0])

            return bi_grams

        def get_uni_gram_candidates(self, pos_word_list):
            uni_grams = []
            for i in range(0, len(pos_word_list)):
                if (self.is_empty(pos_word_list[i][1]) or self.is_pos_present(pos_word_list[i][1][3])):
                    uni_grams.append(pos_word_list[i][0])
            return uni_grams
if __name__ == '__main__':
    # Run all of this methods on each of the tweets.
    tweet = "Venezuela blackout stops subway causes traffic jams and interrupts presidential broadcast"
    #word_list = remove_stop_words(word_tokenize(tweet))
    wn = Wordnet()
    wl = wn.pos_word_list(tweet.split(' '))
    bi_grams = wn.get_bi_gram_candidates(wl)
    uni_grams = wn.get_uni_gram_candidates(wl)
    console_log('bi grams', bi_grams)
    console_log('uni grams', uni_grams)