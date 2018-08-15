from __future__ import division
from Base import Base
from NewCurrency import NewCurrency
import pandas as pd
#pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
from datetime import date, datetime, timedelta

import config

# class Analytics():

def find_0_gaps_max_incr_analysis(hourly_vol, hourly_max, hourly_min, adj_look_back=10, adj_vol_incr=10, price_max_incr=30, adj_next=24):
    result = {}
    steps = 0
    incr_steps = 0
    decr_steps = 0
    up_decr_steps = 0
    incr_total = 0
    decr_total = 0
    next_total_vol = 0
    down_trend = 0

    ## hourly index is increased with time
    for i in range(len(hourly_vol)-1, 10, -1):
        steps += 1

        ## should it be (i+1) or i?
        last_10 = hourly_vol[(i-adj_look_back):i].sum()
        next_max = hourly_max[i+1:(i+adj_next)].max()
        next_min = hourly_min[i+1:(i+adj_next)].min()
        next_vol = hourly_vol[i+1:(i+adj_next)].sum()
        if hourly_vol[i] > adj_vol_incr*last_10:

#             print "{}: {}".format(hourly_vol.index[i], hourly_vol[i])
#             print 'beat: ',last_10
            if hourly_max[i] == 0 or next_max == 0:
                continue

            incr_price = 100*(next_max/hourly_max[i]) - 100
            if incr_price > price_max_incr:
#                 print "{} next: {} | now: {} | incr: {}".format(hourly_vol.index[i], next_max, hourly_max[i], incr_price)
                incr_steps += 1
                incr_total += incr_price
                next_total_vol += next_vol
                continue

            # @TODO: should this be next_min or next_max??
            desc_price = 100*(next_max/hourly_max[i]) - 100
            if desc_price < -0.5*price_max_incr:
#                 print "{} next: {} | now: {} | descr: {}".format(hourly_vol.index[i], next_max, hourly_max[i], incr_price)
                decr_steps += 1
                decr_total += desc_price

                up_decr_steps += 1
                ## detect and avoid down trend (testing)
                ## this if is just for easy reading
                if hourly_max[i] <= hourly_min[i-1]:
                    up_decr_steps -= 1


#     print '****** Final result *******'
#     print "arg adj_look_back={}, adj_vol_incr={}, price_max_incr={}, adj_next = {}".format(adj_look_back, adj_vol_incr, price_max_incr, adj_next)
#     print steps, incr_steps, decr_steps
#     print "Incresed steps: {}".format(incr_steps/steps)
#     print "Decrease steps: {}".format(decr_steps/steps)

    if steps == 0:
        in_ratio = 0
        de_ratio = 0
    else:
        in_ratio = incr_steps/steps
        de_ratio = decr_steps/steps

    if incr_steps == 0:
        incr_avg = 0
        avg_incr_vol = 0
    else:
        incr_avg = incr_total/incr_steps
        avg_incr_vol = next_total_vol/incr_steps

    if decr_steps == 0:
        decr_avg = 0
    else:
        decr_avg = decr_total/decr_steps

    result['adj_look_back'] = adj_look_back
    result['adj_vol_incr'] = adj_vol_incr
    result['price_max_incr'] = price_max_incr
    result['adj_next'] = adj_next
    result['steps'] = steps
    result['increase'] = in_ratio
    result['decrease'] = de_ratio
    result['incr_total'] = incr_total
    result['decr_total'] = decr_total
    result['incr_avg'] = incr_avg
    result['decr_avg'] = decr_avg
    result['avg_incr_vol'] = avg_incr_vol
    result['up_decr_ratio'] = up_decr_steps/steps
#     print 'return result: ', result

    return result

def back_test_time_segment_volume_analysis(base_obj, coin, args):
#     base_obj = Base()
    # r = base_obj.request_ticker()
    # print r

    dag_hist = base_obj.get_trade_history(coin)
    dag_dt = prepare_trade_history_time_line(dag_hist)
    # dag_dt = filter_price_out_lier(dag_dt)
    dag_dt.index = dag_dt['dt']

    seg1 = int(len(dag_dt)/3)
    seg2 = 2*seg1
    print seg1, seg2
    hourly_vols = []
    hourly_maxs = []
    hourly_mins = []

    hourly_vols.append(dag_dt.iloc[:seg1]['total'].resample('1H').sum().fillna(0))
    hourly_vols.append(dag_dt.iloc[seg1:seg2]['total'].resample('1H').sum().fillna(0))
    hourly_vols.append(dag_dt.iloc[seg2:]['total'].resample('1H').sum().fillna(0))
    hourly_vols.append(dag_dt['total'].resample('1H').sum().fillna(0))

    ## Actually, max min na should be filled with previous close price.
    hourly_maxs.append(dag_dt.iloc[:seg1]['price'].resample('1H').max().fillna(method='ffill'))
    hourly_maxs.append(dag_dt.iloc[seg1:seg2]['price'].resample('1H').max().fillna(method='ffill'))
    hourly_maxs.append(dag_dt.iloc[seg2:]['price'].resample('1H').max().fillna(method='ffill'))
    hourly_maxs.append(dag_dt['price'].resample('1H').max().fillna(method='ffill'))

    # dont' fillna to this
    # filling last min doesn't feel right.
    hourly_mins.append(dag_dt.iloc[:seg1]['price'].resample('1H').min().fillna(method='ffill'))
    hourly_mins.append(dag_dt.iloc[seg1:seg2]['price'].resample('1H').min().fillna(method='ffill'))
    hourly_mins.append(dag_dt.iloc[seg2:]['price'].resample('1H').min().fillna(method='ffill'))
    hourly_mins.append(dag_dt['price'].resample('1H').min().fillna(method='ffill'))

