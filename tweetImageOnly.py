import tweepy
import configparser
import os

#def publish_tweet():
dirname = os.path.dirname(__file__)

# open config file
config_init_filename = os.path.join(dirname, 'config.ini')
config_parser = configparser.ConfigParser()
config_parser.readfp(open(config_init_filename))
# read tweeter credentials
consumer_key = config_parser['tweeter']['consumer_key']
consumer_secret = config_parser['tweeter']['consumer_secret']
access_token = config_parser['tweeter']['access_token']
access_token_secret = config_parser['tweeter']['access_token_secret']
bearer_token = config_parser['tweeter']['bearer_token']

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    
# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)
    
# calling the api
api = tweepy.API(auth)
client = tweepy.Client(bearer_token=bearer_token,
                        access_token=access_token,
                        access_token_secret=access_token_secret,
                        consumer_key=consumer_key,
                        consumer_secret=consumer_secret)
    
# the name of the media file
graph_filename = os.path.join(dirname, 'newplot.png')
    
# upload the file
media = api.media_upload(graph_filename)
    
# printing the information
print("The media ID is : " + media.media_id_string)
print("The size of the file is : " + str(media.size) + " bytes")
client.create_tweet(media_ids= [media.media_id_string])