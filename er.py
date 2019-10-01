from pymongo import MongoClient
import pymongo
import numpy as np
import datetime
from tickers import tickers


def report(arr):
    _arr = sorted(arr, key = lambda x: x['date'])
    madeLine = False
    for r in _arr:
        earnings_date = str(r['date'])
        earnings_date_dt = datetime.datetime.strptime(earnings_date, "%Y-%m-%d 00:00:00")
        today_dt = datetime.datetime.now()
        if earnings_date_dt > today_dt and madeLine == False:
            print("   --------------------------------")
            madeLine = True
        market_cap = str(r['market-cap'])
        vds = ""
        for vol in r['vol_data']:
            vd = "{}={:<10} ".format(vol['d'], vol['be'])
            vds = vds + vd

        ans = "   {:<8}{:<22}{:<11}{:<30}{:<10}".format(
            r['ticker'], 
            earnings_date, 
            market_cap, 
            r['sector'],
            vds 
            )
        print(ans)

def get_straddle_vols(conn, ticker):
    collection = conn.database.straddles
    dates = [ datetime.datetime.strptime(x, "%Y-%m-%d") for x in collection.distinct("time_stamp", {'ticker': ticker})]
    arr = []
    try:
        max_date = datetime.datetime.strftime(max(dates), "%Y-%m-%d")
        vols = collection.find({'ticker': ticker, 'time_stamp': max_date})
        for item in vols:
            if item['days_to_expiration'] < 30 and item['type'] == 'put-in-the-money':
                arr.append({
                    'd': item['days_to_expiration'],
                    'be': item['be']
                })
    except:
        return []
    return arr


if __name__ == '__main__':
    print('hello earnings report')
    time_stamps = []
    conn = MongoClient()
    db = conn.database
    collection = db.basic_data
    arr = []
    for ticker in tickers:
        r = collection.find({'ticker': ticker}).sort([('earnings-date-iso', -1)]).limit(0)[0]
        if 'sector' not in r:
            r['sector'] = 'None'

        if not r['earnings-date-iso'] in [None, '']:
            vol_data = get_straddle_vols(conn, r['ticker'])
            arr.append({
                'ticker': r['ticker'], 
                'date':r['earnings-date-iso'], 
                'sector': r['sector'],
                'market-cap': r['market-cap'],
                'vol_data': vol_data
                })
    report(arr)


