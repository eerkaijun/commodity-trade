###### DOCUMENTATION ######
# Summarise Malaysia Palm Oil News Article
# Use BERT pre trained model for summarising tasks
# pip install transformers to get pre trained BERT model
# Make sure previously scraped news article csv file (mpobNews.csv) in this case is in the same directory
# Run command 'python summarisation.py' to execute this script
###########################

import tqdm
import pandas as pd
import csv
from transformers import pipeline

summarizer = pipeline(task='summarization', device=0) # to utilise GPU 
news = pd.read_csv('mpobNews.csv')
news = news[['Date','Text']]

with open('summarized.csv', 'a', newline='', encoding="utf-8") as writeFile:
  writer = csv.writer(writeFile)
  headers = ['Date','Text']
  writer.writerow(headers)

for i in tqdm(range(len(news))):
  text = news.iloc[i].Text
  date = news.iloc[i].Date
  # Maximum character of an article is 3500 characters
  if len(text) > 3500: 
    text = text[0:3500]
  summary = summarizer(text, max_length=500)
  shorten = summary[0]['summary_text'].strip()
  shorten = re.sub(r'\s([?.!"](?:\s|$))', r'\1', shorten)
  with open('summarized.csv', 'a', newline='', encoding="utf-8") as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow([date,shorten])

writeFile.close()