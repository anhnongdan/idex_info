from Base import Base
import pandas as pd

class NewCurrency(Base):

    def __init__(self):
        Base.__init__(self)

    def get_new_listed_cc(self, cc_df, last_cc):
        last_cc['old'] = 1
        new_cc = pd.merge(cc_df, last_cc[['index', 'old']], left_on='index', right_on='index', how='outer')
        return new_cc[new_cc['old'] != 1]

    def get_new_coin_volume(self, new_cc):
        result = []
        for coin in new_cc['index']:
            r = self.get_market_ticker(coin)
            r['index'] = coin
            result.append(r)

        result_cols = ['baseVolume', 'percentChange','high', 'low', 'highestBid', 'quoteVolume']
        result_pd = pd.DataFrame(result)

        # print result_pd

        for rcol in result_cols:
            result_pd[result_pd['high'] == 'N/A'].loc[:, rcol] = '-1'
            # result_pd[result_pd['low'] == 'N/A'].loc[:, 'low'] = '-1'
            # result_pd[result_pd['highestBid'] == 'N/A'].loc[:, 'highestBid'] = '-1'
            # result_pd[rcol] = result_pd[rcol].astype(float)
            pass

        result_pd = result_pd.sort_values(by=['baseVolume'], ascending=False)

        result_cols.append('index')
        print result_cols
        result_pd = result_pd[result_cols]
        return result_pd

if __name__ == '__main__':
    base_obj = NewCurrency()
    # r = base_obj.request_ticker()
    # print r

    result = base_obj.get_market_ticker('COU')
    print result
