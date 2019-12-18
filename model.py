import csv
import time

import tweepy

from utils import connect_api


def build_test_set(search_keyword):
    api = connect_api()
    try:
        tweets_fetched = api.search(search_keyword, count=100)
        print("Fetched " + str(len(tweets_fetched)) + " tweets for the term " +
              search_keyword)
        return [{
            "text": status.text,
            "label": None
        } for status in tweets_fetched]
    except:
        print("Unfortunately, something went wrong..")
        return None


# search_term = input("Enter a search keyword:")
# test_set = build_test_set(search_term)

# print(test_set[0:4])


def build_training_set(corpse_file, tweet_file):
    api = connect_api()
    corpus = []
    with open(corpus_file, 'r') as csvfile:
        lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        for row in lineReader:
            corpus.append({
                "tweet_id": row[2],
                "label": row[1],
                "topic": row[0]
            })

    rate_limit = 180
    sleep_time = 5

    training_set = []
    for tweet in corpus:
        try:
            status = api.get_status(tweet["tweet_id"])
            print("Tweet fetched" + status.text)
            tweet["text"] = status.text
            training_set.append(tweet)
            time.sleep(sleep_time)
        except:
            continue

    with open(tweet_file, 'w') as csvfile:
        linewriter = csv.writer(csvfile, delimiter=',', quotechar="\"")
        for tweet in training_set:
            try:
                linewriter.writerow([
                    tweet["tweet_id"],
                    tweet["text"],
                    tweet["label"],
                    tweet["topic"]
                ])
            except Exception as e:
                print(e)
    return training_set

corpus_file = "data/corpus.csv"
tweet_file = "data/training.csv"

training_set = build_training_set(corpus_file, tweet_file)
