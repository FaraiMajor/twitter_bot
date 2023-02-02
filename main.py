import openai
import random
import config
import tweepy
import pandas
import geocoder
import schedule

# Twitter details
consumer_key = config.twitter_apikey
consumer_secret = config.twitter_apikey_secret
access_token = config.twitter_access_token
access_token_secret = config.twitter_access_token_secret

# OPENAI keys
openai.organization = config.openai_org
openai.api_key = config.openai_apikey
openai.Model.list()


def job():

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

    def generate_tweet(trending):
        # create a completion
        prompt = 'write a tweet about ' + random.choice(hashtags)
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
    try:
        api.verify_credentials()
        print("Authentication Successful")
        generate_tweet(trending)
        like_and_retweet()
    except:
        print("Authentication Error")

    # scraps trending topics from twitter using tweepy
    dataset = {
        "hashtags": trending
    }

    df = pandas.DataFrame(dataset)
    df.to_csv('tweets.csv')


# run the function job() every 1 hr seconds
schedule.every(60).seconds.do(job)

while True:
    schedule.run_pending()
