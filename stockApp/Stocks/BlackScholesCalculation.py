import math
import numpy as np
from scipy.integrate import quad

def getLogAnualizedVolitilityStd(prices):
    returns = []
    for i in range(1,len(prices)):
        returnOne = (prices[i] - prices[i-1])/prices[i-1]
        returns.append(returnOne)
    print(returns)   
    dailyVol  = np.std(returns)
    volatility = math.sqrt(252) * dailyVol 
    return volatility

def probabilityDensity(x):
    density = math.exp(-0.5*x**2)/math.sqrt(2*math.pi)
    return density

def cumDensityFunc(d):
    cumDensity = quad(lambda x: probabilityDensity(x),-20, d, limit= 50)[0]
    return cumDensity

def d1f(St, K, t, T, r, sigma):
    
    TR = (T)/365
    d1 = (math.log(St/K) + (r + 0.5 * sigma**2) * (TR))/(sigma * math.sqrt(TR))
    return d1

def BSM_call_value(St,K, t, T, r, sigma):
    d1 = d1f(St,K, t, T, r, sigma)
    TR = (T)/365
    d2 = d1 - sigma * math.sqrt(TR)
    call_value = St * cumDensityFunc(d1) - math.exp(-r * TR) * K * cumDensityFunc(d2)
    return call_value

def BSM_put_value(St,K, t, T, r, sigma):
    TR = (T)/365
    put_value = BSM_call_value(St,K, t, T, r, sigma) - St + math.exp(-r * TR * K)
    return put_value

def calcCallOptionChain(St, startPrice, t, T, r, sigma):
    optionsDict = {}
    for strike in range(int(startPrice), int(startPrice) + 400, 10): 
        optionPrice = round(BSM_call_value(St, strike, t, T, r, sigma),2)
        optionsDict.update({format(strike,'.2f'): optionPrice})
        
    return optionsDict 

def calcPutOptionChain(St, startPrice, t, T, r, sigma):
    optionsDict = {}
    for strike in range(int(startPrice), int(startPrice) -400, -10): 
        optionPrice = round(BSM_put_value(St, strike, t, T, r, sigma),2)
        optionsDict.update({format(strike,'.2f'): optionPrice})
        

    return optionsDict
    

