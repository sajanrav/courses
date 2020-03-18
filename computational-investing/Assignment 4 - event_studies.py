'''
   Script to generate order file for a set of symbols
   based on a specific event
'''

import pandas as pd
import numpy as np
import math
import copy
import datetime as dt

import utils

def find_events(ls_symbols, d_data):
    '''
    Function to create a dataframe of events
    for a set of symbols

    args:
    ls_symbols(list): List of symbols
    d_data(dict): Dictionary of dataframes with keys - OHLCVA

    except:
    None

    returns:
    df_events(pandas dataframe): Pandas dataframe with events for
                                 a specific set of symbols

    '''

    orders = pd.DataFrame(columns=['Year', 'Month', 'Day', 'Symbol', 'Type', 'Shares'])
    sym_close = d_data['close']
    print("Finding Events")

    ldt_timestamps = sym_close.index

    for s_sym in ls_symbols:
        for i in range(0, len(ldt_timestamps)):
            sym_cl_today = sym_close[s_sym].loc[ldt_timestamps[i]]
            sym_cl_yest  = sym_close[s_sym].loc[ldt_timestamps[i-1]]
          
            if sym_cl_yest >= 10.0 and sym_cl_today < 10.0:
                buy_dt  = ldt_timestamps[i].date()
                sell_dt = utils.get_next_bday(buy_dt, 5)
                if sell_dt > ldt_timestamps[len(ldt_timestamps) - 1]:
                    sell_dt = ldt_timestamps[len(ldt_timestamps) - 1]
                    
                buy_order = [ buy_dt.year, buy_dt.month, buy_dt.day, s_sym, 'Buy', 100]
                sell_order = [ sell_dt.year, sell_dt.month, sell_dt.day, s_sym, 'Sell', 100]
                orders.loc[len(orders)] = buy_order
                orders.loc[len(orders)] = sell_order
                
    return orders.sort_values(['Year', 'Month', 'Day'], ascending=True)


if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = utils.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    print("Developed timestamps")

    ls_symbols = utils.get_symbols_from_list('sp5002012')
    ls_symbols.append('$SPX')
    print("Developed Symbol list")

    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'adj close']
    ldf_data = utils.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    orders_df = find_events(ls_symbols, d_data)
    orders_df.to_csv('orders_10.csv', index=False)
