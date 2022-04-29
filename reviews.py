import pandas as pd
import numpy as np
import requests
from textblob import TextBlob as tb
from bs4 import BeautifulSoup as bs
from matplotlib import pyplot as plt
import time

import nltk
import re 
from IPython.display import clear_output
import matplotlib.pyplot as plt
import seaborn as sns

stopwords = nltk.corpus.stopwords.words("english")

def ruku_likn_de(url , pg = 20):
    if url[12:12+6] == "amazon":
        print("Amazon Link Detected")
        return find_amazon_data_ruku(url , pg)
    else:
        print("FLipkart Link Detected")
        return find_Flip_data_ruku(url , pg)


def mood(t):
        mood = tb(t).sentiment.polarity
        if mood > 0:
            return "Happy"
        elif mood == 0:
            return "No Mood"
        else:
            return "Sad"

#Amazon Website
def find_amazon_data_ruku(link , pg = 10   ):
    raw = link
    last = pg
    code = 0
    review = []
    for p in range(1,last+1):
        num = raw.find("ref")
        url_1 = raw[0:num]
        url_2 = f"ref=cm_cr_arp_d_paging_btm_next_{p}?ie=UTF8&reviewerType=all_reviews&pageNumber={p}"
        finalurl = url_1+url_2
        finalurl = finalurl.replace("/dp/","/product-reviews/")
        data = requests.get(finalurl)
        print("amazon Link Detected")
       
        if (data.reason) == "OK" :
            code = code+1
        data = bs(data.content ,"html.parser")
        data = data.find_all(class_= "aok-relative")
        print(int(p/last *100) , "% Completion")
        print(int(code/last * 100) , "% Success Rate")
        clear_output(wait=True)

        for d in data:
            d = {
                "Rating" : float(d.find(class_="a-link-normal").text[0:3]),
                "Title" : tb(d.find(class_="review-title-content").text).correct(),
                "Content" : (d.find(class_="review-text-content").text),
                "Polarity": mood(d.find(class_="review-text-content").text)
            }
            review.append(d)
    print((code/last) * 100 ,"% is the Sucess rate")
   
    data = pd.DataFrame(review)
    data.replace("\n","",regex=True,inplace=True)

    
    data["Polartiy"] = data["Content"].apply(mood)
    for d in data.columns:
        try:
            data[d] = data[d].apply(low)

        except:
            pass
    show_rating_bar(data)
    show_pie_chart(data)
    show_Sad_chart(data , n = 1)
    show_Happy_chart(data, n = 1)
    return review

#flipkart
def find_Flip_data_ruku(link , pg = 50):
    raw = link
    last = pg
    code = 0
    review = []
    for p in range(1,last+1):
        num = raw.find("&")
        url_1 = raw[0:num+1]+f"page={p}"
        url_1 = url_1.replace("/p/","/product-reviews/")
        
        data = requests.get(url_1)
        
        if (data.reason) == "OK" :
            code = code+1
        data = bs(data.content,"html.parser")
        
        data = data.find_all(class_= "col _2wzgFH K0kLPL")
        
        
        print(int(p/last *100) , "% Completion")
        print(int(code/last * 100) , "% Sucess Rate")
        clear_output(wait=True)

        for d in data:
            d = {
                "Rating" : float(d.find(class_="_1BLPMq").text),
                "Title" : d.find(class_="_2-N8zT").text,
                "Content" : d.find(class_="t-ZTKy").text
            }
            review.append(d)
    print((code/last) * 100 ,"% is the Sucess rate")
   
    data = pd.DataFrame(review)
    data.replace("\n","",regex=True,inplace=True)
    def mood(t):
        mood = tb(t).sentiment.polarity
        if mood > 0:
            return "Happy"
        elif mood == 0:
            return "No Mood"
        else:
            return "Sad"
    data["Polartiy"] = data["Content"].apply(mood)
    for d in data.columns:
        try:
            data[d] = data[d].apply(low)

        except:
            pass
    show_rating_bar(data)
    plt.close()
    show_pie_chart(data)
    plt.close()
    show_Sad_chart(data , n = 2)
    plt.close()
    show_Happy_chart(data, n = 2)
    plt.close()
    return review
    


def low(text):
    return text.lower()


def show_rating_bar(data):
    rating = data.groupby(by="Rating")[["Title"]].count()
    sns.barplot(y=rating.Title,x = rating.index)
    plt.savefig("static/rate.png")
    plt.clf()
#     time.sleep(1)
    
def show_pie_chart(data):
    try:
            
        x = data.groupby(by="Polartiy")[["Content"]].count()
        
        plt.pie(x = x.Content,autopct='%.2f',shadow=True,labels=x.index)
        plt.savefig("static/pie.png")
        plt.clf()
#         time.sleep(1)
        
    except:
        pass
def show_Happy_chart(data, n = 1):
    sad_data = data[data["Polartiy"] == "happy"]
    
    words = []
    for i in range(0,len(sad_data)):
        a = data.Content[i]
        a = re.sub("[', ),:,(,.,!,&,]"," ",a)
        a = re.sub("[0-9]"," ",a)
        a = " ".join(a.split())
        a = nltk.word_tokenize(a)
        a = nltk.ngrams(a,n)
        for m in a:
            if m not in stopwords:
                words.append(m)
    val =  nltk.FreqDist(words).values()
    key =  nltk.FreqDist(words).keys()
    data_1 = pd.DataFrame(data={"Key":key, "val": val})
    data_1= data_1.sort_values(by = "val",ascending=False)[0:10]
    plt.figure(figsize=(8,8))
    sns.barplot(x = data_1.val, y = data_1.Key,orient="h")
    plt.savefig("static/hapy.png")
    plt.clf()
#     time.sleep(1)
    
def show_Sad_chart(data , n = 1):
    sad_data = data[data["Polartiy"] == "sad"]
    
    words = []
    for i in range(0,len(sad_data)):
        a = data.Content[i]
        a = re.sub("[', ),:,(,.,!,&,]"," ",a)
        a = re.sub("[0-9]"," ",a)
        a = " ".join(a.split())
        a = nltk.word_tokenize(a)
        
        a = nltk.ngrams(a,n)
        for m in a:
            if m not in stopwords:
                words.append(m)
    val =  nltk.FreqDist(words).values()
    key =  nltk.FreqDist(words).keys()
    data_1 = pd.DataFrame(data={"Key":key, "val": val})
    data_1= data_1.sort_values(by = "val",ascending=False)[0:10]  
    sns.barplot(x = data_1.val, y = data_1.Key,orient="h")
    plt.savefig("static/sad.png")
    plt.clf()
#     time.sleep(0)
    
    
    
def low(text):
    return text.lower()
    