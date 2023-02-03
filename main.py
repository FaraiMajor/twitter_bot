import openai
import random
import config
import tweepy
import pandas
import geocoder
import time


FILE_NAME = 'last_seen.txt'
# Twitter details
consumer_key = config.twitter_apikey
consumer_secret = config.twitter_apikey_secret
access_token = config.twitter_access_token
access_token_secret = config.twitter_access_token_secret

# OPENAI keys
openai.organization = config.openai_org
openai.api_key = config.openai_apikey
openai.Model.list()

# authentication of consumer key and secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# authentication of access token and secret
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# get the trending topics for a specific WOEID


def get_trends(api, loc):
    # Object that has location's latitude and longitude.
    g = geocoder.osm(loc)

    closest_loc = api.closest_trends(g.lat, g.lng)
    trends = api.get_place_trends(closest_loc[0]["woeid"])
    return trends[0]["trends"]


loc = "United States"
trends = get_trends(api, loc)
# print(json.dumps(trends, indent=1))

# extract our hashtags


def extract_trending_topics(trends):
    hashtags = [trend["name"] for trend in trends]
    return hashtags


trending = extract_trending_topics(trends)

# scraps trending topics from twitter using tweepy
dataset = {
    "hashtags": trending
}

df = pandas.DataFrame(dataset)
df.to_csv('tweets.csv')


# GENERATE TWEETS USING openAI
def generate_tweet(trending):
    # create a completion
    prompt = 'write a tweet about ' + random.choice(trending)
    completion = openai.Completion.create(
        model='text-davinci-003', prompt=prompt, max_tokens=186)

    api.update_status(completion.choices[0].text)

# Auto like and retweet function


def like_and_retweet():
    usernames = ['Cobratate', 'larryelder',
                 'elonmusk', 'KSI', 'jordanbpeterson']
    # Loop through each user in the list
    for username in usernames:
        # Get the latest tweets from the user
        public_tweets = api.user_timeline(screen_name=username, count=10)
        for tweet in public_tweets:
            # get status and check if tweet has been liked already
            status = api.get_status(tweet.id)
            liked = status.favorited
            if not liked:
                api.create_favorite(tweet.id)
                api.retweet(tweet.id)
            else:
                continue


'''
store and write to a file the last id of our mentioned tweet and avoid repetition
This part will reply to our mentions starting search from where we previously
left off
'''


def read_last_seen(FILE_NAME):
    with open(FILE_NAME, 'r') as read_file:
        last_seen_id = int(read_file.read().strip())
        read_file.close()
    return last_seen_id


def store_last_seen(FILE_NAME, last_seen_id):
    with open(FILE_NAME, 'w') as write_file:
        write_file.write(str(last_seen_id))
        write_file.close()
    return

# function to reply to tweets we are mentioned in


def reply_to_mentions():
    tweets = api.mentions_timeline(
        since_id=read_last_seen(FILE_NAME), tweet_mode='extended')
    # reversed tweets because bot read the most recent tweet down but we want the most recent last to get ID
    for tweet in reversed(tweets):
        print(str(tweet.id) + '  - ' + tweet.full_text)
        prompt = "reply to this tweet with strictly 240 characters or less only: " + tweet.full_text
        completion = openai.Completion.create(
            model='text-davinci-003', prompt=prompt, max_tokens=160)
        # Reply to the mention
        reply = '@' + tweet.user.screen_name + completion.choices[0].text
        api.update_status(status=reply, in_reply_to_status_id=tweet.id)
        store_last_seen(FILE_NAME, tweet.id)


def create_engagement():

    for _ in range(10):
        # Choose a random hashtag from the list of hashtags
        hashtag = random.choice(trending)
        # Search for tweets containing the hashtag with a count of 100
        tweets = api.search_tweets(q=hashtag, count=25)
        tweet = random.choice(list(tweets))
        # Follow the user who posted the tweet
        api.create_friendship(user_id=tweet.user.id)
        # Like the tweet
        api.create_favorite(tweet.id)
        # Retweet the tweet
        api.retweet(tweet.id)


try:
    api.verify_credentials()
    print("Authentication Successful")
except:
    print("Authentication Error")


while True:
    reply_to_mentions()
    create_engagement()
    like_and_retweet()
    generate_tweet(trending)
    print('tweet done')
    time.sleep(900)
