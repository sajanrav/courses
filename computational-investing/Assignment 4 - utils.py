'''
   Module with various utility functions
'''

import datetime as dt
from datetime import timedelta, date
import time as t
import numpy as np
import os
import pandas as pd
import copy

NYSE_DATES_FILE = 'NYSE_dates.txt'
SYMBOLS_FILE_DIR = '..\\qstk\\QSData\\Yahoo\\Lists'
SYMBOLS_DATA_DIR = '..\\qstk\\QSData\\Yahoo'

holidays = [ date(2008, 1, 1), date(2008, 1, 21), date(2008, 2, 18),
             date(2008, 3, 21), date(2008, 5, 26), date(2008, 7, 4),
             date(2008, 9, 1), date(2008, 11, 27), date(2008, 12, 25),
             date(2009, 1, 1), date(2009, 1, 19), date(2009, 2, 16),
             date(2009, 4, 10), date(2009, 5, 25), date(2009, 7, 3),
             date(2009, 9, 7), date(2009, 11, 26), date(2009, 12, 25) ]

def _cache_dates():
    '''
    Function to return a series of dates after reading from file.
    The dates are related to NYSE business days.

    args:
    None

    except:
    None

    returns:
    pd.Series(pandas series): Pandas series with NYSE business days
    '''
    
    try:
        filename = NYSE_DATES_FILE
    except KeyError:
        print("Please be sure you have NYSE_dates.txt in the current working directory")

    datestxt = np.loadtxt(filename, dtype=str)
    dates = []
    for i in datestxt:
        dates.append(dt.datetime.strptime(i, "%m/%d/%Y"))
    return pd.Series(index=dates, data=dates)

GTS_DATES = _cache_dates()

def getNYSEdays(startday = dt.datetime(1964,7,5), endday = dt.datetime(2020,12,31),
    timeofday = dt.timedelta(0)):
    '''
    Function to fetch NYSE business days

    args:
    startday(datetime): Start date to be considered
    endday(datetime): End date to be considered
    timeofday(timedelta): Delta in terms of hours

    except:
    None

    returns:
    ret(list): Dates of business days for NYSE

    '''
    
    start = startday - timeofday
    end = endday - timeofday

    dates = GTS_DATES[start:end]

    ret = [x + timeofday for x in dates]

    return ret

def get_symbols_from_list(sym_list):
    '''
    Function to fetch list of symbols from a symbol file

    args:
    sym_list(file): Text file with list of symbols

    except:
    None

    returns:
    ls_symbols(list): List of symbols

    '''

    ls_symbols = []
    full_path = os.path.join(SYMBOLS_FILE_DIR, sym_list + '.txt')
    f_in = open(full_path, 'r')
    for line in f_in.readlines():
        filtered = line[:-1]
        ls_symbols.append(filtered)

    f_in.close()

    return ls_symbols

def get_data (ts_list, symbol_list, data_item):
    '''
    Function to fetch price data for a given set of symbols,
    timestamps and fields ( OHLCVA )

    args:
    ls_list(list): List of timestamps
    symbol_list(list): List of symbols
    data_item(list): List of fields ( OHLCVA )

    except:
    None

    returns:
    retval(list): List of dataframes with OHLCVA data
                  for symbols
    '''
    
    ls_syms_copy = copy.deepcopy(symbol_list)
    start = t.time()
    retval = get_data_hardread(ts_list, symbol_list, data_item)
    elapsed = t.time() - start
    print("reading took {} seconds".format(str(elapsed)))

    if type(retval) == type([]):
        for i, df_single in enumerate(retval):
            retval[i] = df_single.reindex(columns=ls_syms_copy)
    else:
        retval = retval.reindex(columns=ls_syms_copy)

    return retval

def get_data_hardread(ts_list, symbol_list, data_item):
    '''
    Function to create list of dataframes with OHLCVA data
    for a list of symbols

    args:
    ts_list(list): List of timestamps
    symbol_list(list): List of symbols
    data_items(list): List of fields for each data is to be
                      fetched for each symbol

    except:
    None

    returns:
    all_stocks_data(list): List of dataframes with OHLCVA data

    '''
    
    all_stocks_data = []
    for item in data_item:
        master_df = pd.DataFrame()
        for sym in symbol_list:
            try:
                file_path = os.path.join(SYMBOLS_DATA_DIR, sym + '.csv')
                df = pd.read_csv(file_path)
                columns = df.columns
                columns = [ val.strip() for val in columns ]
                df.columns = columns
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.set_index('Date')
                item_df = df[(df.index >= ts_list[0]) & (df.index <= ts_list[-1])]
                master_df = pd.concat([master_df, item_df[item.title()]], axis=1)
            except:
                print("Failed to get data for Symbol : {}".format(sym))
                continue

        master_df.columns = symbol_list
        master_df = master_df.sort_index()
        all_stocks_data.append(master_df)

    return all_stocks_data

def event_profiler(df_events_arg, i_lookback=20, i_lookforward=20,
                   b_market_neutral=True, s_market_sym='SPY'):

    '''
    Function to calculate no. of events, given an event matrix

    args:
    df_events_arg(pandas dataframe): Event dataframe
    i_lookback(int): Backward lookback period
    i_lookback(int): Forward lookback period
    b_market_neutral(bool): Flag to indicate whether returns
                            should be market neutral
    s_market_sym(str): Name of symbol which represents market

    except:
    None

    returns
    i_no_events(int): Number of events

    '''

    df_events = df_events_arg.copy()
    if b_market_neutral == True:
        del df_events[s_market_sym]

    i_no_events = int(np.logical_not(np.isnan(df_events.values)).sum())

    return i_no_events


def is_holiday(dt):
    '''
    Function to check if a data is a holiday

    args:
    dt(datetime.date): Given data

    except:
    None

    returns:
    True/False(boolean): True if holiday else False

    '''
    
    if dt.weekday() == 5 or dt.weekday() == 6 or dt in holidays:
          return True
    else:
          return False

def get_next_bday(init_dt, offset):
    '''
    Function to get next business day, given a date and
    and offset

    args:
    init_dt(datetime.date): Given date
    offset(int): No. of days to be added to given date

    except:
    None

    returns:
    next_dt(datetime.date): Date after adding offset to
                            given date
    '''
    
    check = 0
    next_dt = init_dt
    while check < offset:
        next_dt = next_dt + timedelta(days=1)
        if is_holiday(next_dt) == False:
            check += 1

    return next_dt


