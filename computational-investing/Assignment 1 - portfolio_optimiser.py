'''
   Script to simulate and assess performance of a
   4 stock portfolio
'''

import yfinance as yf
import pandas as pd
import numpy as np
import argparse as ag
from datetime import datetime, timedelta
from itertools import combinations

def develop_price_frame(startdate, enddate, syms):
    mdf = pd.DataFrame()
    for sym in syms:
        df = yf.download(sym, startdate, enddate)
        first_price = df.loc[df['Adj Close'].idxmin(), 'Adj Close']
        adcl = df['Adj Close'].to_frame()
        adcl_norm = adcl['Adj Close']/first_price
        mdf = pd.concat([mdf, adcl_norm], axis=1)

    mdf.columns = syms
    mdf.index.name = 'Date'
    mdf = mdf.reset_index().loc[1:].set_index('Date')
    
    return mdf

def simulate(investment, price_df, startdate, enddate, syms, weights):
    price_df['Portfolio_Value'] = price_df[syms[0]] * weights[0] * investment + \
                                  price_df[syms[1]] * weights[1] * investment + \
                                  price_df[syms[2]] * weights[2] * investment + \
                                  price_df[syms[3]] * weights[3] * investment

    price_df['Portfolio_Returns'] = (price_df['Portfolio_Value']/price_df['Portfolio_Value'].shift(1)) - 1
    price_df['Portfolio_Cumulative_Returns'] = 1 + price_df['Portfolio_Returns'].cumsum()
    price_df = price_df.fillna(0.0)

    vol = price_df['Portfolio_Returns'].std()
    daily_ret = price_df['Portfolio_Returns'].mean()
    cum_ret = price_df.loc[price_df.index.max(), 'Portfolio_Cumulative_Returns']
    sharpe = (daily_ret / vol) * pow(252,0.5)
   
    return vol, daily_ret, sharpe, cum_ret

def identify_weight_list(syms):
    base_list = [ 0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0 ]
    final_list = []
    for ind in range(0, len(syms)):
        final_list.extend(base_list)

    all_weights = list(combinations(final_list, 4))
    filtered_weights = list(set([ val for val in all_weights if sum(val) == 1.0 ]))

    return filtered_weights
        

def optimize_portfolio(investment, price_df, startdate, enddate, syms):
    weight_test = open('weight_test.csv', 'w')
    headers = ",".join(syms + ["Sharpe"])
    weight_test.write(headers)
    weight_test.write("\n")
    
    weight_list = identify_weight_list(syms)
    max_sharpe = 0.0
    opt_weights = []
    for weights in weight_list:
        vol, daily_ret, sharpe, cum_ret = simulate(investment, price_df, startdate, enddate, syms, weights)

        text_list = [ str(val) for val in weights ] + [ str(sharpe) ]
        text_data = ",".join(text_list)
        weight_test.write(text_data)
        weight_test.write('\n')
        
        if sharpe > max_sharpe:
            max_sharpe = sharpe
            opt_weights = weights
            ret_data = (vol, daily_ret, sharpe, cum_ret, opt_weights)
        else:
            continue

    return ret_data[0], ret_data[1], ret_data[2], ret_data[3], ret_data[4], len(weight_list)
        
if __name__ == "__main__":
    parser = ag.ArgumentParser()
    parser.add_argument("investment", help="Investment", type=str)
    parser.add_argument("startyear", help="Start Year", type=str)
    parser.add_argument("startmonth", help="Start Month", type=str)
    parser.add_argument("startday", help="Start Day", type=str)
    parser.add_argument("endyear", help="End Year", type=str)
    parser.add_argument("endmonth", help="End Month", type=str)
    parser.add_argument("endday", help="End Day", type=str)

    parser.add_argument("sym1", help="Symbol of 1st Stock", type=str)
    parser.add_argument("sym2", help="Symbol of 2nd Stock", type=str)
    parser.add_argument("sym3", help="Symbol of 3rd Stock", type=str)
    parser.add_argument("sym4", help="Symbol of 4th Stock", type=str)

    args = parser.parse_args()
    investment = float(args.investment)
    startdate = args.startyear + '-' + args.startmonth + '-' + args.startday
    enddate = args.endyear + '-' + args.endmonth + '-' + args.endday

    syms = [args.sym1, args.sym2, args.sym3, args.sym4]
    
    startdate_ptr = datetime.strptime(startdate, '%Y-%m-%d')
    enddate_ptr = datetime.strptime(enddate, '%Y-%m-%d')
    price_df = develop_price_frame(startdate, enddate, syms)
    vol, daily_ret, sharpe, cum_ret, weights, weights_verified = optimize_portfolio(investment, price_df, startdate, enddate, syms)
    
    print("Start Date: {}".format(datetime.strftime(startdate_ptr, '%B %d,%Y')))
    print("End Date: {}".format(datetime.strftime(enddate_ptr, '%B %d,%Y')))
    print("Symbols: {}".format(syms))
    print("Weights verified: {}".format(weights_verified))
    print("Optimal Allocations: {}".format(weights))
    print("Sharpe Ratio: {}".format(sharpe))
    print("Volatility (stdev of daily returns): {}".format(vol))
    print("Average Daily Return: {}".format(daily_ret))
    print("Cumulative Return: {}".format(cum_ret))
    
    
