# Extract tweets possibly containing health misinformation

This repo provides three Python scripts to extract tweets possibly containing health misinformation. These tweets have replies semantically similar with official advice from health authorities such as the WHO and the CDC. Please follow the instructions below. 

## Dependencies should be installed first.
- pandas 1.0.0: `pip install pandas==1.0.0`
- twint 2.1.12: `pip install twint==2.1.12`
- preprocessor 0.5.0: `pip install tweet-preprocessor`
- sentence-transformers 0.2.6.1: `pip install sentence-transformers`
- scikit-learn 0.22.2.post1: `pip install -U scikit-learn`

## Instructions

1) You need to download tweet replies that satisfying a query comprising context-specific keywords by using the `twint` library.

- Here is a sample command that saves tweet replies about COVID-19 that were written in English and posted during the first week of 2020. It takes some time to be finished (~12MB). 
    * twint -s "(corona OR virus OR coronavirus OR covid-19 OR covid19 OR 2019-ncov) lang:en since:2020-01-01 until:2020-01-07 filter:replies" -o replies.json --json -ho
    * Put the download file in the `/dat` folder. Delete files given with this repo if you are not interested in COVID-19 related tweet replies. 
    * You should change the query depending on your interest. 

2) Run `preprocess.py` that returns a file `replies.csv` consisting of three columns: tweet_id, user_id, and text. Mentions, emojis, and URLs in body texts will be removed.

3) Run `calculate_similarity.py` that returns a file `replies_with_sims.csv` that a new column "sims" is added to the `replies.csv`. This column stores cosine similarity between representation vectors of replies and the vector of official advice that we set as a reference of accurate information. Representation vectors are computed through the Sentence-BERT model (Reimers & Gurevych, 2019). You can change official advice in `calculate_similarity.py`.
    * Warning messages will be shown, like "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/tensorflow/python/framework/dtypes.py:467: FutureWarning: Passing (type, 1) or '1type' as a synonym of type is deprecated; in a future version of numpy, it will be understood as (type, (1,)) / '(1,)type'.
  _np_qint32 = np.dtype([("qint32", np.int32, 1)])". Ignore them. 
    * You can observe that replies of high similarity have similar context with the official advice defined in `calculate_similarity.py`.
  
4) 

### References
Reimers, N., & Gurevych, I. (2019, November). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP) (pp. 3973-3983).

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

