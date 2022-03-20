from pprint import pprint
from matplotlib.pyplot import get
import spacy
from get_stock_pred import get_stock_pred
nlp = spacy.load('en_core_web_lg')
from random import random
from constants import response_how_ques_res, welcome_txts, greeting
from predict_stock_res import predict_stock_res

def org_res(stm):
    org_arr = []
    for ent in nlp(stm.upper()).ents:
        if ent.label_ == 'ORG':
            org_arr.append(ent)
    print(org_arr)
    if len(org_arr) == 0:
        beta_search = stm.split(" ")
        for w in beta_search:
            print((w.isupper() == True), (len(w) > 1), (w[len(w) - 1].isalpha()))
            if (w.isupper() == True) and (len(w) > 1) and (w[len(w) - 1].isalpha()):
                stock_exist = get_stock_pred(w)
                if stock_exist != None:
                    return stock_exist
                else:
                    return f"*I didn't found any stock ticker in your message!, Try again?*"
                
        return f"I'm Sorry, I didn't found any stock ticker in your message!\n\n*Hint: 'Try typing the ticker in uppercase'"
    else:
        stock_exist = get_stock_pred(org_arr[0])
        if stock_exist != None:
            return stock_exist
        else:
            return f"*I'm Sorry, I didn't found any stock ticker in your message!*"
    
def greet_res():
    reply = round(random() * len(greeting) - 1)
    return greeting[reply].capitalize()

def welcome_res():
    reply = round(random() * len(welcome_txts) - 1)
    return welcome_txts[reply].capitalize()

def how_ques_res():
    reply = round(random() * len(response_how_ques_res) - 1)
    return response_how_ques_res[reply].capitalize()

def who_made():
    return "*@JS_Artboy#0888 knows more than you about me.*"

def your_name_res():
    return "*Hi! My name is Artbot👋🤖.  Type `-help` to know more*"

def default_res():
    return "Your message wasn unclear 🤔\n *Try again? or maybe type `-help`*"
    
def help_res():
    return f"""
You can ask me if a stock is a good purchase    
eg - `Should I buy AAPL stock?` or `Is KO a good buy?`

I can make a suggestion based of your pfp what industry should be in your portfolio. Just type `-suggest`
    """
    
def predict_res(avt):
    stock = predict_stock_res(avt)
    if not stock["stock"] == None:
        if not stock['cmt'] == None:
            print(f"**{stock['stock']['stock']}**{stock['cmt']}")
            return f"**{stock['stock']['stock']}**{stock['cmt']}"
        else:
            print(f"**{stock['stock']['stock']}**")
            return f"**{stock['stock']['stock']}**"
            
    else:
        return "I Couldn't find any stocks based of your pfp. Maybe cuz it's blank"
    