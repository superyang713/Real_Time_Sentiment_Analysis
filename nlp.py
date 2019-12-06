"""
Contains various functions to process texts, mainly tweets.
"""

import string
import re
import pandas as pd
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from utils import extract_data
import settings

nltk.download("stopwords")
nltk.download("punkt")


def clean_text(text):
    # remove hyperlink
    text = re.sub(r"(?:https?\://)\S+", "", text)

    # remove special character
    text = "".join([char for char in text if char not in string.punctuation])

    # remove numbers
    text = re.sub(r"[0-9]+", "", text)

    # remove non-ascii characters, mainly different languages and emojis.
    text = text.encode('ascii', 'ignore').decode()

    return text

def remove_stopwords(text):
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = " ".join(filtered_sentence)
    return filtered_sentence

def preprocess_text(text):
    text = clean_text(text)
    text = remove_stopwords(text)
    return text

def analyze_sentiment(text):
    text = TextBlob(text)
    polarity = text.sentiment.polarity
    subjectivity = text.sentiment.subjectivity
    return polarity, subjectivity
