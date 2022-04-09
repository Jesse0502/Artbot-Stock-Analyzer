from random import random
import requests
from dotenv import load_dotenv
import os
import spacy
from constants import stock_categories
import openai

load_dotenv()

nlp = spacy.load('en_core_web_md')

openai.api_key = os.getenv('OPEN_AI_TOKEN')
client_id = os.getenv('EVERYPIXEL_CLIENT_ID')
secret = os.getenv('EVERYPIXEL_SECRET')

def stock_info_res(avt):
    
    url = str(avt)
    params = {'url': url, 'num_keywords': 10}
    fetch = requests.get('https://api.everypixel.com/v1/keywords',
                         params=params, auth=(client_id, secret))
    res = fetch.json()

    fetch_status = (fetch.status_code == 200)
    if fetch_status and res["status"] == 'ok':
        keywords = ""
        noun = ""
        adj = ""

        for key in res["keywords"]:
            for n in nlp(key["keyword"]):
                if n.pos_ == "NOUN":
                    keywords = (keywords + " " + n.text).strip()
                if n.pos_ == "NOUN" and not noun:
                    noun = n.text
                if n.pos_ == "ADJ" and not adj:
                    adj = n.text
            
        stock_prediction = match_keywords_with_industry(keywords)
        cmt = comment_about(adj, noun)
        return {"stock": stock_prediction, "cmt": cmt}
    else:
        return None


def match_keywords_with_industry(keywords):
    max_till_now = {"val": -1, "stock": ""}
    for stock in stock_categories:
        compare = nlp(keywords).similarity(nlp(stock))
        if compare > max_till_now["val"]:
            max_till_now = {"val": compare, "stock": stock}

    return max_till_now

def comment_about(adj, noun):
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"Say something to me about my {adj} {noun} in my profile picture",
    temperature=1,
    max_tokens=20,
    )

    return f'{response["choices"][0]["text"]} '
