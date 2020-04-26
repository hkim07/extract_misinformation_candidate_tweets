import pandas as pd
import twint
from datetime import datetime, timedelta
from time import sleep
import os

folder = 'dat'
if not os.path.exists(folder):
    os.makedirs(folder)
filelist = os.listdir(folder)

query = '(antibiotic OR antibiotics) AND (corona OR virus OR coronavirus OR covid-19 OR covid19 OR 2019-ncov OR wuhanvirus OR (wuhan AND virus))'
query_no_space = ''.join(query.split())
resume_file = "resume.txt"

c = twint.Config()
c.Since = "2020-03-01"
c.Until = "2020-03-02"
c.Hide_output = False
c.Store_csv = True
c.Resume = resume_file
c.Search = query
c.Lang = 'en'

filename = f"./dat/{query_no_space}_{c.Since}_{c.Until}.csv"
c.Output = filename
twint.run.Search(c)
