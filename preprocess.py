import os, json, re
import pandas as pd
import emoji

def twitter_preprocessing(x):
    #https://towardsdatascience.com/twitter-sentiment-analysis-using-fasttext-9ccd04465597
    #Remove mentions
    x = ' '.join(re.sub("(@[A-Za-z0-9]+)", " ", x).split())
    #Remove URLs
    x = ' '.join(re.sub("(\w+:\/\/\S+)", " ", x).split())
    #Remove emojis
    x = emoji.get_emoji_regexp().sub(r'', x)
    return x

file_list= ['./dat/'+ x for x in os.listdir('./dat/') if x.endswith('.json')]

def extract_tweet_info(x):
    return ['_'+str(x.get('id', '')), '_'+str(x.get('user_id', '')), x.get('tweet', '')]

sampled_tweets = []
for file in file_list:
    for line in open(file, 'r', encoding='latin-1'):
        sampled_tweets.append(extract_tweet_info(json.loads(line)))

sampled_tweets_df = pd.DataFrame(sampled_tweets, columns=['reply_id', 'user_id', 'reply_text'])
sampled_tweets_df = sampled_tweets_df.drop_duplicates()
sampled_tweets_df.reply_text = sampled_tweets_df.reply_text.apply(twitter_preprocessing)
sampled_tweets_df.to_csv('./replies.csv', index=False)
print("Saved in replies.csv")
