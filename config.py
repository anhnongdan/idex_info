import requests
import pandas as pd
import csv
import os
from datetime import datetime, date, timedelta


def get_config():
    return {
        'new_cc_csv_today' : 'new_cc_{}.csv'.format(datetime.now().strftime('%H%M%S')),
        'cc_csv_today': 'currencies_{}.csv'.format(datetime.now().strftime('%H%M%S')),
        'CC_COLUMNS' : ['index', 'decimals', 'name', 'address'],
        'STARED' : ['WEL', 'EDR', 'CNN', 'IVN', 'ZCO', 'COIN'],
        'DATA_PATH' : '/data/{}/'
    }

def get_idex_api_config():
    url_base = 'https://api.idex.market/'

    return {
        'returnCurrencies' : url_base + 'returnCurrencies',
        'returnTicker' : url_base + 'returnTicker'
    }

def get_cmc_api_config():
    url_base =  'https://api.coinmarketcap.com/v2/'

    return {
        'returnCurrencies' : url_base + 'listings',
        'returnTicker' : url_base + 'ticker/?convert={}',
        'returnCoinTicker' : url_base + 'ticker/{}/?convert={}'
    }

def get_day_path(dstr=''):
    if dstr == '':
        dstr = date.today().strftime('%Y%m%d')

    currentPath = os.getcwd()
    csv_file = currentPath + get_config()['DATA_PATH'].format(dstr)

    if not os.path.exists(csv_file):
        os.makedirs(csv_file)

    return csv_file

def get_new_today_cc_path():
    file = get_config()['new_cc_csv_today'].format(datetime.now().strftime('%H%M%S'))
    file_path = get_day_path() + file
    return file_path

if __name__ == "__main__":
    print get_config()
    print get_idex_api_config()
    print get_day_path()
