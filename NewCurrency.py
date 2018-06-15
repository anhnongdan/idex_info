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

        result_cols = ['index', 'baseVolume', 'percentChange','high', 'low', 'highestBid', 'quoteVolume']
        result_pd = pd.DataFrame(result)
        result_pd[result_pd['high'] == 'N/A'] = '-1'
        result_pd[result_pd['low'] == 'N/A'] = '-1'
        result_pd[result_pd['highestBid'] == 'N/A'] = '-1'

        for col in result_cols:
            if col == 'index':
                continue
            result_pd[col] = result_pd[col].astype(float)

        result_pd = result_pd.sort_values(by=['baseVolume'], ascending=False)
        result_pd = result_pd[result_cols]
        return result_pd

if __name__ == '__main__':
    base_obj = NewCurrency()
    # r = base_obj.request_ticker()
    # print r

    result = base_obj.get_market_ticker('COU')
    print result
