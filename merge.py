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
    x = ' '.join(emoji.get_emoji_regexp().sub(r'', x).split())
    return x

from langdetect import detect
def detect_lang(_text):
    from langdetect import DetectorFactory
    DetectorFactory.seed = 0
    try:
        lang = detect(_text)
    except:
        lang = ''
    return lang

dat = pd.read_csv('./replies_with_sims.csv')

op_df = []
for ix, target_id in enumerate(dat.reply_id):
    target_id = target_id[1:]
    try:
        with open("./parents/%s.json" % target_id, 'r') as f:
            tmp = json.load(f)
        if len(tmp)==0:
            continue
        else:
            op = tmp[-1] # direct parent
            op_df.append(['_'+str(op['id']), '_'+str(target_id), '_'+str(op['user']['id']), op['full_text']])
    except:
        continue

op_df = pd.DataFrame(op_df, columns = ['parent_id', 'reply_id', 'user_id', 'parent_text'])
op_df.parent_text = op_df.parent_text.apply(twitter_preprocessing)
lang = op_df.parent_text.apply(detect_lang)
op_df = op_df[lang=='en']

merged = op_df.merge(dat, left_on='reply_id', right_on='reply_id')
merged = merged[merged.user_id_x!=merged.user_id_y]
merged = merged[['parent_id', 'parent_text', 'reply_text', 'sim']]

merged.to_csv('./merged.csv', index=False)
print("Saved in merged.csv")
