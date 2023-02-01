import openai
import random
import config
import tweepy
import pandas
import json
import sys
import geocoder

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
def extract_hashtags(trends):
    hashtags = [trend["name"] for trend in trends]
    return hashtags


hashtags = extract_hashtags(trends)


# create a completion
prompt = 'write a tweet about ' + random.choice(hashtags)

completion = openai.Completion.create(
    model='text-davinci-003', prompt=prompt, max_tokens=186)

# print the completion
# print(completion.choices[0].text)

try:
    api.verify_credentials()
    print("Authentication Successful")
    api.update_status(completion.choices[0].text)
except:
    print("Authentication Error")

# scraps trending topics from twitter using tweepy
dataset = {
    "hashtags": hashtags
}

df = pandas.DataFrame(dataset)
df.to_csv('tweets.csv')
'''
We want to use thos portion to find all the location trends for twitter. save this in a json
and now we have our woied number for each location
'''
# available_loc = api.available_trends()
# # writing a JSON file that has the available trends around the world
# with open("available_locs_for_trend.json", "w") as wp:
#     wp.write(json.dumps(available_loc, indent=1))

#     # Trends for Specific Country
# loc = sys.argv[1]     # location as argument variable
# # getting object that has location's latitude and longitude
# g = geocoder.osm(loc)

# closest_loc = api.closest_trends(g.lat, g.lng)
# trends = api.get_place_trends(closest_loc[0]['woeid'])
# # writing a JSON file that has the latest trends for that location
# with open("twitter_{}_trend.json".format(loc), "w") as wp:
#     wp.write(json.dumps(trends, indent=1))

'''
--------------------location finder ends here-------------------
'''
