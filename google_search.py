from googlesearch import search, search_news
from bs4 import BeautifulSoup
import re
from keywords import simple_rake
from datetime import date
import urllib.request
from time import sleep
from googleapiclient.discovery import build
import embedding


model = None
site = "cnn.com"
title_class = "pg-headline"
num_search_url = 250
num_recursion = 3

CSE_ID = "001991282022784705633:tfydvzge3ue"
API_KEY = "AIzaSyCO0YDXwTFGkgjjEbEXj-wWOhzjFMUkmMA"


def extract_date(url):
    list_dates = re.findall(r'/(\d{4})/(\d{1,2})/(\d{1,2})/', url)
    if list_dates:
        news_date = list_dates[0]
        return date(int(news_date[0]), int(news_date[1]), int(news_date[2]))
    else:
        return None

def extract_pagehead(url):
    urlf = urllib.request.urlopen(url)
    soup =  BeautifulSoup(urlf, "html.parser" )
    pagehead = soup.find_all("h1")[0]
    return pagehead.text


def recursive_search(query_input, date=date.today()):
    global model
    if not model:
        model = embedding.EmbeddingModel()
    query = "site:{} {}".format(site, query_input)
    list_url = list(search_news(query, tld="co.in", num=15, stop=15, pause=2))
    result = [] # {title: , url: , similarity:
    for url in list_url:
        news_date = extract_date(url)
        if news_date:
            if news_date < date:
                pagehead = extract_pagehead(url)
                keywords = simple_rake(pagehead)
                for keyword in keywords:
                    similarity = model.phraseSimilarity(keyword[1], query_input)
                    info_dic = {}
                    info_dic['title'] = pagehead
                    info_dic['url'] = url
                    info_dic['similarity'] = similarity
                    info_dic['keyword'] = keyword[1]
                    info_dic['date'] =  news_date
                    result.append(info_dic)
    result = filter(lambda x: x['similarity'] < 0.99, result) 
    result = sorted(result, key=lambda x: x['similarity'], reverse=True)[:3]
    new_query = ""
    for info in result:
        new_query += info['keyword']
        new_query += " "
    return result, new_query 

def recursive_model(initial_query):
    output_result = {'results':[]}
    query_input = initial_query
    for i in range(num_recursion):
        result, query_input = recursive_search(query_input) 
        print(result)
        for info in result:
            output_result['results'].append({
                'date': info['date'], 
                'title' : info['title'], 
                'url' : info['url']
                })
    print(output_result)
    return output_result


def google_search(query_input):
    query = "site:{} {}".format(site, query_input)
    list_url = list(search_news(query, tld="co.in", num=num_search_url, stop=num_search_url, pause=3))
    current_date = date.today()

    info = {'results':[]}

    print("extracting timeline.....")
    for url in list_url:
        news_date = extract_date(url)
        if news_date:
            if news_date < current_date:
                current_date = news_date
                pagehead = extract_pagehead(url)
                info['results'].append({
                    'date': news_date, 
                    'title' : pagehead, 
                    'url' : url})
                print(news_date)
                print(pagehead)
                print(url)
                print(simple_rake(pagehead))
                print(" ")
    info['results'] = sorted(info['results'], key=lambda x : x['date'], reverse=False)
    info['results'].reverse()
    return info

def main():
    recursive_model("Iraq War")

if __name__ == "__main__":
    main()

                

