
import numpy as np;
import time
from sklearn import svm
from data_processor import Data_Processor
debug = 0
def console_debug(var):
    if (debug):
        print var

class SVM(Data_Processor):
    def create_feature_matrix(self, text):
        feature_matrix = np.zeros(shape = (len(text), len(self.feature_set)))
        count = 0
        for i in range(len(text)):
            for word in text[i]:
                if word in self.feature_set:
                    feature_matrix[i, self.feature_set.index(word)] = 1
                count += 1
                print '. ',
                if count == 11:
                    print ''
                    count = 0
        print ''
        return feature_matrix

    def create_label_matrix(self):
        label_matrix = np.zeros(self.no_of_training_examples)
        for i in range(self.no_of_training_examples):
            if self.label[i] == 'YES':
                label_matrix[i] = 1
        return label_matrix

    def create_svm_classifier(self, X, Y):
        clf = svm.SVC()
        clf.fit(X,Y)
        return clf

    def obtain_evaluation_matrix(self, result):
        test_samples = len(self.label) - self.no_of_training_examples
        label = np.array(self.label[self.no_of_training_examples: ])
        # print '********************Labels ************'
        # print label[10], label[70], label[90]
        positive_samples = (label == 'YES').sum()
        negative_samples = (label == 'NO').sum()
        assert positive_samples + negative_samples == test_samples
        assert len(result) == len(label)

        true_positive = np.logical_and (result == 1, label == 'YES' ).sum()
        false_positive = np.logical_and (result == 1 , label == 'NO').sum()
        false_negative = np.logical_and(result == 0, label == 'YES').sum()

        precision = float(true_positive) /(true_positive + false_positive)
        recall = float(true_positive) /(true_positive + false_negative)

        F1 = 2*precision*recall/(precision + recall)

        print '************************'
        print 'Precision: ', precision
        print 'Recall: ', recall
        print 'F1-Score: ', F1
        print '************************'

if __name__ == '__main__':
    svm_obj = SVM()
    print 'Reading Text from Excel file:'
    text = svm_obj.read_data_from_excel('labeled_data.xlsx')

    #below is sample for testing algorithm
    # test = text[2:5]
    # text = text[0:2]
    # svm_obj.no_of_training_examples = 2
    # svm_obj.label = svm_obj.label[0:5]

    test = text[svm_obj.no_of_training_examples : ]
    for i in range(len(text)):
        print text[i]
    print 'Text pre_processing: '
    time.sleep(1);
    text = svm_obj.pre_process(text)

    svm_obj.get_top_features(text, 100)
    print 'Generating feature matrix: '
    time.sleep(1)
    feature_matrix = svm_obj.create_feature_matrix(text[0: svm_obj.no_of_training_examples])
    console_debug(feature_matrix)

    print 'Generating Y matrix: '
    label_matrix = svm_obj.create_label_matrix()
    console_debug(label_matrix)
    assert np.shape(feature_matrix)[0] == np.shape(label_matrix)[0]

    print 'Training SVM model: '
    classifier = svm_obj.create_svm_classifier(feature_matrix, label_matrix)
    # print text[svm.no_of_training_examples])
    # print classifier.predict([text[svm.no_of_training_examples]]))
    # print classifier.predict([text[svm.no_of_training_examples + 1]]))
    print classifier.support_vectors_
    print classifier.support_

    print 'Predicting for test data:'
    print '*************Test samples *********************'
    for i in range(len(test)):
        print test[i]
    test = svm_obj.pre_process(test)
    test_features = svm_obj.create_feature_matrix(test)
    print ''

    result = classifier.predict(test_features)
    print 'Evaluating the Model: '
    svm_obj.obtain_evaluation_matrix(result)
    print len(test)