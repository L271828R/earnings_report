from pymongo import MongoClient
import pymongo
import numpy as np
import datetime
from tickers import tickers


def report(arr, param=None):
    _arr = None
    print('param=x', param)
    if param is None:
        _arr = sorted(arr, key = lambda x: x['date'])
    if param == 'sorted':
        _arr = sorted(arr, key = lambda x: x['front'])

    # print(_arr)
    madeLine = False
    for index, r in enumerate(_arr):
        earnings_date = str(r['date'])
        earnings_date_dt = datetime.datetime.strptime(earnings_date, "%Y-%m-%d 00:00:00")
        today_dt = datetime.datetime.now()
        if earnings_date_dt > today_dt and madeLine == False and param is None:
            print("   --------------------------------")
            madeLine = True
        market_cap = str(r['market-cap'])
        vds = ""
        for vol in r['vol_data']:
            vd = "{}={:<10} ".format(vol['d'], vol['be'])
            vds = vds + vd

        has_note = ""
        if r['has_note']:
            has_note = ">"

        ans = "{:<5}   {:<1}{:<8}{:<22}{:<11}{:<30}{:<10}".format(
            index,
            has_note,
            r['ticker'], 
            earnings_date, 
            market_cap, 
            r['sector'],
            vds 
            )
        try:
            if param is not None and r['vol_data'][0]['d'] > 11:
                pass
            else:
                print(ans)
        except:
            pass
    return _arr

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

def save_note(conn, obj):
    conn.database.earnings_notes.save(obj)
    return True

def edit_screen(conn, arr):
    print('\r\n edit screen...')
    ans = int(input("enter id for earnings change"))
    print("")
    ticker = arr[ans]['ticker']
    print('entering for ', ticker)
    print("")
    date = input('enter the date for earnings "yyyy-mm-dd"')
    percent_change_after_eod = input("enter the percent change at EOD")
    percent_change_straddle = input("percent impact on straddle")
    percent_expected_straddle = input("percent expected on straddle")
    percent_expected_days_for_straddle = input("percent expected days on straddle")
    print('')
    print('')
    print('summary:')
    note = f"expected={percent_expected_straddle} for {percent_expected_days_for_straddle} days actual={percent_change_after_eod}={percent_change_straddle}"
    print(date, ticker, note)
    ans = input('correct? [Y]es [N]o').lower()
    obj = {
        'date':datetime.datetime.strptime(date, '%Y-%m-%d'),
        'ticker': ticker,
        'percent_change_after_eod': percent_change_after_eod,
        'percent_change_straddle': percent_change_straddle,
        'percent_expected_straddle': percent_expected_straddle,
        'percent_expected_days_for_straddle': percent_expected_days_for_straddle,
        'note': note
    }
    if ans == 'y':
        save_note(conn, obj)

def get_tickers_with_notes(conn):
    return conn.database.earnings_notes.distinct('ticker')


def show_notes(conn, ticker):
    notes = conn.database.earnings_notes.find({'ticker':ticker})
    for note in notes:
        print(note['date'].strftime('%Y-%m-%d'), note['note'])

if __name__ == '__main__':
    print('hello earnings report')
    time_stamps = []
    conn = MongoClient()
    db = conn.database
    collection = db.basic_data
    arr = []
    tickers_with_notes = get_tickers_with_notes(conn)
    for i, ticker in enumerate(tickers):
        # print('ticker=', ticker)
        try:
            r = collection.find({'ticker': ticker}).sort([('earnings-date-iso', -1)]).limit(0)[0]
            if 'sector' not in r:
                r['sector'] = 'None'

            if not r['earnings-date-iso'] in [None, '']:
                vol_data = get_straddle_vols(conn, r['ticker'])
                front = 0
                try:
                    front = float(vol_data[0]['be'].strip("%"))
                except:
                    front = 0

                arr.append({
                    'ticker': r['ticker'],
                    'has_note': r['ticker'] in tickers_with_notes,
                    'date':r['earnings-date-iso'], 
                    'sector': r['sector'],
                    'market-cap': r['market-cap'],
                    'vol_data': vol_data,
                    'front': front 
                    })
        except:
            pass
    import sys
    param = None
    if len(sys.argv) > 1:
        param = sys.argv[1]
        print('param=', param)
    
    while True:
        arr =report(arr, param)
        ans = input(" Enter id for notes, [E]dit earnigns change,  E[x]it\r\n")
        if ans == 'x':
            exit()
        if ans == 'e':
            edit_screen(conn, arr)
        if ans.isdigit():
            ticker = arr[int(ans)]['ticker']
            if ticker in tickers_with_notes:
                show_notes(conn, ticker)
                input()
            input('[ENTER]')




