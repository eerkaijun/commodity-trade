###### DOCUMENTATION ######
# Malaysia Palm Oil News Article
# http://bepi.mpob.gov.my/news/detail.php?id=x
# Scrape only the date, title and article content and store in a csv file
# Run command 'python mpobNewsScraper.py' to execute this script
###########################


from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime, timedelta
from langdetect import detect
import tqdm
import time
import pandas as pd
import numpy as np
import re
import csv
import string


def remove_special_characters(text):
    pattern = r'[^a-zA-z0-9$%!?/.,&\<\>()\-\s\'\+]'
    text = re.sub(pattern, '', text)
    return text

newsList = []
for i in tqdm(range(15000,23000)):
    url = "http://bepi.mpob.gov.my/news/detail.php?id=" + str(i) 
    page = urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")
    posts = soup.find("table")
    temp = posts.findAll("span", {"class": "style23"})
    postdt = temp[0].text.strip()
    postdt = datetime.strptime(postdt, "%d/%m/%Y").date()
    posttitle = temp[-1].text.strip()
    posttitle = remove_special_characters(posttitle)
    postcontent = posts.find("div",{"class": "style10"})
    passage = ''
    for child in postcontent.findAll('p'): 
        paragraph = child.text.strip()
        passage = passage + ' ' + paragraph
        child.decompose()
    passage = postcontent.text.strip() + passage
    passage = remove_special_characters(passage)
    passage = passage.replace('\n','')
    try:
      if detect(passage) != 'en':
        continue
    except: 
      continue
    newsList.append([postdt,posttitle,passage])

with open('mpobNews.csv', 'w', newline='', encoding="utf-8") as writeFile:
    writer = csv.writer(writeFile)
    headers = ['Date', 'Title','Text']
    writer.writerow(headers)
    for i in newsList:
        writer.writerow(i)
  
writeFile.close()
print("mpob news retrieval success!")