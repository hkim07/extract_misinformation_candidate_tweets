import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
sbert = SentenceTransformer('bert-base-nli-mean-tokens')

dat = pd.read_csv('./replies.csv')
sbert_embs = np.array(sbert.encode(dat.reply_text, show_progress_bar=True, batch_size=50))

#https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters
official_advice = "Smokers are likely to be more vulnerable to COVID-19 as the act of smoking means that fingers (and possibly contaminated cigarettes) are in contact with lips which increases the possibility of transmission of virus from hand to mouth. Smokers may also already have lung disease or reduced lung capacity which would greatly increase risk of serious illness."

advice_embs = sbert.encode([official_advice], show_progress_bar=False)
sims = cosine_similarity(advice_embs, sbert_embs)
sims = sims.flatten()

dat = dat.assign(sim=sims)
dat = dat.sort_values(by=['sim'], ascending=False)

dat.to_csv("./replies_with_sims.csv", index=False)
print("Saved in replies_with_sims.csv")
