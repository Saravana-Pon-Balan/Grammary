from gingerit.gingerit import GingerIt
from textblob import TextBlob

def grammar_check(sentence):
    ginger_parser = GingerIt()

    corrected = ginger_parser.parse(sentence)['result']

    blob = TextBlob(corrected)
    sentiment = blob.sentiment.polarity
    noun_phrases = blob.noun_phrases

    return corrected, sentiment, noun_phrases
