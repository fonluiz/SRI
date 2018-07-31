import tweepy
import csv
import pandas as pd
# input your credentials here
consumer_key = 'W5zdtI3tT6UcdAEv7zYcLQDbk'
consumer_secret = 'NhiQckcYGOy7e5Ku9Fsxa0B5hNrZ50Y2IOOEnEV6xNakv40SdG'
access_token = '79004037-HhptDKcQoSYrkhe2OOj2KTYn9TNcnYbBqYILQjp5Q'
access_token_secret = 'E5PDvg4PT5aiPmNR8RSiA9cDW95ApnH6FVAkjZu82vOSG'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
# United Airlines
# Open/Create a file to append data
csvFile = open('test.csv', 'a')
# Use csv Writer
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search, q="neymar AND copa", count=100,
                           lang="pt",
                           since="2018-07-30").items():
    print(tweet.created_at, tweet.text)
    encoded_tweet = tweet.text.encode('utf-8')
    decoded_tweet = encoded_tweet.decode("utf-8")
    csvWriter.writerow(
        [tweet.created_at, decoded_tweet])
