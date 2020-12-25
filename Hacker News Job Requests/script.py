from hackernews import HackerNews
import urllib.request
from bs4 import BeautifulSoup

hn = HackerNews()
out = open('..\\hacker_news_jobs.csv','w')

jobs = hn.job_stories(limit=None)


words = ['data science','data scientist','ml','machine learning','python','sql','healthcare','clinic','business intelligence','bi','machine','learning','business','intelligence']

for job in jobs:
    if job.text is not None:
        if any(word in job.text.lower() for word in words):
            out.write(str(job) + '\n')
    else:
        try:
            html = urllib.request.urlopen(job.url).read()
            soup = BeautifulSoup(html, "html.parser")
        except:
            continue

        if any(word in soup for word in words):
            out.write(str(job) + '\n')