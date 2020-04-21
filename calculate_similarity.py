import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
sbert = SentenceTransformer('bert-base-nli-mean-tokens')

dat = pd.read_csv('./replies.csv')
sbert_embs = np.array(sbert.encode(dat.reply_text, show_progress_bar=True, batch_size=50))

#https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters
official_advice = "The first human cases of COVID-19 were identified in Wuhan City, China in December 2019. At this stage, it is not possible to determine precisely how humans in China were initially infected with SARS-CoV-2."

advice_embs = sbert.encode([official_advice], show_progress_bar=False)
sims = cosine_similarity(advice_embs, sbert_embs)
sims = sims.flatten()

dat = dat.assign(sim=sims)
dat = dat.sort_values(by=['sim'], ascending=False)

dat.to_csv("./replies_with_sims.csv", index=False)
print("Saved in replies_with_sims.csv")
