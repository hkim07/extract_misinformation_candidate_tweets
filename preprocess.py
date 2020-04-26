import os, json, re, ast
import pandas as pd
import numpy as np
import emoji, ftfy
def twitter_preprocessing(x):
    #https://towardsdatascience.com/twitter-sentiment-analysis-using-fasttext-9ccd04465597
    #Remove mentions
    x = ' '.join(re.sub("(@[A-Za-z0-9_]+)", " ", x).split())
    #Remove URLs
    x = ' '.join(re.sub("(\w+:\/\/\S+)", " ", x).split())
    #Remove emojis
    x = ' '.join(emoji.get_emoji_regexp().sub(r'', x).split())
    x = ftfy.fix_text(x)
    return x

folder = 'res'
if not os.path.exists(folder):
    os.makedirs(folder)

file_list= ['./dat/'+ x for x in os.listdir('./dat/') if x.endswith('.csv')]

dat = []
for file in file_list:
    dat.append(pd.read_csv(file))

dat = pd.concat(dat)

reply_ids = []
for ix, x in enumerate(dat.reply_to):
    x = ast.literal_eval(x)
    tmp = []
    for y in x:
        tmp.append(y['user_id'])
    user_id = str(dat.iloc[ix].user_id)
    if user_id in tmp:
        tmp.remove(user_id)
    reply_ids.append(tmp)

dat.id = ['_'+str(x) for x in dat.id]
dat.user_id = ['_'+str(x) for x in dat.user_id]
dat.tweet = dat.tweet.apply(twitter_preprocessing)

tweet_df = dat[['id', 'user_id', 'created_at', 'tweet']]
tweet_df = tweet_df.drop_duplicates()
tweet_df = tweet_df.assign(created_at = ['_'+str(x) for x in (tweet_df.created_at/1000.0).map(int)])

non_replies = tweet_df.loc[pd.Series([len(x) for x in reply_ids])==0]
non_replies = non_replies.reset_index(drop=True)
non_replies.to_csv('./res/non_replies.csv', index=False)

replies = tweet_df[np.array([len(x) for x in reply_ids])!=0]
replies = replies.reset_index(drop=True)
replies.to_csv('./res/replies.csv', index=False)

print("Saved in ./res folder.")
