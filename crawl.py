import pandas as pd
import twint
from datetime import datetime, timedelta
from time import sleep
import os

folder = 'dat'
if not os.path.exists(folder):
    os.makedirs(folder)
filelist = os.listdir(folder)

query = '(medicine OR remedy) AND (corona OR virus OR coronavirus OR covid-19 OR covid19 OR 2019-ncov OR wuhanvirus OR (wuhan AND virus))'
query_no_space = ''.join(query.split())
resume_file = "resume.txt"

c = twint.Config()
c.Since = "2020-01-01"
c.Until = "2020-03-31"
c.Hide_output = False
c.Store_json = True
c.Resume = resume_file
c.Search = query
c.Lang = 'en'
c.Get_replies = True

filename = f"./dat/{query_no_space}_{c.Since}_{c.Until}.json"
c.Output = filename
twint.run.Search(c)
