'''
   Script to calculate daily portfolio values from
   a given order file

   Usage : python marketsim.py <order-file> <investment> <portfolio-value-file>
   
'''

import pandas as pd
from datetime import datetime, date, time, timedelta
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import argparse as ag

data_dir   = '../qstk/QSData/Yahoo'

def gen_order_facts(order_file):
    '''
    Function to calculate market order facts
    from a given order file

    args:
    order_file(str): Name of order file

    except:
    None

    returns:
    orders(dict): Dictionary with market orders
    all_syms(list): List of all symbols in the order file
    start_date(datetime): Start date from which daily portfolio value is
                          to be calculated
    end_date(datetime): End date upto which daily portfolio value is to
                        be calculated

    '''
    
    all_syms = []
    with open(order_file, 'r') as f:
        reader = csv.reader(f)
        orders = []
        for row in reader:
            order = {}
            order['dt'] = datetime.strptime(row[0] + '-' + [ row[1] if int(row[1]) >= 10 else "0" + row[1] ][0] + '-' + row[2], 
                                            '%Y-%m-%d')
            order['sym'] = row[3]
            order['type'] = row[4]
            order['shares'] = int(row[5])
            orders.append(order)
            all_syms.append(order['sym'])

    all_syms = list(set(all_syms))
    start_date = orders[0]['dt']
    end_date   = orders[-1]['dt'] + timedelta(days=1)
    
    return orders, all_syms, start_date, end_date


def gen_price_df(all_syms, start_date, end_date):
    '''
    Function to create dataframe with adjusted closes
    of a list of symbols for a given start date and
    end date

    args:
    all_syms(list): List of symbols
    start_date(datetime): Start date for adjusted price
                          data generation
    end_date(datetime): End date for adjusted price data
                        generation

    except:
    None

    returns:
    closes(pandas dataframe): Pandas dataframe with adjusted
                              close value for a given list of
                              symbols
    '''
    
    closes = pd.DataFrame()
    for sym in all_syms:
        price_df = pd.read_csv(os.path.join(data_dir, sym + '.csv'))
        cols = price_df.columns
        cols = [ val.strip() for val in cols ]
        price_df.columns = cols
        price_df['Date'] = pd.to_datetime(price_df['Date'], format='%Y-%m-%d')
        filt_df = price_df[(price_df['Date'] >= start_date) & (price_df['Date'] <= end_date)]
        filt_df = filt_df.set_index('Date')
        closes = pd.concat([closes, filt_df['Adj Close']], axis=1)

    closes.columns = all_syms
    
    return closes

def init_ds(all_syms, start_date, end_date):
    '''
    Function to initialize output dataframe

    args:
    all_syms(list): List of symbols
    start_date(datetime): Start date of daily portfolio value
                          calculation
    end_date(datetime): End date of daily portfolio value
                        calculation

    except:
    None

    returns:
    portfolio_df(pandas dataframe): Pandas dataframe with output
                                    dataframe structure

    '''

    dates = pd.bdate_range(start_date, end_date)
    portfolio_df = pd.DataFrame({'Date': dates})
    portfolio_df['cash_chg'] = [0] * len(portfolio_df)
    for sym in all_syms:
        portfolio_df[sym] = [0] * len(portfolio_df)
    
    return portfolio_df


def find_close(sym, dt, closes):
    '''
    Function to find adjusted close of a given symbol
    on a specific date

    args:
    sym(str): Symbol name
    dt(dateime): Date for which adjusted close is to be
                 identified
    closes(pandas dataframe): Pandas dataframe with adjusted
                              close value for a set of symbols

    except:
    None

    returns:
    type(float): Adjusted close value for a given date and symbol

    '''
    
    return closes.loc[dt, sym]


def apply_holdings(x, orders, closes):
    '''
    Function to calculate change in cash value and
    no. of shares for a given day if order is present

    args:
    x(pandas dataframe row): A row of a pandas dataframe
    orders(dict): Dictionary with order data
    closes(pandas dataframe): Pandas dataframe with adjusted closes
                              for a list of symbols

    except:
    None

    returns:
    x(pandas dataframe row): Row with updated values for portfolio

    '''
    
    for val in orders:
        if val['dt'] == x['Date']:
            if val['type'] == 'Buy':
                x[val['sym']] += val['shares']
                x['cash_chg'] += val['shares'] * find_close(val['sym'], val['dt'], closes) * (-1)
            else:
                x[val['sym']] += val['shares'] * (-1)
                x['cash_chg'] += val['shares'] * find_close(val['sym'], val['dt'], closes)
    return x


def update_portfolio_df(portfolio_df, orders, closes, initial):
    '''
    Function to update portfolio dataframe

    args:
    portfolio_df(pandas dataframe): Pandas dataframe to hold daily
                                    portfolio values
    orders(dict): Dictionary with all order data
    closes(pandas dataframe): Pandas dataframe with daily adjusted
                              closes for a list of symbols
    initial(float): Initial investment

    except:
    None

    returns:
    updated_df(pandas dataframe): Pandas dataframe with updated daily
                                  portfolio values

    '''

    portfolio_df = portfolio_df[portfolio_df['Date'].isin(closes.index.tolist())]
    portfolio_df = portfolio_df.apply(apply_holdings, args=(orders,closes) , axis=1)
    cols = portfolio_df.columns
    for col in cols[1:]:
        portfolio_df[col] = portfolio_df[col].shift(1)
        
    portfolio_df = portfolio_df.fillna(0)
    for col in cols[2:]:
        portfolio_df[col] = portfolio_df[col].cumsum()
    
    actual_prices = portfolio_df.set_index('Date').iloc[:, 1:] * closes
    
    new_cols = [ val for val in cols if val not in all_syms + ['Date'] ]
    updated_df = pd.concat([portfolio_df.set_index('Date').loc[:, new_cols], actual_prices], axis=1)
    updated_df['cash_balance'] = updated_df['cash_chg'].cumsum() + initial
    updated_df['net_value'] = updated_df.drop(['cash_chg'], axis=1).apply(lambda x: x.sum(), axis=1)
    
    return updated_df
    
def main():
    parser = ag.ArgumentParser()
    parser.add_argument('orderfile', help='Order file name', type=str)
    parser.add_argument('investment', help='Initial investment', type=str)
    parser.add_argument('valuefile', help='Output file with portfolio value', type=str)
    args = parser.parse_args()

    order_file = args.orderfile
    initial    = args.investment
    value_file = args.valuefile
    
    orders, all_syms, start_date, end_date = gen_order_facts(order_file)
    closes = gen_price_df(all_syms, start_date, end_date)
    portfolio_df = init_ds(all_syms, start_date, end_date)
    updated_df = update_portfolio_df(portfolio_df, orders, closes, initial)
    updated_df.index.name = 'Date'
    updated_df.to_csv(value_file, index=True)


