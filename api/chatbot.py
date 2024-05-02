"""
Chatbot AI helper

Preprocess question string, classify according to a given model and
return the answer according to the intents file.

Author: Igor Souza
"""
import json
import random
import pickle
from os import path
from typing import Any, Dict, List

import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from tensorflow.keras.models import load_model # type: ignore


# Download of nltk base
nltk.download('wordnet')


class ChatbotException(Exception):
    """Exception raise when error on Chatbot."""


class Chatbot:

    _lemmatizer = WordNetLemmatizer()
    _tokenizer = RegexpTokenizer(r'\w+')

    def __init__(self, base_path: str = '.'):
        self.model = self._load_model(path.join(base_path, 'chatbot_model.h5'))
        self.intents = self._load_intents(path.join(base_path, 'intents.json'))
        self.words = self._load_pickles(path.join(base_path, 'words.pkl'))
        self.classes = self._load_pickles(path.join(base_path, 'classes.pkl'))

    def _load_model(self, path: str):
        """Load the tensorflow model. It expects a .h5 file."""
        try:
            return load_model(path)
        except (ImportError, IOError) as e:
            raise ChatbotException("Model not found. %s" % e)

    def _load_intents(self, path: str) -> Dict[str, dict]:
        """Load the intents.json which model were trained into."""
        try:
            with open(path, 'rb') as file:
                return json.load(file)
        except Exception as e:
            raise ChatbotException("Intents file not loaded. %s" % e)

    def _load_pickles(self, path: str) -> Any:
        """Helper function to load pickled file."""
        try:
            with open(path, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            raise ChatbotException("Pickle file not loaded. %s" % e)

    def _clean_up_sentence(self, sentence: str) -> List[str]:
        """Tranform a string like sentence in a list of lemmatize words."""
        sentence_words = self._tokenizer.tokenize(sentence)
        sentence_words = [
            self._lemmatizer.lemmatize(word.lower()) for word in sentence_words
        ]

        return sentence_words

    def _bow(self, sentence: str) -> np.ndarray:
        """
        Get the bag of words for the given sentence. It just set 1 on the
        dictionary list if that words belongs to the sentence.
        """
        sentence_words = self._clean_up_sentence(sentence)

        # Start the bag with a n-long vector. Each space is a word on the
        # dictionary
        bag = [1 if sentence_words.count(w) >= 1 else 0 for w in self.words]

        return np.array(bag)

    async def _predict_class(self,
                             sentence: str,
                             ERROR_THRESHOLD: float) -> List[Dict[str, Any]]:
        """Get the list of classes and its probability of setence belonging."""
        p = self._bow(sentence)

        # Make sure model was sucessf
        try:
            assert self.model is not None, "Model wasn't loaded!"
        except AssertionError as e:
            raise ChatbotException(e)

        # Get the list of probabilities for each class
        res = self.model.predict(np.array([p]))[0]

        # Get the classes filtering by the threshold
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)

        # Build the list of the intent classes found above the given threshold
        intent_classes = [
            {
                "intent": self.classes[r[0]],
                "probability": str(r[1])
            } for r in results
        ]

        return intent_classes

    def _getResponse(self, clss: str) -> str:
        """
        Search on the list of intents the answers for that class. It should
        return a random result.
        """
        resp: List[str] = list()

        for intent in self.intents['intents']:
            if intent['tag'] == clss:
                resp = intent['responses']

        return random.choice(resp)

    async def get_response(self, msg: str, threshold: float = 0.25) -> str:
        """
        Given a question, return the most probable answer.

        A optional parameters may be set, the threshold, it will cut the answer
        if the probability is lower then itself.
        """
        ints = await self._predict_class(msg, threshold)

        try:
            res = self._getResponse(ints[0]['intent'])
        except ValueError:
            return "I'm sorry, didn't undestand your question!"

        return res
