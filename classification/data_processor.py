from nltk.corpus import stopwords
from nltk import FreqDist
import pandas as pd;
import numpy as np;
import time
from sklearn import svm
import re
import nltk

debug = 0
def console_debug(var):
    if (debug):
        print var

class Data_Processor:
    sno = nltk.stem.SnowballStemmer('english')
    label = None
    total_labeled_examples = None
    no_of_training_examples = None
    feature_set = None

    def read_data_from_excel(self, file):
        data = pd.read_excel(file)
        text = list(data.iloc[:, 0])
        self.label = list(data.iloc[:, 1])
        self.label = [l.strip() for l in self.label]
        assert len(text) == len(self.label)
        print 'Number of Labelled examples: ' + str(len(text))
        self.no_of_training_examples = int(len(text) * 0.7);
        return text

        # lower -> remove @user_name, #words, remove special characters[.,?, !, ", ', :, #, (, ) ]
        # remove stop words, replace url, replace number, to lower, apply stemming

    def pre_process(self, text):
        for i in range(len(text)):
            text[i] = text[i].replace("-", " ")
            word_list = text[i].encode('ascii', 'ignore').lower().split(" ")
            processed_text = []
            count = 0
            for word in word_list:
                if word in stopwords.words('english'):
                    continue
                if re.match('@\w+', word):
                    continue
                if re.match('#\w+', word):
                    continue
                word = re.sub('[0-9]+', 'gotNumber', word)
                word = re.sub('http(s)?.+', 'gotURL', word)
                word = re.sub('[^a-zA-Z0-9]', ' ', word)
                words = word.split(' ')
                for w in words:
                    if w is not ' ' and len(w) > 1 and w not in stopwords.words('english'):
                        w = self.sno.stem(w)
                        processed_text.append(w)
                    count += 1
                    print  '. ',
                    if count == 11:
                        print ''
                        count = 0
            text[i] = processed_text
        print ''
        return text

    def get_top_features(self, text, no_of_features):
        all_words_freq = FreqDist(word for line in text for word in line)
        # console_debug(all_words_freq.keys()[0:10])
        self.feature_set = all_words_freq.most_common(no_of_features)
        self.feature_set = [word[0] for word in self.feature_set]
        console_debug(self.feature_set)
