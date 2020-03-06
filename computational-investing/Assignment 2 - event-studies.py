'''
   Script to get count of events for a set of symbols 
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
    
    df_close = d_data['close']
    print("Finding Events")

    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    for s_sym in ls_symbols:
         df_events[s_sym] = np.where((df_events[s_sym].shift(1) >= 10.0) & (df_events[s_sym] < 10.0), 1, 0)   
                
    return df_events


if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = utils.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    print("Developed timestamps")

    ls_symbols = utils.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')
    print("Developed Symbol list")

    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'adj close']
    ldf_data = utils.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events = find_events(ls_symbols, d_data)

    event_count = utils.event_profiler(df_events, i_lookback=20, i_lookforward=20, b_market_neutral=True, s_market_sym='SYM')
    print("No. of events : {}".format(event_count))
