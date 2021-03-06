from Base import Base
from NewCurrency import NewCurrency
import pandas as pd
#pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

import config


base_info = Base()
new_cc = NewCurrency()

# ReadCSVasDict(csv_file, csv_columns)
# new_file = base_info.request_currencies_persisted()
# cc_df = pd.read_csv(new_file)
cc_df = base_info.request_currencies(persisted = True)
# print cc_df.count()
# print cc_df

# print cc_df[cc_df['index'].isin(STARED)]
# stared_cc = cc_df[cc_df['index'].isin(STARED)]
last_csv = config.get_day_path(dstr='20180801') + "currencies_222515.csv"
last_cc = pd.read_csv(last_csv)
# print last_cc

new_list = new_cc.get_new_listed_cc(cc_df, last_cc)

if len(new_list.index > 0):
    new_info = new_cc.get_new_coin_volume(new_list)
    new_file_path = config.get_new_today_cc_path()
    new_info.to_csv(new_file_path)

    print "############## NEW LISTED ###################"
    print new_list
    print new_info

print "##############$$$$$$$$$$$$$$###################"
print cc_df.count()
print last_cc.count()
