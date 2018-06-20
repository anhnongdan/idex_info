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
        # print th_df.info()

        # print th_df[['date', 'price', 'total', 'usdValue']]
        #
        th_df['dt'] = pd.to_datetime(th_df.date, format="%Y-%m-%d %H:%M:%S")
        th_df['bid_hour'] = th_df['dt'].dt.hour
        th_df['bid_minute'] = th_df['dt'].dt.minute
        th_df['bid_date'] = th_df['dt'].dt.date

        hrs_count = th_df.groupby(['bid_date', 'bid_hour', 'bid_minute']).count()

        print  hrs_count.info()
        
        # print hrs_count[hrs_count['bid_date'] == '2018-06-20' & hrs_count['bid_hour'] == 16]

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
