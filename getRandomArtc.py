import random
import re
import requests
from bs4 import BeautifulSoup

def randomArticle():
    url = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(url.content, "html.parser")
    title = soup.find_all('p')
    realText = ""
    for a in title:
        realText += a.getText()


    #print(f"{realText}")

    return realText

texts = randomArticle()
# lists = texts.split(" ")
# for a in lists:
#     print(a)

with open("article.txt", "w") as article:
    article.write(texts)