from django.shortcuts import render
from pandas_datareader import data
import pandas as pd
import json
from datetime import date 
import datetime 
import pandas_datareader.data as pdr
import yfinance as yf
from. import BlackScholesCalculation as bsc
from alpha_vantage.timeseries import TimeSeries
import requests
from yahoo_fin import options

myKey =  "8MY3LIWOHCF78K17"
 
def addStock(request):
    return render(request,'addStock.html', {})


# Create your views here.
def home(request):
    #pk_31a1b8fffcc8415eb270b92c98757e06
    import requests
    import json
    
    
    myKey =  "8MY3LIWOHCF78K17"
    if request.method == 'POST':
           
            ticker = request.POST["ticker"]
            strExpDate = request.POST["expDate"]

            url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey=8MY3LIWOHCF78K17'
            req = requests.get(url)
            stockA = req.json()
            print(stockA['Time Series (Daily)']['2021-11-16'])

            url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=CNY&apikey=8MY3LIWOHCF78K17'
            r = requests.get(url)
            crypto = r.json()
            #print(crypto)
            
            #print(datetime.date.today())
            expDate = datetime.datetime.strptime(strExpDate,"%Y-%m-%d").date()
            print(expDate)
           
            timeToExpDelta =  expDate - datetime.date.today()
            DaysToExp = timeToExpDelta.days
            print(DaysToExp)
            stock = yf.Ticker(ticker)
            startDate = '2020-11-10'
            endDate = '2021-11-17'
            stockData  = data.get_data_yahoo(ticker, startDate, endDate)
            #date_unit = "s"
            jsonDataString = stockData.to_json( date_format = 'iso', double_precision = 2)
            jsonDataDict = json.loads(jsonDataString) 
            print(jsonDataDict)
           
           
            api_quote = requests.get("https://sandbox.iexapis.com/stable/stock/"+ticker+"/quote?token=Tpk_e52c0b5efdff4d758f59a043f6001d40")
            api_chart = requests.get("https://sandbox.iexapis.com/stable/stock/"+ticker+"/chart?token=Tpk_e52c0b5efdff4d758f59a043f6001d40")
            try:
                apiQuote = json.loads(api_quote.content)
                apiChart = json.loads(api_chart.content)
            except:
                apiQuote = "Error"
                apiChart = "Error"
            priceList = list(jsonDataDict['Close'].values())
            volatility = bsc.getLogAnualizedVolitilityStd(priceList)
            #volatility = 0.3
            High = stockA['Time Series (Daily)']['2021-11-17']['2. high']
            Close = float(stockA['Time Series (Daily)']['2021-11-17']['4. close'])
            Low = stockA['Time Series (Daily)']['2021-11-17']['3. low']
            optionsChain = bsc.calcCallOptionChain(Close, 950.0, 0.0, DaysToExp, 0.03, volatility)

            Open = stockA['Time Series (Daily)']['2021-11-17']['1. open']

            return render(request,'home.html', {'apiQuote':jsonDataDict, 'Open':Open, 'Close':Close, 'Low':Low, 'High':High, 'Volatility':volatility, 'optionsChain' :optionsChain})



    else:       
        return render(request,'home.html',{'ticker':"enter a valid ticker symbol"})


    api_request = requests.get("https://sandbox.iexapis.com/stable/stock/TSLA/quote?token=Tpk_e52c0b5efdff4d758f59a043f6001d40")
    try:
        api = json.loads(api_request.content)
    except:
        api = "Error"
    



    return render(request,'home.html',{'api':api})