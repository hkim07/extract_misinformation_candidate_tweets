import pandas as pd
import twint
from datetime import datetime, timedelta
from time import sleep
import os

query = '((corona OR virus OR coronavirus OR covid-19 OR covid19 OR 2019-ncov OR wuhanvirus OR (wuhan AND virus)) AND (treat OR cure OR remedy))'


start_str = "2020-01-01"
end_str = "2020-03-31"
start_date = pd.to_datetime(start_str, format='%Y-%m-%d', errors='ignore')
end_date = pd.to_datetime(end_str, format='%Y-%m-%d', errors='ignore')
filename = f"{start_str}_{end_str}.csv"
resume_file = f"resume.txt"

c = twint.Config()
c.Hide_output = True
c.Store_csv = True
c.Output = filename
c.Resume = resume_file
c.Search = query
c.Lang = 'en'

while start_date < end_date:

    check = 0
    c.Since = datetime.strftime(start_date, format='%Y-%m-%d')
    c.Until = datetime.strftime(start_date + timedelta(days=1), format='%Y-%m-%d')

    while check < 1:
        try:
            print("Running Search: Check ", start_date)
            twint.run.Search(c)
            check += 1

        except Exception as e:
            # pause when twitter blocks further scraping
            print(e, "Sleeping for 7 mins")
            print("Check: ", check)
            sleep(420)

    # before iterating to the next day, remove the resume file
    os.remove(resume_file)

    # increment the start date by one day
    start_date = start_date + timedelta(days=1)
