import tweepy
import pandas as pd
import re
from textblob import TextBlob

# -------------------------------
      #Twitter API Authentication
# -------------------------------
api_key = "QEoWHsTYSkEXuePfdz7S3O9rA"
api_secret = "C75g73Scq8EiVQPvCO0FU9TYoTW1x5HGd7jx0gnx2xQVbmp7BT"
access_token = "1721432396-PAikGIttCr5aRQ7C434qJukssHbRafXfDkhDBPT"
access_secret = "6OOE5K1aF45Lose7rBUV8PWl19u1SI3efaHZlTSYsOZhU"
Bearer_Token_api = "AAAAAAAAAAAAAAAAAAAAAA5o5gEAAAAAwU6iIFZFs742ibqk9kEgqtIw8tw%3DltIn4O93HZae52pu2169pwj2btoE9dvdyYKaMjgH46HeuuRl1B"

client = tweepy.Client(
    bearer_token=Bearer_Token_api,
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_secret
)

# -------------------------------
#  Collect Tweets
# -------------------------------
query = "iPhone 17 -is:retweet lang:en"   # Change keyword here
tweets = client.search_recent_tweets(query=query, max_results=100,
                                     tweet_fields=["created_at", "text", "author_id"])

tweet_list = []
for t in tweets.data:
    tweet_list.append([t.id, t.text, t.created_at, t.author_id])

df = pd.DataFrame(tweet_list, columns=["tweet_id", "tweet_text", "created_at", "author_id"])
print("\n Raw tweets collected:")
print(df.head())

# -------------------------------
#  Filter & Clean Tweets
# -------------------------------
def clean_tweet(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)      # Remove URLs
    text = re.sub(r"@\w+", "", text)                # Remove mentions
    text = re.sub(r"#\w+", "", text)                # Remove hashtags
    text = re.sub(r"[^a-zA-Z\s]", "", text)         # Remove special characters
    text = re.sub(r"\s+", " ", text).strip()        # Remove extra spaces
    return text

df["clean_text"] = df["tweet_text"].apply(clean_tweet)

print("\n🔹 Cleaned tweets:")
print(df[["tweet_text", "clean_text"]].head())

# -------------------------------
  # Sentiment Analysis
# -------------------------------
def get_sentiment(text):
    score = TextBlob(text).sentiment.polarity
    if score > 0: return "Positive"
    elif score < 0: return "Negative"
    else: return "Neutral"

df["sentiment"] = df["clean_text"].apply(get_sentiment)

print("\n🔹 Sentiment Results:")
print(df[["clean_text", "sentiment"]].head())

# -------------------------------
#  Save to CSV
# -------------------------------
df.to_csv("tweet_sentiment_report.csv", index=False)
print("\n CSV saved as: tweet_sentiment_report.csv")
print("\n Process completed successfully!")
