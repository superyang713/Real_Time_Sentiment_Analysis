"""
Contains various functions to process texts, mainly tweets.
"""

import string
import re
import flair

from utils import extract_data
import settings

flair_sentiment = flair.models.TextClassifier.load('en-sentiment')

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

def analyze_sentiment(text):
    sentence = flair.data.Sentence(text)
    flair_sentiment.predict(sentence)
    total_sentiment = sentence.labels
    return total_sentiment


df = extract_data(settings.table_name)

df["text_punct_removed"] = df["text"].apply(clean_text)
df["sentiment"] = df["text_punct_removed"].apply(analyze_sentiment)

print(df.head())
print(df["sentiment"].iloc[2])
