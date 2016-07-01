import time
from data_processor import Data_Processor
import nltk

class NBClassifier(Data_Processor):
    # defining feature extractor
    def document_features(self, document):
        document_words = set(document)
        document_features = {}
        for word in self.feature_set:
            document_features['contains({})'.format(word)] = (word in document_words)
        return document_features

    def create_features(self, text):
        features = [ (self.document_features(text[i]), self.label[i]) for i in range(len(text)) ]
        return features

    def get_NB_classifier(self, train_set):
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        print 'classifier', classifier.labels()
        return classifier

    def evaluate_model(self, classifier, test_set):
        true_positive = 0
        false_positive = 0
        false_negative = 0
        for (document, label) in test_set:
            guess = classifier.classify(document)
            print guess
            if guess == 'YES' and  label == 'YES':
                true_positive += 1
            if guess == 'YES' and label == 'NO':
                false_positive += 1
            if guess == 'NO' and label == 'YES':
                false_negative += 1
        precision = float(true_positive) / (true_positive + false_positive)
        recall =  float(true_positive)/ (true_positive + false_negative)
        F1 = 2 * precision * recall / (precision + recall)

        accuracy = nltk.classify.accuracy(classifier, test_set)

        print classifier.show_most_informative_features(10)

        print '********** Model Evaluation*******'
        print 'Naive Bayes classifier accuracy: ', accuracy
        print "Precision: ", precision
        print "Recall:  ", recall
        print "F1-Score: ", F1
        print '**********************************'
if __name__ == '__main__':
    nb_obj = NBClassifier()
    print 'Reading Text from Excel file:'
    text = nb_obj.read_data_from_excel('labeled_data.xlsx')
    print 'Text pre_processing: '
    time.sleep(1);
    text = nb_obj.pre_process(text)
    nb_obj.get_top_features(text, 1000)

    print 'Generating features for NB algorithm: '
    time.sleep(1)
    all_text_features = nb_obj.create_features(text)
    train_set, test_set = all_text_features[0:nb_obj.no_of_training_examples], all_text_features[nb_obj.no_of_training_examples:]

    classifier = nb_obj.get_NB_classifier(train_set)

    nb_obj.evaluate_model(classifier, test_set)
