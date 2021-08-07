import enum
from io import StringIO
import nltk
from nltk.stem.lancaster import LancasterStemmer

import numpy as np
import os
import json
import datetime
import time

stemmer = LancasterStemmer()

class NeuralNetwork():
    def __init__(self) -> None:
        self.synapse_file = "synapses.json"

        with open('intents.json') as json_data:
            self.training_data = json.load(json_data)

        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_words = ['?', '\'', '!', '.', ',', 'to', 'a', 'the']

        for intent in self.training_data['intents']:
            for pattern in intent['patterns']:
                w = nltk.word_tokenize(pattern)

                self.words.extend(w)
                self.documents.append((w, intent['tag']))

                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        self.words = [stemmer.stem(w.lower()) for w in self.words if w not in self.ignore_words]
        self.words = sorted(list(set(self.words)))

        self.classes = sorted(list(set(self.classes)))

        print (len(self.documents), "documents", self.documents)
        print (len(self.classes), "classes", self.classes)
        print (len(self.words), "unique stemmed words", self.words)

        training = []
        output = []

        output_empty = [0] * len(self.classes)

        for doc in self.documents:
            bag = []
            pattern_words = doc[0]
            pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)
            
            training.append(bag)
            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            output.append(output_row)

        X = np.array(training)
        y = np.array(output)

        start_time = time.time()

        overwrite = False

        if not overwrite:
            with open(self.synapse_file) as data_file: 
                self.synapse = json.load(data_file) 
                self.synapse_0 = np.asarray(self.synapse['synapse0']) 
                self.synapse_1 = np.asarray(self.synapse['synapse1'])

        self.train(X, y, hidden_neurons=20, alpha=0.1, epochs=100000, dropout=False, dropout_percent=0.2, overwrite=overwrite)

        if overwrite:
            elapsed_time = time.time() - start_time
            print("processing time:", elapsed_time, "seconds")
            with open(self.synapse_file) as data_file: 
                self.synapse = json.load(data_file) 
                self.synapse_0 = np.asarray(self.synapse['synapse0']) 
                self.synapse_1 = np.asarray(self.synapse['synapse1'])

    @staticmethod
    def sigmoid(x):
        output = 1 / (1 + np.exp(-x))
        return output

    @staticmethod
    def sigmoid_output_to_derivative(output):
        return output * (1 - output)

    @staticmethod
    def clean_up_sentence(sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
        return sentence_words

    def bow(self, sentence, words, show_details=False):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(words)
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("Found in bag: %s" % w)

        return(np.array(bag))

    def think(self, sentence, show_details=False):
        x = self.bow(sentence.lower(), self.words, show_details)
        if show_details:
            print("sentence: ", sentence, "\n bow", x)
        l0 = x
        l1 = self.sigmoid(np.dot(l0, self.synapse_0))
        l2 = self.sigmoid(np.dot(l1, self.synapse_1))
        return l2

    def train(self, X, y, hidden_neurons=10, alpha=1, epochs=50000, dropout=False, dropout_percent=0.5, overwrite=False):
        if not overwrite:
            return
        print("Training with %s neurons, alpha: %s, dropout: %s %s" % (str(hidden_neurons), str(alpha), str(dropout), str(dropout_percent) if dropout else ''))
        print("Input matrix: %sx%s\nOutput matrix: %sx%s" % (len(X), len(X[0]), 1, len(self.classes)))
        np.random.seed(1)

        last_mean_error = 1

        self.synapse_0 = 2 * np.random.random((len(X[0]), hidden_neurons)) - 1
        self.synapse_1 = 2 * np.random.random((hidden_neurons, len(self.classes))) - 1

        prev_synapse_0_weight_update = np.zeros_like(self.synapse_0)
        prev_synapse_1_weight_update = np.zeros_like(self.synapse_1)

        synapse_0_direction_count = np.zeros_like(self.synapse_0)
        synapse_1_direction_count = np.zeros_like(self.synapse_1)

        for j in iter(range(epochs+1)):
            layer_0 = X
            layer_1 = self.sigmoid(np.dot(layer_0, self.synapse_0))
            
            if(dropout):
                layer_1 *= np.random.binomial([np.ones((len(X), hidden_neurons))], 1 - dropout_percent)[0] * (1.0 / (1 - dropout_percent))

            layer_2 = self.sigmoid(np.dot(layer_1, self.synapse_1))

            layer_2_error = y - layer_2

            if (j % 10000) == 0 and j > 5000:
                if np.mean(np.abs(layer_2_error)) < last_mean_error:
                    print("delta after " + str(j) + " iterations: " + str(np.mean(np.abs(layer_2_error))))
                    last_mean_error = np.mean(np.abs(layer_2_error))
                else:
                    print("break: ", np.mean(np.abs(layer_2_error)), ">", last_mean_error)
                    break

            layer_2_delta = layer_2_error * self.sigmoid_output_to_derivative(layer_2)
            layer_1_error = layer_2_delta.dot(self.synapse_1.T)
            layer_1_delta = layer_1_error * self.sigmoid_output_to_derivative(layer_1)

            synapse_1_weight_update = (layer_1.T.dot(layer_2_delta))
            synapse_0_weight_update = (layer_0.T.dot(layer_1_delta))

            if(j > 0):
                synapse_0_direction_count += np.abs(((synapse_0_weight_update > 0) + 0) - ((prev_synapse_0_weight_update > 0) + 0))
                synapse_1_direction_count += np.abs(((synapse_1_weight_update > 0) + 0) - ((prev_synapse_1_weight_update > 0) + 0))
            
            self.synapse_1 += alpha * synapse_1_weight_update
            self.synapse_0 += alpha * synapse_0_weight_update

            prev_synapse_0_weight_update = synapse_0_weight_update
            prev_synapse_1_weight_update = synapse_1_weight_update

        now = datetime.datetime.now()

        self.synapse = {'synapse0': self.synapse_0.tolist(), 'synapse1': self.synapse_1.tolist(),
                'datetime': now.strftime("%Y-%m-%d $H:$M"),
                'words': self.words,
                'classes': self.classes
                }

        with open(self.synapse_file, 'w') as outfile:
            json.dump(self.synapse, outfile, indent=4, sort_keys=True)
        print("saved synapses to:", self.synapse_file)

    def classify(self, sentence, show_details=False):
        ERROR_THRESHOLD = 0.2
        results = self.think(sentence, show_details)

        results = [[i,r] for i,r in enumerate(results) if r > ERROR_THRESHOLD] 
        results.sort(key = lambda x: x[1], reverse=True) 
        return_results =[[self.classes [r[0]], r[1]] for r in results]
        # print ("classification: %s" % return_results)
        return return_results