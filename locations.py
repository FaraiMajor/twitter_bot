import json
import sys
import geocoder
import config
import tweepy

# Twitter details
consumer_key = config.twitter_apikey
consumer_secret = config.twitter_apikey_secret
access_token = config.twitter_access_token
access_token_secret = config.twitter_access_token_secret

# authentication of consumer key and secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# authentication of access token and secret
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
'''
We want to use thos portion to find all the location trends for twitter. save this in a json
and now we have our woied number for each location
'''
available_loc = api.available_trends()
# writing a JSON file that has the available trends around the world
with open("available_locs_for_trend.json", "w") as wp:
    wp.write(json.dumps(available_loc, indent=1))

# Trends for Specific Country
loc = sys.argv[1]     # location as argument variable
# getting object that has location's latitude and longitude
g = geocoder.osm(loc)

closest_loc = api.closest_trends(g.lat, g.lng)
trends = api.get_place_trends(closest_loc[0]['woeid'])
# writing a JSON file that has the latest trends for that location
with open("twitter_{}_trend.json".format(loc), "w") as wp:
    wp.write(json.dumps(trends, indent=1))

'''
--------------------location finder ends here-------------------
'''
