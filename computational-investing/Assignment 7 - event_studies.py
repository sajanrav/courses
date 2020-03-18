'''
   Script to generate order file using bollinger bands for a
   set of symbols
'''

import pandas as pd
import numpy as np
import math
import copy
import datetime as dt
import numpy as np
from datetime import date, timedelta

import utils


def find_events(ls_symbols, bb_bands):
    '''
    Function to create a dataframe of events
    for a set of symbols from bollinger band
    values

    args:
    ls_symbols(list): List of symbols
    bb_bands(pandas dataframe): Pandas dataframe with bollinger band
                                values for a set of symbols

    except:
    None

    returns:
    df_events(pandas dataframe): Pandas dataframe with events for
                                 a specific set of symbols calculated
                                 from Bollinger bands

    '''

    
    print("Finding Events")
 
    orders = pd.DataFrame(columns=['Year', 'Month', 'Day', 'Symbol', 'Type', 'Shares']) 
    bb_syms = bb_bands
    bb_mkt = bb_bands['$SPX']
    print("Finding Events")

    df_events = copy.deepcopy(bb_syms)
    df_events = df_events * np.NAN

    ldt_timestamps = bb_syms.index 

    for s_sym in ls_symbols: 
        for i in range(0, len(ldt_timestamps)):
            bb_sym_today = bb_syms[s_sym].loc[ldt_timestamps[i]]
            bb_sym_yest  = bb_syms[s_sym].loc[ldt_timestamps[i-1]]
            bb_mkt_today = bb_mkt.loc[ldt_timestamps[i]]

            if bb_sym_today < -2.0 and bb_sym_yest >= -2.0 and bb_mkt_today >= 1.4:
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

    bb_bands = utils.gen_bb_bands(ls_symbols, d_data['adj close'], 20, 1)
   
    order_df = find_events(ls_symbols, bb_bands)
    order_df.to_csv('order_test.csv', index=False)
    
