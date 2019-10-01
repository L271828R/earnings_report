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
        ans = "   {:<8}{:<22}{:<11}{}".format(
            r['ticker'], 
            earnings_date, 
            market_cap, 
            r['sector'])
        print(ans)


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
            arr.append({
                'ticker': r['ticker'], 
                'date':r['earnings-date-iso'], 
                'sector': r['sector'],
                'market-cap': r['market-cap'],
                })
    report(arr)


