import config
import requests
import pandas as pd
import csv
import os
from datetime import datetime, date, timedelta

class Base:

    def __init__(self):
        self.api_config = config.get_idex_api_config()
        self.configs = config.get_config()

    def request_currencies(self, persisted=True):
        r1 = requests.post(self.api_config['returnCurrencies'])
        # print r1.status_code
        # print result_dict.keys()

        result_dict = r1.json()
        flat_dict = []
        for key, value in result_dict.iteritems():
            value['index'] = key
            flat_dict.append(value)

        if persisted:
            file = self.configs['cc_csv_today']
            file_path = config.get_day_path() + file

            # print file_path
            # print flat_dict

            self.WriteDictToCSV(file_path,self.configs['CC_COLUMNS'], flat_dict)

        return pd.DataFrame(flat_dict)

    def request_ticker(self):
        r1 = requests.post(self.api_config['returnTicker'])
        return r1.json()

    def get_market_ticker(self, coin):
        r = requests.post(self.api_config['returnTicker'],
                            json={"market": 'ETH_' + coin}
                        )
        return r.json()

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
    base_obj = Base()
    # r = base_obj.request_ticker()
    # print r

    result = base_obj.get_market_ticker('COU')
    print result
