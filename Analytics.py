from Base import Base
from NewCurrency import NewCurrency
import pandas as pd
#pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
from datetime import date, datetime, timedelta


import config

class Analytics():

    def analyze_trade_history_time_line(self, th_df):
        # print th_df['date']
        # print th_df.describe()
        print th_df.info()

        print th_df[['date', 'price', 'total', 'usdValue']]
        #
        # th_df['hist_hour'] = pd.to_datetime(th_df.timestamp)
        #
        # hrs_count = th_df.groupby('hist_hour').count()
        #
        # print hrs_count

        return th_df

    def analyze_bid_price_slope(self, th_df):
        '''
        The price is heavily manipulated, so it's important to monitor the bid order book
        and spot the unreasonable bids.
        '''
        return

if __name__ == '__main__':
    base_info = Base()
    analyzer = Analytics()

    result = base_info.get_trade_history('NPXS')
    analyzer.analyze_trade_history_time_line(result)
