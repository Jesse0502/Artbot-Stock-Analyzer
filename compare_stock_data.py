from cProfile import label
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date
plt.style.use('ggplot') 

def compare_stock_data(stocks):
    plt.figure(figsize=(16,8))
    plt.title(f'Close Price History)', fontsize=18)
    
    stock_arr = []
    legends = []
    no_data_found = []
    for stock in stocks:
        TODAY = date.today().strftime("%Y-%m-%d")
        data = yf.download(stock, '2017-01-01', TODAY)
        if len(data) > 1:
            stock_arr.append({"data": data, "stock": stock})
        else:
            no_data_found.append(stock)
    for idx, i in enumerate(stock_arr):
        plt.plot(i['data']['Close'])
        legends.append(i['stock'].upper())
    plt.legend(legends)
    plt.xlabel("Date", fontsize=18)
    plt.ylabel("Close Price USD ($)", fontsize=18)
    plt.savefig('fig.png')
    if len(stock_arr) < 1:
        return f"No data found for ***{', '.join(no_data_found)}***"
    if len(stocks) != len(stock_arr):
        return {"txt": f"Here's your comparison:-\n\n *No data found for* ***{', '.join(no_data_found)}*** "}
    return {"txt": "Here's your comparison:-"}
