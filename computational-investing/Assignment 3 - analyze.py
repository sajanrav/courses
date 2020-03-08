'''
   Script to calculate portfolio and market index
   metrics and plot normalized price and return values

   Usage: python analyze.py <portfolio-value-file> <market-index-name>
                            <plot-file-name> <start-date> <end-date>
   
'''

import pandas as pd
from datetime import datetime, date, time, timedelta
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import argparse as ag

data_dir = '..//qstk//QSData//Yahoo'

def gen_fund_metrics(updated_df):
    '''
    Function to calculate metrics for a portfolio
    given net daily values of a portfolio

    args:
    updated_df(pandas dataframe): Dataframe with daily values
                                  of a portfolio

    except:
    None

    returns:
    std_rets(float): Standard deviation of daily returns
    mean_rets(float): Mean of daily returns
    sharpe(float): Sharpe ratio of the portfolio
    cum_ret(float): Maximum cumulative return of portfolio
    updated_df(pandas dataframe): Dataframe with daily portfolio
                                  value
    '''


    updated_df['norm_net_value'] = updated_df['net_value'] / updated_df.loc[updated_df.index.min(), 'net_value']
    updated_df['ret'] = ( updated_df['norm_net_value'] / updated_df['norm_net_value'].shift(1) ) - 1
    
    std_rets = updated_df['ret'].std()
    mean_rets = updated_df['ret'].mean()
    sharpe = mean_rets/std_rets * pow(252,0.5)
    cum_ret = updated_df.loc[updated_df.index.max(), 'norm_net_value']
    
    return std_rets, mean_rets, sharpe, cum_ret, updated_df


def gen_mkt_metrics(mkt_sym, start_date, end_date):
    '''
    Function to calculate market return metrics
    given a market symbol, start date and end date

    args:
    mkt_sym(str): Market index symbol
    start_date(datetime): Start date of calculation
    end_date(datetime): End date of calculation

    except:
    None

    returns:
    std_rets(float): Standard deviation of daily returns
    mean_rets(float): Mean of daily returns
    sharpe(float): Sharpe ratio of portfolio
    cum_ret(float): Maximum cumulative return of portfolio
    filt_df(pandas dataframe): Pandas dataframe with market data
    
    '''

    mkt_df = pd.read_csv(os.path.join(data_dir, '$SPX.csv'))
    mkt_df['Date'] = pd.to_datetime(mkt_df['Date'], format='%Y-%m-%d')
    mkt_df['Date'] = mkt_df['Date'].dt.date
    filt_df = mkt_df[(mkt_df['Date'] >= start_date) & (mkt_df['Date'] <= end_date)]
    filt_df = filt_df.set_index('Date')
    cols = filt_df.columns
    cols = [ val.strip() for val in cols ]
    filt_df.columns = cols
    filt_df = filt_df['Adj Close'].sort_index().to_frame()
    filt_df['norm_close'] = filt_df['Adj Close'] / filt_df.loc[filt_df.index.min(), 'Adj Close']
    filt_df['ret'] = (filt_df['norm_close']/ filt_df['norm_close'].shift(1)) - 1

    std_rets = filt_df['ret'].std()
    mean_rets = filt_df['ret'].mean()
    sharpe = mean_rets/std_rets * pow(252,0.5)
    cum_ret = filt_df.loc[filt_df.index.max(), 'norm_close']

    return std_rets, mean_rets, sharpe, cum_ret, filt_df

def plot_values(values, plotfile):
    '''
    Script to plot returns and prices of portfolio vs. market

    args:
    values(pandas dataframe): Pandas dataframe with portfolio and market
                              data
    plotfile(plot file name): File name to hold plot figures

    except:
    None

    returns:
    None
    
    '''
     
    fig, axes = plt.subplots(2,1, figsize=(10,10))
    plt.subplots_adjust(hspace=0.4)
    values[['Fund Daily Returns', 'Market Daily Returns']].plot(grid=True, ax=axes[0]).set_title('Fund Daily Returns vs. Market Daily Returns')   
    values[['Fund Value', 'Market Value' ]].plot(grid=True, ax=axes[1]).set_title('Fund Value vs. Market Value')
    plt.savefig(plotfile)

if __name__ == '__main__':
    parser = ag.ArgumentParser()
    parser.add_argument('valuefile', help="Portfolio Value File", type=str)
    parser.add_argument('marketsym', help="Market Symbol", type=str)
    parser.add_argument('plotfile', help="Plot File", type=str)
    parser.add_argument('startdate', help="Start date", type=str)
    parser.add_argument('enddate', help="End date", type=str)
    args = parser.parse_args()

    valuefile = args.valuefile
    mkt_sym = args.marketsym
    plotfile  = args.plotfile + '.pdf'
    start_date = datetime.strptime(args.startdate, '%Y%m%d').date()
    end_date = datetime.strptime(args.enddate, '%Y%m%d').date()

    fund_df = pd.read_csv(valuefile)
    fund_df = fund_df.drop([0]).set_index('Date')
    std_rets, mean_rets, sharpe, cum_rets, fund_df = gen_fund_metrics(fund_df)
    
    print("Fund - Standard Deviation of Daily Returns : {}".format(std_rets))
    print("Fund - Mean of Daily Returns : {}".format(mean_rets))
    print("Fund - Sharpe Ratio : {}".format(sharpe))
    print("Fund - Total Fund Return : {}".format(cum_rets))
                      
    std_rets, mean_rets, sharpe, cum_ret, mkt_df = gen_mkt_metrics(mkt_sym, start_date, end_date)
    print("Market - Standard Deviation of Daily Returns : {}".format(std_rets))
    print("Market - Mean of Daily Returns : {}".format(mean_rets))
    print("Market - Sharpe Ratio : {}".format(sharpe))
    print("Market - Total Market Return : {}".format(cum_ret))

    fund_df = fund_df.reset_index()
    fund_df['Date'] = pd.to_datetime(fund_df['Date'])

    mkt_df = mkt_df.reset_index()
    mkt_df['Date'] = pd.to_datetime(mkt_df['Date'])
    
    values = pd.merge(fund_df, mkt_df, on='Date')
    values = values[['Date', 'norm_net_value', 'norm_close', 'ret_x', 'ret_y']]
    values.columns= ['Date', 'Fund Value', 'Market Value', 'Fund Daily Returns', 'Market Daily Returns']
    values = values.set_index('Date')
    values.to_csv('values.csv', index=True)

    plot_values(values, plotfile)


