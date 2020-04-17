# Extract candidate tweets possibly containing misinformation

This repo provides three Python scripts to extract candidate tweets possibly containing misinformation associated with an official advice from officially sanctioned sources such as the WHO and the CDC. Please follow the instructions below. 

1) You need to download tweet replies that satisfying a query comprising context-specific keywords by using the `twint` library. If this library is not installed on your machine, install the library first. 

```
$ pip install twint
```

- Here is a sample command that save tweet replies about COVID-19 that were written in English and posted during January, 2020
-- twint -s "(corona OR coronavirus OR covid-19 OR covid19 OR 2019-ncov) lang:en since:2020-01-01 until:2020-01-31 filter:replies" -o replies.json --json -ho

1) 

## COVID-19 misinformation about use of antibiotics

### Data collection (Jan 1 - Mar 31, 2020)
#### For replies
twint -s "((corona OR **virus** OR coronavirus OR covid-19 OR covid19 OR 2019-ncov OR wuhanvirus OR (wuhan AND virus)) AND (antibiotic OR antibiotics)) lang:en since:2019-12-31 until:2020-04-01 filter:replies" -o 20191231_20200401_replies.json --json -ho

NEXT collect their parents. 
```python
import tweepy
api = tweepy.API(auth)
api.get_status(id=target_id, tweet_mode='extended')
```
Hereafter, only analyze parents created by different users, written in English, and satisfying the query ((corona OR coronavirus OR covid-19 OR covid19 OR 2019-ncov OR wuhanvirus OR (wuhan AND virus)) AND (antibiotic OR antibiotics)). 


#### For non-replies
twint -s "((corona OR coronavirus OR covid-19 OR covid19 OR 2019-ncov OR wuhanvirus OR (wuhan AND virus)) AND (antibiotic OR antibiotics)) lang:en since:2019-12-31 until:2020-04-01 -filter:replies" -o 20191231_20200401_non_replies.json --json -ho

### Tweet replies preprocessing and sentence-BERT
#### Remove mentions, emojis, and URLs in text
```python
import preprocessor as p
p.set_options(p.OPT.MENTION, p.OPT.EMOJI, p.OPT.URL)
```
Then, feed preprocessed tweets to a Sentence-BERT model.

#### Sentence-BERT & Official advice setting
```python
from sentence_transformers import SentenceTransformer
sbert = SentenceTransformer('bert-base-nli-mean-tokens')

#https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters
who_official = "No, antibiotics do not work against viruses, only bacteria. The new coronavirus (2019-nCoV) is a virus and, therefore, antibiotics should not be used as a means of prevention or treatment. However, if you are hospitalized for the 2019-nCoV, you may receive antibiotics because bacterial co-infection is possible."
```

