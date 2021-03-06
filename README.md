# Extract tweets possibly containing health misinformation

Please follow the instructions below. 

## Dependencies should be installed first.

```
pip install -r requirements.txt
```

- pandas: `pip install pandas`
- twint: `pip install twint`
- sentence-transformers: `pip install sentence-transformers`
- tweepy: `pip install tweepy`
- langdetect:`pip install langdetect`
- emoji: `pip install emoji`
- ftfy: `pip install ftfy`

## Instructions

**Assume that we are interested in identifying misinformation about COVID-19 and antibiotics**

1) Run `crawl.py` to download public tweet replies that satisfy a query comprising context-specific keywords.
    * You should change query, start date, and end date, depending on your interest. 
    * This script returns `{query}_{start date}_{end date}.csv` in the `/dat` folder.   
    * As Twitter often blocks repeated requests, `twint` library offers an option `Resume` to resume search from the last scroll ID. `crawl.py` saves `resume.txt` for this purpose. If this script stops, wait a few minutes and run the script again. Do not delete `resume.txt` until you get the intended data.
    * If you want to run a script for a new query, delete the existing `resume.txt`.
    * We preset the query for collecting tweet replies posted on March 1, 2020.

2) Run `preprocess.py` that returns two files `replies.csv` and `non_replies.csv` in the `./res` folder. These files consist of four columns: id, user_id, created_at, and tweet. Mentions, emojis, and URLs in body texts are removed.
    * As Microsoft Excel does not fully recognize tweet and user IDs, we intentionally paste "_" in front of IDs and created_at. 

3) Run `calculate_similarity.py` that returns a file `./res/replies_with_sims.csv`. A new column "sims" will be added to the data of `replies.csv`. This column stores cosine similarity between representation vectors of replies and the vector of official advice that we set as a reference of accurate information. Representation vectors are computed through the Sentence-BERT model (Reimers & Gurevych, 2019). **You should change official advice in `calculate_similarity.py`.**
    * We set the official advice related to COVID-19 and antibiotics from the WHO (Visit https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters)
    * Warning messages can be shown, like "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/tensorflow/python/framework/dtypes.py:467: FutureWarning: Passing (type, 1) or '1type' as a synonym of type is deprecated; in a future version of numpy, it will be understood as (type, (1,)) / '(1,)type'.
  _np_qint32 = np.dtype([("qint32", np.int32, 1)])". If you encounter any warning messages, Just ignore them. 
    * You can observe that replies of high similarity have similar context with the official advice defined in `calculate_similarity.py`.
    
4) Save your Twitter API credential in `config.py`.
    * Consumer API key as `ckey` in `./config.py`
    * Consumer API secret key as `csec` in `./config.py`
    * Access token as `akey` in `./config.py`
    * Access token secret as `asec` in `./config.py`
    * `config.py` should have four lines as follows.
    
      ```
      ckey=''
      csec=''
      akey=''
      asec=''
      ```
  
5) Run `collect_parents.py` that saves JSON files for parents of selected replies. As Twitter API has a rate limit on searching a specific tweet ID, it takes much time if you want to collect parents of all replies. For this reason, we recommend to collect parents of a subset of replies of high similarity. The size of the subset can be set with `-n`.
    * For example, if you run `python collect_parents.py -n 10`, only parents of top 10 replies in terms of similarity will be obtained.
    * JSON files will be stored in the folder `./parents`.        

6) Run `merge.py` to concatenate tweet replies and their parents in a dataframe `./res/merged.csv`. Now, it is time to examine whether misinformation about COVID-19 exists in parents of replies having similar context with accurate information. 
    * Self-replies are excluded as we expect volunteer fact checkers correct other users' posts containing misinformation. 
    * For obtaining better results, parents related to COVID-19 and antibiotics should be examined. Searching parents that have context-specific keywords may help to reduce the search space.
    * An example tweet containing misinformation about COVID_19 and antibiotics: (ID = 1234076122381418496) claimed that antibiotics work against COVID-19 because the new coronavirus is just a flu virus. 

### References
Reimers, N., & Gurevych, I. (2019, November). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP) (pp. 3973-3983).
