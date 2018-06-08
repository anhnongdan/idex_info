import requests
import pandas as pd
import csv
import os
from datetime import datetime, date, timedelta
import config


CC_COLUMNS = ['index', 'decimals', 'name', 'address'],
STARED = ['WEL', 'EDR', 'CNN', 'IVN', 'ZCO', 'COIN'],

def get_day_path(dstr=''):
    if dstr == '':
        dstr = date.today().strftime('%Y%m%d')

    currentPath = os.getcwd()
    csv_file = currentPath + "/{}/".format(dstr)

    if not os.path.exists(csv_file):
        os.makedirs(csv_file)

    return csv_file


def ReadCSVasDict(csv_file, csv_columns=[]):
    try:
        with open(csv_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print row[csv_columns[0]], row[csv_columns[1]], row[csv_columns[2]]
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
    return

def WriteDictToCSV(csv_file,csv_columns,dict_data):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
    return

# r = requests.post('https://api.idex.market/returnTicker',
#                     json={"market": "ETH_EVN"}
#                 )
#
#
# print r.status_code
# print r.json()
# print r.text

def request_currencies_persisted():
    r1 = requests.post('https://api.idex.market/returnCurrencies')
    # print r1.status_code
    # print result_dict.keys()

    result_dict = r1.json()
    flat_dict = []
    for key, value in result_dict.iteritems():
        value['index'] = key
        flat_dict.append(value)

    file = 'currencies_{}.csv'.format(datetime.now().strftime('%H%M%S'))
    file_path = get_day_path() + file

    WriteDictToCSV(file_path, CC_COLUMNS, flat_dict)
    return file_path
    # print flat_dict

def get_new_listed_cc(cc_df, last_cc):
    last_cc['old'] = 1
    new_cc = pd.merge(cc_df, last_cc[['index', 'old']], left_on='index', right_on='index', how='outer')
    return new_cc[new_cc['old'] != 1]



#
# print csv_file
# csv_columns = ['index', 'decimals', 'name', 'address']
# WriteDictToCSV(csv_file,csv_columns,flat_dict)

# ReadCSVasDict(csv_file, csv_columns)
new_file = request_currencies_persisted()
cc_df = pd.read_csv(new_file)
# print cc_df.count()
# print cc_df

# print cc_df[cc_df['index'].isin(STARED)]
# stared_cc = cc_df[cc_df['index'].isin(STARED)]
last_csv = get_day_path(dstr='20180608') + "currencies_001952.csv"
last_cc = pd.read_csv(last_csv)
# print last_cc

new_cc = get_new_listed_cc(cc_df, last_cc)

file = 'new_cc_{}.csv'.format(datetime.now().strftime('%H%M%S'))
file_path = get_day_path() + file
new_cc.to_csv(file_path)

print "##############$$$$$$$$$$$$$$###################"
print cc_df.count()
print last_cc.count()
print new_cc
# print new_cc
