from django.shortcuts import render
from pandas_datareader import data
import pandas as pd
import json
from datetime import date 
import datetime 
import pandas_datareader.data as pdr
import yfinance as yf
from. import BlackScholesCalculation as bsc


def addStock(request):
    return render(request,'addStock.html', {})


# Create your views here.
def home(request):
    #pk_31a1b8fffcc8415eb270b92c98757e06
    import requests
    import json
    
    

    if request.method == 'POST':
           
            ticker = request.POST["ticker"]
            strExpDate = request.POST["expDate"]
            
            print(datetime.date.today())
            expDate = datetime.datetime.strptime(strExpDate,"%Y-%m-%d").date()
            print(expDate)
           
            timeToExpDelta =  expDate - datetime.date.today()
            DaysToExp = timeToExpDelta.days
            print(DaysToExp)
            stock = yf.Ticker(ticker)
            startDate = '2019-03-17'
            endDate = '2020-03-17'
            stockData  = data.get_data_yahoo(ticker, startDate, endDate)
            #date_unit = "s"
            jsonDataString = stockData.to_json( date_format = 'iso', double_precision = 2)
            jsonDataDict = json.loads(jsonDataString) 
           
           
           
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
            High = list(jsonDataDict['High'].values())[-1]
            Close = list(jsonDataDict['Close'].values())[-1]
            optionsChain = bsc.calcListOptionChain(Close, 300.0, 0.0, DaysToExp, 0.03, volatility)

            High = list(jsonDataDict['High'].values())[-1]

            return render(request,'home.html', {'apiQuote':jsonDataDict, 'Open':list(jsonDataDict['Open'].values())[-1], 'Close':list(jsonDataDict['Close'].values())[-1], 'Low':list(jsonDataDict['Low'].values())[-1], 'High':High, 'Volatility':volatility, 'optionsChain' :optionsChain})



    else:       
        return render(request,'home.html',{'ticker':"enter a valid ticker symbol"})


    api_request = requests.get("https://sandbox.iexapis.com/stable/stock/TSLA/quote?token=Tpk_e52c0b5efdff4d758f59a043f6001d40")
    try:
        api = json.loads(api_request.content)
    except:
        api = "Error"
    



    return render(request,'home.html',{'api':api})