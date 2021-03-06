import pandas as pd
import numpy as np
import scipy as spi 
import yfinance as yf
import scipy.optimize as sco
from scipy.optimize import minimize
from pt_tickers import tickers3

# This is brute force method for portfolio Optimization. 
appended_data = pd.DataFrame()
for t in tickers3:
    stock_info = yf.Ticker(f'{t}').history(period='5y',interval='1d')
    close = stock_info['Close']
    df = pd.DataFrame({f'{t}': close})
    appended_data = pd.concat([appended_data,df],axis=1)

# Statistics
risk_free_rate = 0.0298
returns = appended_data.pct_change()
mean_returns = returns.mean()
cov_matrix = returns.cov()

# Log Returns Statistics\
log_return = np.log(appended_data/appended_data.shift(1))
meanLogReurns = log_return.mean()
annualLogReturns = ((1+log_return).prod())**(252/len(log_return)) -1
Sigma = log_return.cov()*252
#NUmber of Assets 
num_assets = len(mean_returns)

'''Portfolio Optimization for Random Weights'''
num_port = 100000
weight = np.zeros((num_port,len(mean_returns)))
expectedReturn = np.zeros(num_port)
expectedVolatility = np.zeros(num_port)
sharpeRatio = np.zeros(num_port)

for k in range(num_port):
    # Generate random weight vector
    w = np.array(np.random.random(len(meanLogReurns)))
    w = w / np.sum(w)
    weight[k,:] = w

    # Expected Return
    expectedReturn[k] = np.sum((meanLogReurns * w))

    # Expected Volatility 
    expectedVolatility[k] = np.sqrt(np.dot(w.T,np.dot(Sigma, w)))

    #Sharpe Ratio
    sharpeRatio[k] = expectedReturn[k]/expectedVolatility[k]

# Printing out optimum weight to maximize sharpe ratio
maxIndex = sharpeRatio.argmax()
lmx = weight[maxIndex,:]

print(lmx)


