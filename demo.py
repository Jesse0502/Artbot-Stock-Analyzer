from predict_stock_trend import predict_stock_trend

def predict_res(stm):
    splitMsg = stm.split()
    ticker = splitMsg[1]
    yrs = splitMsg[2]
    predict_stock_trend(ticker, yrs)
    return

predict_res("-predict AAPL 5")