import config
import requests
import pandas as pd
import csv
import os
from datetime import datetime, date, timedelta

class CMCBase:

    def __init__(self):
        self.api_config = config.get_cmc_api_config()
        self.configs = config.get_config()

    def request_currencies(self, persisted=True):
        r1 = requests.get(self.api_config['returnCurrencies'])

        result_dict = r1.json()['data']

        if persisted:
            file = self.configs['cc_csv_today']
            file_path = config.get_day_path() + file

            # print file_path
            # print flat_dict

            self.WriteDictToCSV(file_path,self.configs['CC_COLUMNS'], result_dict)

        return pd.DataFrame(result_dict)

    def request_ticker(self, convert='USD'):
        '''
        convert either USD or ETH, BTC, EUR, etc.
        '''
        # print self.api_config['returnTicker'].format(convert)
        r1 = requests.get(self.api_config['returnTicker'].format(convert))
        ticker = r1.json()['data']
        return pd.DataFrame(ticker)

    def get_coin_ticker(self, coin_id, convert='USD'):
        r = requests.get(self.api_config['returnCoinTicker'].format(coin_id, convert))
        mt = r.json()['data']
        return pd.DataFrame(mt)

    def ReadCSVasDict(self, csv_file, csv_columns=[]):
        try:
            with open(csv_file) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    print row[csv_columns[0]], row[csv_columns[1]], row[csv_columns[2]]
        except IOError as (errno, strerror):
                print("I/O error({0}): {1}".format(errno, strerror))
        return

    def WriteDictToCSV(self, csv_file,csv_columns,dict_data):
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in dict_data:
                    writer.writerow(data)
        except IOError as (errno, strerror):
                print("I/O error({0}): {1}".format(errno, strerror))
        return

if __name__ == '__main__':
    base_obj = CMCBase()
    # r = base_obj.request_ticker()
    # print r

    # result = base_obj.get_market_ticker('COU')
    #
    # result = base_obj.request_currencies(persisted=False)
    result = base_obj.get_coin_ticker(1)
    result.to_csv('test_cmc_coin.csv')
    print result
