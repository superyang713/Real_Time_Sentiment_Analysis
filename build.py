tweetProcessor = PreProcessTweets()
preprocessedTrainingSet = tweetProcessor.processTweets(trainingData)
preprocessedTestSet = tweetProcessor.processTweets(testDataSet)


def buildVocabulary(preprocessedTrainingData):
    all_words = []

    for (words, sentiment) in preprocessedTrainingData:
        all_words.extend(words)

    wordlist = nltk.FreqDist(all_words)
    word_features = wordlist.keys()

    return word_features


# ------------------------------------------------------------------------


def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in tweet_words)
    return features


# ------------------------------------------------------------------------

# Now we can extract the features and train the classifier
word_features = buildVocabulary(preprocessedTrainingSet)
trainingFeatures = nltk.classify.apply_features(extract_features,
                                                preprocessedTrainingSet)

# ------------------------------------------------------------------------

NBayesClassifier = nltk.NaiveBayesClassifier.train(trainingFeatures)

# ------------------------------------------------------------------------

NBResultLabels = [
    NBayesClassifier.classify(extract_features(tweet[0]))
    for tweet in preprocessedTestSet
]
