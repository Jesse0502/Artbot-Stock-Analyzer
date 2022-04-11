from pprint import pprint
from requests import get
from dotenv import load_dotenv
import yfinance as yf
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import os
load_dotenv()
plt.style.use('ggplot') 


def get_stock_pred(param):
    if not param == None:
        res = get_resonse_from_api(str(param))
        return res
    else:
        return None


def get_resonse_from_api(param):
    TOKEN = os.getenv('RAPID_API_API')
    
    res = get("https://yh-finance.p.rapidapi.com/stock/v2/get-summary", headers={'x-rapidapi-host': 'yh-finance.p.rapidapi.com',

    'x-rapidapi-key': TOKEN}, params={'symbol': param})
    if res.status_code == 200:
        dat = res.json()
        rec = {
            "buy": 1,
            "hold": 1,
            "sell": 1
        }
        if "recommendationTrend" in dat:
            for t in dat["recommendationTrend"]["trend"]:
                rec["buy"] = (rec["buy"] + t["buy"]) 
                rec["hold"] = (rec["hold"] + t["hold"])
                rec["sell"] = (rec["sell"] + t["sell"])
        else:
            rec["buy"] = '*No data found*'
            rec["hold"] = '*No data found*'
            rec["sell"] = '*No data found*'
        y_earnings = []
        if "earnings" in dat:
            for e in dat["earnings"]["financialsChart"]["yearly"]:
                y_earnings.append({
                    "year": e["date"],
                    "revenue": e["revenue"]["fmt"]
                })
        notFound = "No data found"
        result = {
            "name": dat["price"]["longName"],
            "symbol": dat["symbol"],
            "trend": rec,
            "currentPrice": dat["price"]["regularMarketOpen"].get("fmt", notFound),
            "currency": dat['price'].get("currencySymbol", notFound),
            "previousClose": dat["summaryDetail"].get("previousClose", {}).get("fmt", notFound),
            "yearly_earning": y_earnings,
            "financial": {
                "profitMargins": dat["defaultKeyStatistics"].get("profitMargins", {}).get("fmt", notFound),
                "52WeekChange": dat["defaultKeyStatistics"].get("52WeekChange", {}).get("fmt", notFound),
                "sharesShort": dat["defaultKeyStatistics"].get("sharesPercentSharesOut", {}).get("fmt", notFound),
                },
            "country": dat.get("summaryProfile", {}).get("country", notFound),
            "industry": dat.get("summaryProfile", {}).get("industry", notFound)
        }
        
        
        img = open('fig.png', 'r')
        
        START = "2017-01-01"
        TODAY = date.today().strftime("%Y-%m-%d")
    
        df = yf.download(result['symbol'], START, TODAY)
        plt.figure(figsize=(16,8))
        plt.title(f'Close Price History - {result["name"]} ({result["symbol"]})', fontsize=18)
        plt.plot(df['Close'])
        plt.xlabel("Date", fontsize=18)
        plt.ylabel("Close Price USD ($)", fontsize=18)
        plt.savefig('fig.png')
        
        txt =  f"""
    
*Here's some data I found on* ***{result["name"]} ({result["symbol"]})*** 🤔

Country:- ***{result["country"]}***
Industry:- ***{result['industry']}***

**Financials:-**
Current Price - **{result["currency"]}{result["currentPrice"]}**
Previous Close - **{result["currency"]}{result["previousClose"]}**
----
Profit Margin:- ***{result["financial"]["profitMargins"]}***
52WeekChange:- ***{result["financial"]["52WeekChange"]}***
Shares Short:- ***{result["financial"]["sharesShort"]}***

**Market Sentiments:-**
🟢 Buy - **{result["trend"]["buy"]}%**
🔴 Sell - **{result["trend"]["sell"]}%** 
🟡 Hold - **{result["trend"]["hold"]}%** 

\n\n
    """
        return {"txt": txt}

    else:
        return None
        
        