#     hourly_mins = dag_dt['price'].resample('1H').min()

    for time_seg in range(0, 4):
        result = []
        for arg in args:
    #         print arg
            rlt = find_0_gaps_max_incr_analysis(hourly_vols[time_seg], hourly_maxs[time_seg], hourly_mins[time_seg], adj_look_back=arg[0], adj_vol_incr =arg[1], price_max_incr =arg[2], adj_next =arg[3])
            result.append(rlt)

        rpd = pd.DataFrame(result)
        rpd['id_ratio'] = rpd['increase']/rpd['decrease']
        rpd['total_gain'] = rpd['incr_total'] + rpd['decr_total']
        print "********* {} seg: {} *********".format(coin.upper(), time_seg)
        final_result = rpd.sort_values('id_ratio', ascending=False).head(8)
        print final_result

        # return final_result

def prepare_trade_history_time_line(th_df):
    # print th_df['date']
    # print th_df.describe()
    # print th_df.info()

    # print th_df[['date', 'price', 'total', 'usdValue']]
    #

    # look at the chart to consider 'Swing interval'
    # 1 hr might be good, 2 hrs might be better.

    th_df['total'] = pd.to_numeric(th_df['total'])
    th_df['price'] = pd.to_numeric(th_df['price'])
    th_df['dt'] = pd.to_datetime(th_df.date, format="%Y-%m-%d %H:%M:%S")

    # convert from UTC to ICT
    th_df['dt'] +=  pd.to_timedelta(7, unit='h')

    th_df['bid_hour'] = th_df['dt'].dt.hour
    th_df['bid_minute'] = th_df['dt'].dt.minute
    th_df['bid_date'] = th_df['dt'].dt.strftime('%Y-%m-%d')

    # print hrs_count[hrs_count['bid_date'] == '2018-06-20' & hrs_count['bid_hour'] == 16]

    return th_df

def analyze_bid_price_slope(th_df):
    '''
    The price is heavily manipulated, so it's important to monitor the bid order book
    and spot the unreasonable bids.
    '''
    return

def get_volume_date_price(df, min_date, min_price):
    min_date = '2018-07-07 11:00:00'
    min_price = 0.000060

    return df[(df['dt'] >= min_date) & (df['price'] >= min_price)]['total'].sum()

def max_price_volume(threshold = 0.5):
    '''
    Return a meaningful max price value, consider volume larger than 0.5 ETH.
    This eliminate the outlier transaction when 0.15ETH is used to buy with ridiculously high price.

    ==>> shouldn't do this, better filter out outlier.
    '''

    return max_value

def filter_price_out_lier(hist):
    '''
    I better use daily average -> take 5 samples and remove BS values.
    '''
    ##hist has index reverse with time.
    drops = []
    i = 0
    while i < (len(hist)-4):
        if (hist.iloc[i+1].price + hist.iloc[i+2].price + hist.iloc[i+3].price ) > hist.iloc[i].price*50*3:
            print i+1, hist.iloc[i+1].date, hist.iloc[i+1].price
            i += 1
            drops.append(i)
            ##continue the trace, keep incr level at 25x
            while hist.iloc[i+1].price > hist.iloc[i].price*0.5 and i < len(hist)-2:
                print i+1, hist.iloc[i+1].date, hist.iloc[i+1].price
                i += 1
                drops.append(i)
            if i >= len(hist)-4:
                break
            # continue to avoid checking below condition
            # when the up trend end, the below condition is satisfied
        if (hist.iloc[i+1].price + hist.iloc[i+2].price + hist.iloc[i+3].price)*15 < hist.iloc[i].price*3:
            print i+1, hist.iloc[i+1].date, hist.iloc[i+1].price
            i += 1
            drops.append(i)
            ##continue the trace, keep incr level at ~1/9x
            while hist.iloc[i+1].price < hist.iloc[i].price*1.3 and i < len(hist)-2:
                print i+1, hist.iloc[i+1].date, hist.iloc[i+1].price
                i += 1
                drops.append(i)
            if i >= len(hist)-4:
                break
            ## leap through the end of down trend as well

            #avoid below +=1
            # continue

        #increase index when nothing happen
        i += 1

    proc_hist = hist
    return proc_hist.drop(hist.index[drops])


#### Utility functions
def generate_grid_search_params():
    adj_look_backs = [2, 4]
    adj_vol_incrs = [ 6, 12]
    price_max_incrs = [30, 50]
    adj_nexts = [10, 24]

    args_array = [adj_look_backs, adj_vol_incrs, price_max_incrs, adj_nexts]
    args = list(itertools.product(*args_array))

    return args

if __name__ == '__main__':
    base_info = Base()
    analyzer = Analytics()

    result = base_info.get_trade_history('NPXS')
    analyzer.analyze_trade_history_time_line(result)
