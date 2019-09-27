library(quantmod)
library(PerformanceAnalytics)
library(tseries)
library(tidyquant)
library(tidyverse)
library(dplyr)

returns = read.csv("G://nse50_monthly_returns_25_stocks.csv")
returns.use = returns[,-1]
returns.dist = dist(returns.use)
returns.hclust = hclust(returns.dist)
plot(returns.hclust, labels=returns$company, main='Nifty 25 Stocks Cluster')

returns_filt = filter(returns, 
                      company=="HINDALCO.NS"|company=="TITAN.NS"|
                      company=="EIGHERMOT.NS"|company=="HEROMOTOCO.NS"|
                      company=="ASIANPAINT.NS"|company=="BRITANNIA.NS"|
                      company=="HDFCBANK.NS"|company=="AXISBANK.NS"|
                      company=="TECHM.NS"|company=="HCLTECH.NS"|
                      company=="INFY.NS"|company=="BPCL.NS"|
                      company=="ONGC.NS"|company=="COALINDIA.NS"|
                      company=="NTPC.NS"|company=="JSWSTEEL.NS"|
                      company=="M&M.NS"|company=="GRASIM.NS"
                      )

returns_t = t(returns_filt)
colnames(returns_t) = returns_t[1,]
returns_t = returns_t[-1, ]
class(returns_t) = "numeric"
opt=portfolio.optim(returns_t, shorts=FALSE, rf = 0.07/12)
opt
