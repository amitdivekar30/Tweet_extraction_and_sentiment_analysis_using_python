#Tweets extraction and Sentiment Analysis


import tweepy #https://github.com/tweepy/tweepy

#Twitter API credentials
consumer_key = "consumer key"
consumer_secret = "consumer secret"
access_key = "access key"
access_secret = "access secret token"


def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    alltweets = []	
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    
    oldest = alltweets[-1].id - 1
    while len(new_tweets)>0:
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        #save most recent tweets
        alltweets.extend(new_tweets)
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        print ("...%s tweets downloaded so far" % (len(alltweets)))                # tweet.get('user', {}).get('location', {})
 
    outtweets = [[tweet.created_at,tweet.entities["hashtags"],tweet.entities["user_mentions"],tweet.favorite_count,
                  tweet.geo,tweet.id_str,tweet.lang,tweet.place,tweet.retweet_count,tweet.retweeted,tweet.source,tweet.text,
                  tweet._json["user"]["location"],tweet._json["user"]["name"],tweet._json["user"]["time_zone"],
                  tweet._json["user"]["utc_offset"]] for tweet in alltweets]
    
    import pandas as pd
    tweets_df = pd.DataFrame(columns = ["time","hashtags","user_mentions","favorite_count",
                                    "geo","id_str","lang","place","retweet_count","retweeted","source",
                                    "text","location","name","time_zone","utc_offset"])
    tweets_df["time"]  = pd.Series([str(i[0]) for i in outtweets])
    tweets_df["hashtags"] = pd.Series([str(i[1]) for i in outtweets])
    tweets_df["user_mentions"] = pd.Series([str(i[2]) for i in outtweets])
    tweets_df["favorite_count"] = pd.Series([str(i[3]) for i in outtweets])
    tweets_df["geo"] = pd.Series([str(i[4]) for i in outtweets])
    tweets_df["id_str"] = pd.Series([str(i[5]) for i in outtweets])
    tweets_df["lang"] = pd.Series([str(i[6]) for i in outtweets])
    tweets_df["place"] = pd.Series([str(i[7]) for i in outtweets])
    tweets_df["retweet_count"] = pd.Series([str(i[8]) for i in outtweets])
    tweets_df["retweeted"] = pd.Series([str(i[9]) for i in outtweets])
    tweets_df["source"] = pd.Series([str(i[10]) for i in outtweets])
    tweets_df["text"] = pd.Series([str(i[11]) for i in outtweets])
    tweets_df["location"] = pd.Series([str(i[12]) for i in outtweets])
    tweets_df["name"] = pd.Series([str(i[13]) for i in outtweets])
    tweets_df["time_zone"] = pd.Series([str(i[14]) for i in outtweets])
    tweets_df["utc_offset"] = pd.Series([str(i[15]) for i in outtweets])
    tweets_df.to_csv(screen_name+"_tweets.csv")
    return tweets_df

bo_tweets = get_all_tweets("BarackObama")
bo_tweets.to_csv("twitter_bo.csv",encoding="utf-8")
bo_tweets['text'].to_csv("twitter_bo.txt",encoding="utf-8")
#cadd_centre_tweets = get_all_tweets("DreamZoneSchool")

import nltk
import re
# Sentiment Analysis
# Joinining all the reviews into single paragraph 
tweet_rev_string = " ".join(bo_tweets['text'])



# Removing unwanted symbols incase if exists
tweet_rev_string = re.sub("[^A-Za-z" "]+"," ",tweet_rev_string).lower()
tweet_rev_string = re.sub("[0-9" "]+"," ",tweet_rev_string)



# words that contained in tweet 7 reviews
tweet_reviews_words = tweet_rev_string.split(" ")

from nltk.corpus import stopwords
stop_words = stopwords.words('english')

with open("stop.txt","r") as sw:
    stopwords = sw.read()

stopwords = stopwords.split("\n")
stopwords=stopwords + ['https']

tweet_reviews_words = [w for w in tweet_reviews_words if not w in stopwords]


# Joinining all the reviews into single paragraph 
tweet_rev_string = " ".join(tweet_reviews_words)

# WordCloud can be performed on the string inputs. That is the reason we have combined 
# entire reviews into single paragraph
# Simple word cloud
import matplotlib.pyplot as plt
from wordcloud import WordCloud

wordcloud_tweet = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(tweet_rev_string)

plt.imshow(wordcloud_tweet)

# positive words # Choose the path for +ve words stored in system
with open("positive-words.txt","r") as pos:
  poswords = pos.read().split("\n")
  
poswords = poswords[36:]



# negative words  Choose path for -ve words stored in system
with open("negative-words.txt","r") as neg:
  negwords = neg.read().split("\n")

negwords = negwords[37:]

# negative word cloud
# Choosing the only words which are present in negwords
tweet_neg_in_neg = " ".join ([w for w in tweet_reviews_words if w in negwords])

wordcloud_neg_in_neg = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(tweet_neg_in_neg)

plt.imshow(wordcloud_neg_in_neg)

# Positive word cloud
# Choosing the only words which are present in positive words
tweet_pos_in_pos = " ".join ([w for w in tweet_reviews_words if w in poswords])
wordcloud_pos_in_pos = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(tweet_pos_in_pos)

plt.imshow(wordcloud_pos_in_pos)
 

# Unique words 
tweet_unique_words = list(set(" ".join(tweet_reviews_words).split(" ")))
		


