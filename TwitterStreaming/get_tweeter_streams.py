import  json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream



# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="xxxxxxx"
consumer_secret="xxxxxxx"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="yyy-yyy"
access_token_secret="zzzzz"


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is tweets_counta basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        print(data.rstrip())
        return True

    def on_exception(self, exception):
        print(exception)
        return

    def on_error(self, status):
        print(status)

    def on_status(self, status):
        return

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
   # msg = raw_input('Enter search string? ')
    #query=("[\'"+msg+"\']")
    #print(query)
    stream.filter(track=['election','votede','bhajpa','loksabha','rss','votekar','shivsena','bjp','chowkidar','janata','indiancongress','janasena','aap','mulayam','tdp', 'bjd', 'bsp','samajwadi','mns','dmk','aiadmk','pdp','cpi','gatbandhan','tmc','trinamool'], stall_warnings=True)


