from pprint import pprint
from requests import get
from get_stock_news import getSearch
from dotenv import load_dotenv

load_dotenv()

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
        
        news_res = getSearch(f"{param} stock", "IN", 4)
        news = ""
        for n in news_res:
            news = news + f"""\n☞ [{n["Heading"]}](<{n["Link"]}>)"""
        
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
            "news": news,
            "financial": {
                "profitMargins": dat["defaultKeyStatistics"]["profitMargins"]["fmt"],
                "52WeekChange": dat["defaultKeyStatistics"]["52WeekChange"]["fmt"],
                "sharesShort": dat["defaultKeyStatistics"]["sharesPercentSharesOut"]["fmt"],
                },
            "country": dat["summaryProfile"]["country"],
            "industry": dat["summaryProfile"]["industry"]
        }
        return f"""
    
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

**📰 Latest news on {result["name"]}:-**
{result["news"]}
    """
    else:
        return None