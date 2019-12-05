"""
Contains various functions to process texts, mainly tweets.
"""

import string
import re
import flair

from utils import extract_data
import settings


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


df = extract_data(settings.table_name)

df["text_punct_removed"] = df["text"].apply(remove_punctuation)
flair_sentiment = flair.models.TextClassifier.load('en-sentiment')
s = flair.data.Sentence(sentence)
flair_sentiment.predict(s)
total_sentiment = s.labels
total_sentiment
