from pprint import pprint
from requests import get
from dotenv import load_dotenv
import yfinance as yf
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
load_dotenv()
plt.style.use('ggplot') 


def get_stock_pred(param):
    if not param == None:
        print(f'get_stock_pred {param}')
        res = get_resonse_from_api(str(param))
        return res
    else:
        return None


def get_resonse_from_api(param):
    print("inside get_resonse_from_api", type(param))
    res = get("https://yh-finance.p.rapidapi.com/stock/v2/get-summary", headers={'x-rapidapi-host': 'yh-finance.p.rapidapi.com',

    'x-rapidapi-key': '9aa35d4502mshb4b1998a9a28115p1df00ejsn6edba7b9494d'}, params={'symbol': param})
    print(res.status_code, res.reason)
    if res.status_code == 200:
        dat = res.json()
        
        rec = {
            "buy": 1,
            "hold": 1,
            "sell": 1
        }
        
        y_earnings = []
        
        for t in dat["recommendationTrend"]["trend"]:
            rec["buy"] = (rec["buy"] + t["buy"]) 
            rec["hold"] = (rec["hold"] + t["hold"])
            rec["sell"] = (rec["sell"] + t["sell"])
        
        pprint(rec)
        
        for e in dat["earnings"]["financialsChart"]["yearly"]:
            y_earnings.append({
                "year": e["date"],
                "revenue": e["revenue"]["fmt"]
            })
        result = {
            "name": dat["price"]["longName"],
            "symbol": dat["symbol"],
            "trend": rec,
            "currentPrice": dat["price"]["regularMarketOpen"]["fmt"],
            "currency": dat['price']["currencySymbol"],
            "previousClose": dat["summaryDetail"]["previousClose"]["fmt"],
            "yearly_earning": y_earnings,
            "financial": {
                "profitMargins": dat["defaultKeyStatistics"]["profitMargins"]["fmt"],
                "52WeekChange": dat["defaultKeyStatistics"]["52WeekChange"]["fmt"],
                "sharesShort": dat["defaultKeyStatistics"]["sharesPercentSharesOut"]["fmt"],
                },
            "country": dat["summaryProfile"]["country"],
            "industry": dat["summaryProfile"]["industry"]
        }
        
        
        img = open('fig.png', 'r')
        
        START = "2017-01-01"
        TODAY = date.today().strftime("%Y-%m-%d")
    
        df = yf.download(result['symbol'], START, TODAY)
        print(np.array(df['Close']))
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
        return {"txt": txt, "img": img}

# **📰 Latest news on {result["name"]}:-**
# {result["news"]}
    else:
        return None