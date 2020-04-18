import os, json
import pandas as pd
import preprocessor as p
p.set_options(p.OPT.MENTION, p.OPT.EMOJI, p.OPT.URL)

def twitter_preprocessing(x):
  tmp = p.clean(x)
  return tmp

file_list= ['./dat/'+ x for x in os.listdir('./dat/') if x.endswith('.json')]

def extract_tweet_info(x):
    return ['_'+str(x.get('id', '')), '_'+str(x.get('user_id', '')), x.get('tweet', '')]

sampled_tweets = []
for file in file_list:
    for line in open(file, 'r', encoding='latin-1'):
        sampled_tweets.append(extract_tweet_info(json.loads(line)))

sampled_tweets_df = pd.DataFrame(sampled_tweets, columns=['reply_id', 'user_id', 'reply_text'])
sampled_tweets_df.reply_text = sampled_tweets_df.reply_text.apply(twitter_preprocessing)
sampled_tweets_df.to_csv('./replies.csv', index=False)
print("Saved in replies.csv")
