import re


def electionMap(tweet):
    parties_list = list()
    if tweet: 
        tweet = tweet.lower()
        if re.search(r"bjp|modi|namo|chowkidaar", tweet):
            parties_list.insert(0,("BJP",1))
        if re.search(r"raga|gandhi|inc|sonia", tweet):
            parties_list.insert(0,("INC",1))
        if re.search(r"aap|kejri|arvind", tweet):
            parties_list.insert(0,("AAP",1)) 
        if re.search(r"mamta|cpi|kanhaiya|bsp|samajwadi|tmc", tweet):
            parties_list.insert(0,("Others",1))
    return parties_list

# Uses GCP Sentiment Analysis (archived)

from google.cloud import language
import os

home = os.environ['HOME']
path = home + "/nlp.json" #FULL path to your service account key
client = language.LanguageServiceClient.from_service_account_json(path)
    
def sentiment_category(sentiment):
    score = sentiment[0]
    magnitude = sentiment[1]
    if score == 0.0:
        category = "neutral"
    elif score > 0.0:
        category = "positive"
    elif score < 0.0:
        category = "negative"
        
    return category

def gc_sentiment(text): 
   
    document = language.types.Document(
            content=text,
            type=language.enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude
    return score, magnitude

def findSentimentForStream(records) :
    topic_name = "gcp_sentiments"
    sentimap = {"positive":0, "negative":0, "neutral": 0, "unprocessed": 0}
    unprocessed_count = 0
    for record in records:
        try:
            sentiment = gc_sentiment(str(record))
            category = sentiment_category(sentiment)
            previous_count = sentimap[category]
            sentimap[category] = previous_count+1
        except Exception as ex:
            unprocessed_count += 1
    sentimap['unprocessed'] = unprocessed_count
    output = json.dumps(sentimap) 
    print(output)
    if len(records) > 0:
        #publishToKafka(topic_name, output)
        pass
    
# (not in use)
def filterOnLang(tweet):
    try:
        lang = tweet['lang']
        if lang == 'en':
            return True
    except KeyError as ex:
        return False
    return False   

# (not in use)
def findTopHashtags(hashtags):
    hashtagdic = dict()
    topic_name = "election_hashtags"
    for hashtag in hashtags:
        if isinstance(hashtag, list):
            if hashtag:
                for h in hashtag:
                    htext = h['text']
                    try: 
                        hashtagdic[htext] = hashtagdic[htext] + 1
                    except KeyError as ex:
                        hashtagdic[htext] = 1
    output = json.dumps(hashtagdic)
    print(output)
    if hashtagdic:
        pass
        #publishToKafka(topic_name, output)
        
# (archived)
def findTweetsPerParty(partylist):
    topic_name = "election_parties"
    partydic = dict()
    if partylist:
        for party in partylist:
            try:
                partydic[party] = partydic[party] + 1
            except KeyError as ex:
                partydic[party] = 1
    output = json.dumps(partydic)
    print(output)
    if partylist:
        pass
        #publishToKafka(topic_name, output)
        
# (not in use)
def findSentiment(tweet):
    senti_list = list()
    if tweet :
        try:
            sentiment = gc_sentiment(str(tweet))
            print(sentiment)
            category = sentiment_category(sentiment)
            senti_list.insert(0,category)
        except Exception as ex:
            print(ex)
    return senti_list

# (not in use) Aggregates the sentiment for each stream and returns a map of sentiments
def findBlobSentimentForStream(records) :
    
    topic_name = "blob_sentiments"
    sentimap = {"positive":0, "negative":0, "neutral": 0}
    unprocessed_count = 0
    for record in records:
        try:
            sentiment = blobSentimentAnalysis(str(record))
            #print(sentiment)
            category = sentimentCategoryBlob(sentiment)
            previous_count = sentimap[category]
            sentimap[category] = previous_count+1
        except Exception as ex:
            #print(ex)
            unprocessed_count += 1
    output = json.dumps(sentimap) 
    print(output)
    if len(records) > 0:
        #publishToKafka(topic_name, output)
        pass