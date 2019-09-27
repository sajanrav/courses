############################################################
# Functions to generate comparative Annualized Returns, Ann-
# ualized Standard Deviation and Sharpe Ratios between Boll-
# inger Bands/Buy & Hold Strategies and RSI / Buy & Hold St-
# rategies for a given list of prices of a security 
#
# USAGE:
# 1. Bollingers/Buy & Hold :
#    func_bb_bands(xts_price_vector, days, std)
#    where xts_price_vector : XTS vector with price data
#          days : No. of days to calculate MA (default: 20)
#          std : Standard deviation (default: 2)
#           
#    Eg. func_bb_bands(xts_vector) 
#        func_bb_bands(xts_vector, 10, 1)
#         
# 2. RSI/Buy & Hold :
#    func_rsi(xts_price_vector, down, up)
#    where xts_price_vector : XTS vector with price data
#          down : Lower limit for RSI (default: 30)
#          up : Upper limit for RSI (default: 70)
#           
#    Eg. func_rsi(xts_vector)
#        func_rsi(xts_vector, 25, 65)
#
############################################################



library(quantmod)
library(PerformanceAnalytics)
library(lubridate)
library(tidyverse)

func_bb_bands=function(xts_vector, days=20, std=2){
  bb=BBands(xts_vector, n=days, sd = std)
  bbtr=lag(ifelse(lag(xts_vector)<lag(bb[,1]) & xts_vector>bb[,1],1, ifelse(lag(xts_vector)<lag(bb[,3]) & xts_vector>bb[,3], -1,0)))
  bbtr[is.na(bbtr)]=0
  bbpos=ifelse(bbtr>1,1,0)
  for (i in 1:length(bbpos)){
    bbpos[i] = ifelse(bbtr[i]==1, 1, ifelse(bbtr[i]==-1, 0, bbpos[i-1]))
  }
  bbpos[is.na(bbpos)]=0
  rets=dailyReturn(xts_vector, type='arithmetic')
  bhstrat=rets
  bbstrat=bbpos*rets
  bbstrat_comp=cbind(bbstrat,bhstrat)
  colnames(bbstrat_comp)=c("BB","BH")
  return(table.AnnualizedReturns(bbstrat_comp))
}

func_rsi=function(xts_vector, days=14, down=30, up=70){
  rsi=RSI(xts_vector, n=days)
  rsitr=lag(ifelse(lag(rsi)<down & rsi>down,1,ifelse(lag(rsi)<up & rsi>up,-1,0)))
  rsitr[is.na(rsitr)]=0
  rsipos=ifelse(rsitr>1,1,0)
  for (i in 1:length(rsipos)){
    rsipos=ifelse(rsitr==1, 1, ifelse(rsitr==-1,0,rsipos[i-1]))
  }
  rsipos[is.na(rsipos)]=0
  rets=dailyReturn(xts_vector, type='arithmetic')
  bhstrat=rets
  rsistrat=rsipos*rets
  rsistrat_comp=cbind(rsistrat,bhstrat)
  colnames(rsistrat_comp)=c("RSI","BH")
  return(table.AnnualizedReturns(rsistrat_comp))
  
}
