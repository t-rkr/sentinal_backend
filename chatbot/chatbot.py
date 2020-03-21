import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import flask
import io
import json
import random
import os
from keras.models import load_model
import tensorflow as tf

class Chatbot:

    def __init__(self,app):
        #File Reading
        intents_filename = os.path.join(app.root_path, 'chatbot\\data', 'intents.json')
        words_filename = os.path.join(app.root_path, 'chatbot\\data', 'words.pkl')
        classes_filename = os.path.join(app.root_path, 'chatbot\\data', 'classes.pkl')
        model_filename = os.path.join(app.root_path, 'chatbot\\data', 'chatbot_model.h5')

        self.intents = json.loads(open(intents_filename).read())
        self.words = pickle.load(open(words_filename, 'rb'))
        self.classes = pickle.load(open(classes_filename, 'rb'))
        self.model = load_model(model_filename)
        self.lemmatizer = WordNetLemmatizer()
        self.session = tf.Session()
        self.graph = tf.get_default_graph()
        with self.graph.as_default():
            with self.session.as_default():
                print("Model Loaded!")

    def clean_up_sentence(self,sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words


    def bow(self, sentence, words, show_details=True):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0] * len(words)
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)
        return (np.array(bag))

    def predict_class(self, sentence, modelChatbot):
        # filter out predictions below a threshold
        p = self.bow(sentence, self.words, show_details=False)
        #keras.backend.clear_session()
        res = None
        with self.graph.as_default():
            res = modelChatbot.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})
        return return_list


    def getResponse(self, ints):
        tag = ints[0]['intent']
        list_of_intents = self.intents['intents']
        for i in list_of_intents:
            if (i['tag'] == tag):
                result = random.choice(i['responses'])
                break
        return result
