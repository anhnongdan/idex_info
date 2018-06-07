import requests
import pandas as pd
import csv
import os

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

r1 = requests.post('https://api.idex.market/returnCurrencies')


# print r1.status_code
# print result_dict.keys()

result_dict = r1.json()
flat_dict = []
for key, value in result_dict.iteritems():
    value['index'] = key
    flat_dict.append(value)

# print flat_dict


currentPath = os.getcwd()
csv_file = currentPath + "/20180606/currencies.csv"

print csv_file
csv_columns = ['index', 'decimals', 'name', 'address']
WriteDictToCSV(csv_file,csv_columns,flat_dict)

# ReadCSVasDict(csv_file, csv_columns)

STARED = ['WEL', 'EDR', 'CNN', 'IVN', 'ZCO', 'COIN']


cc_df = pd.read_csv(csv_file)
print cc_df.count()
# print cc_df

# print cc_df[cc_df['index'].isin(STARED)]
stared_cc = cc_df[cc_df['index'].isin(STARED)]
