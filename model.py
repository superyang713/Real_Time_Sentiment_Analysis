import nltk

import csv
import pickle

from nlp import PreProcessTweets


def build_volcabulary(processed_train):
    all_words = []

    for (words, sentiment) in processed_train:
        all_words.extend(words)

    word_list = nltk.FreqDist(all_words)
    word_features = word_list.keys()

    return word_features


def extract_features(tweet):
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in tweet)
    return features


with open("./data/training.csv") as f:
    train = csv.DictReader(f)
    tweet_processor = PreProcessTweets()
    processed_train = tweet_processor.process_tweets(train)

# Now we can extract the features and train the classifier
word_features = build_volcabulary(processed_train)


# training_features = nltk.classify.apply_features(
#     extract_features,
#     processed_train
# )

# NBayesClassifier = nltk.NaiveBayesClassifier.train(training_features)
# print("Classifier accuracy percent:",(nltk.classify.accuracy(NBayesClassifier, training_features))*100)

# f = open('./data/classifier.pickle', 'rb')
# classifier = pickle.load(f)
# f.close()

# NBResultLabels = [
#     classifier.classify(extract_features(tweet[0]))
#     for tweet in processed_train[-100:]
# ]

# print(NBResultLabels)

