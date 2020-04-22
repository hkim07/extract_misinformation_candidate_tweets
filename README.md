# Extract tweets possibly containing health misinformation

Please follow the instructions below. 

## Dependencies should be installed first.
- pandas: `pip install pandas`
- twint: `pip install twint`
- sentence-transformers: `pip install sentence-transformers`
- scikit-learn: `pip install -U scikit-learn`
- tweepy: `pip install tweepy`
- langdetect:`pip install langdetect`
- emoji: `pip install emoji`
- ftfy: `pip install ftfy`

## Instructions

**Assume that we are interested in identifying misinformation about COVID-19 and antibiotics**

1) Run `crawl.py` to download public tweets that satisfying a query comprising context-specific keywords by using the `twint` library.
- Credit: jomorrcode - https://github.com/twintproject/twint/issues/604
- I put the code written by jomorrcode as `crawl.py`
    * You should change query, start date, and end date, depending on your interest. 
    * This file returns `{start date}_{end date}.csv`.    

2) Run `preprocess.py` that returns a file `replies.csv` consisting of three columns: reply_id, user_id, and reply_text. Mentions, emojis, and URLs in body texts are removed.
    * As Microsoft Excel does not fully recognize tweet and user IDs, we intentionally paste "_" in front of each ID.

3) Run `calculate_similarity.py` that returns a file `replies_with_sims.csv`. A new column "sims" will be added to the data of `replies.csv`. This column stores cosine similarity between representation vectors of replies and the vector of official advice that we set as a reference of accurate information. Representation vectors are computed through the Sentence-BERT model (Reimers & Gurevych, 2019). **You should change official advice in `calculate_similarity.py`.**
    * We set the official advice related to COVID-19 and antibiotics from the WHO (Visit https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters)
    * Warning messages will be shown, like "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/tensorflow/python/framework/dtypes.py:467: FutureWarning: Passing (type, 1) or '1type' as a synonym of type is deprecated; in a future version of numpy, it will be understood as (type, (1,)) / '(1,)type'.
  _np_qint32 = np.dtype([("qint32", np.int32, 1)])". Just ignore them. 
    * You can observe that replies of high similarity have similar context with the official advice defined in `calculate_similarity.py`.
    
4) Save your Twitter API credential in `./config.py`.
    * Consumer API key as `ckey` in ./config.py
    * Consumer API secret key as `csec` in ./config.py
    * Access token as `akey` in ./config.py
    * Access token secret as `asec` in ./config.py
  
5) Run `collect_parents.py` that saves JSON files for parents of selected replies. As Twitter API has a rate limit on searching a specific tweet ID, it takes much time if you want to collect parents of all replies. For this reason, we recommend to collect parents of a subset of replies of high similarity. The size of the subset can be set with `-n`.
    * For example, if you run `python collect_parents.py -n 10`, only parents of top 10 replies in terms of similarity will be obtained.
    * JSON files will be stored in the folder `/parents`.        

6) Run `merge.py` to concatenate tweet replies and their parents in a dataframe. Now, it is time to examine whether misinformation about COVID-19 exists in parents of replies having similar context with accurate information. 
    * Self-replies are excluded as we expect volunteer fact checkers correct other users' posts containing misinformation. 
    * For obtaining better results, parents related to COVID-19 and antibiotics should be examined. Searching parents that have context-specific keywords may help to reduce the search space.
    * Several tweets contain misinformation about COVID-19 and antibiotics. For example, a tweet (ID = 1221440124912713730) claimed that an antibiotics therapy is effective against COVID-19 and another tweet (ID = 1221334540993478656) raised a conspiracy theory that COVID-19 was created by the China to sell more antibiotics.

### References
Reimers, N., & Gurevych, I. (2019, November). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP) (pp. 3973-3983).
