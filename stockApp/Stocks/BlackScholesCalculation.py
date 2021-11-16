import math
import numpy as np
from scipy.integrate import quad

def getLogAnualizedVolitilityStd(prices):
    returns = []
    for i in range(1,len(prices)):
        returnOne = math.log((prices[i] - prices[i-1])/prices[i-1] + 1)
        returns.append(returnOne)
       
    volatility  = np.std(returns)
    return volatility

def probabilityDensity(x):
    density = math.exp(-0.5*x**2)/math.sqrt(2*math.pi)
    return density

def cumDensityFunc(d):
    cumDensity = quad(lambda x: probabilityDensity(x),-20, d, limit= 50)[0]
    return cumDensity

def d1f(St, K, t, T, r, sigma):
    d1 = (math.log(St/K) + (r + 0.5 * sigma**2) * (T-t))/(sigma * math.sqrt(T - t))
    return d1

def BSM_call_value(St,K, t, T, r, sigma):
    d1 = d1f(St,K, t, T, r, sigma)
    d2 = d1 - sigma * math.sqrt(T-t)
    call_value = St * cumDensityFunc(d1) - math.exp(-r * (T-t)) * K * cumDensityFunc(d2)
    return call_value

def BSM_put_value(St,K, t, T, r, sigma):
    put_value = BSM_call_value(St,K, t, T, r, sigma) - St + math.exp(-r * (T-t) * K)
    return put_value

def calcCallOptionChain(St, startPrice, t, T, r, sigma):
    optionsDict = {}
    for strike in range(int(startPrice), int(startPrice) + 300, 10): 
        optionPrice = BSM_call_value(St, strike, t, T, r, sigma)
        optionsDict.update({str(strike):optionPrice}) 

def calcPutOptionChain(St, startPrice, t, T, r, sigma):
    optionsDict = {}
    for strike in range(int(startPrice), int(startPrice) + 300, 10): 
        optionPrice =BSM_put_value(St, strike, t, T, r, sigma)
        optionsDict.update({str(strike):optionPrice}) 

    return optionsDict
    

