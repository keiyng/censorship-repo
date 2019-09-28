from aip import AipNlp
import csv
import sys
import io
import json
import pandas as pd
import pprint
import urllib.request
import urllib.parse
import ssl
import requests



""" 你的 APPID AK SK """
APP_ID = '10816790'
API_KEY = 'wAsZ7j9tvafCdT0QhTz95Lkf'
SECRET_KEY = 'jmEINHCK3yppxoQcwH9sAiOF0oX8ug7b'
REFRESH_TOKEN = '25.dc3c83dfe8a8634d3a535a26a831aaf0.315360000.1859754839.282335-10816790'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

# headers = {'Content-Type': 'application/json; charset=UTF-8'}

# response = urllib.request.urlopen('https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=wAsZ7j9tvafCdT0QhTz95Lkf&client_secret=jmEINHCK3yppxoQcwH9sAiOF0oX8ug7b')
# content = response.read()
# if (content):
#     pprint.pprint(content)

r = requests.post('https://aip.baidubce.com/rest/2.0/antispam/v2/spam', params={'access_token': '25.dc3c83dfe8a8634d3a535a26a831aaf0.315360000.1859754839.282335-10816790'}, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data={'content': '这应该是哲学中最基本也是最重要的问题'})
print(r.text)


request_url = 'https://aip.baidubce.com/rest/2.0/antispam/v2/spam?access_token=25.dc3c83dfe8a8634d3a535a26a831aaf0.315360000.1859754839.282335-10816790'

df = pd.read_csv("/Users/Kei/OneDrive/censorship-research/data/features/scrapper_ling_features.csv")


def dep_parse():

     for index, data in df.iterrows():
        data["content"] = data["content"].encode("gbk", "ignore")
        data["content"] = data["content"].decode("gbk")
        result = client.emotion(data["content"])

        pprint.pprint(result)

# dep_parse()

def sentiment_analysis():
    pos = []
    neg = []
    sentiment = []
    for index, data in df.iterrows():
        data["text"] = data["text"].encode("gbk", "ignore")
        data["text"] = data["text"].decode("gbk")
        result = client.sentimentClassify(data["text"])
        try:
            pos.append(result['items'][0]['positive_prob'])
            neg.append(result['items'][0]['negative_prob'])
            sentiment.append(result['items'][0]['sentiment'])
        except:
            pos.append(0)
            neg.append(0)
            sentiment.append(0)
        print(len(pos))

    df["pos_sent"] = pos
    df["neg_sent"] = neg
    df["sentiment"] = sentiment

    df.to_csv("test.csv")
