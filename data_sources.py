import requests
import datetime
import pandas

def get_candles_bitstamp(pair, step, limit):

    url = f"https://www.bitstamp.net/api/v2/ohlc/{pair}/?step={step}&limit={limit}"
    data = requests.get(url)
    js_result = data.json()
    ohlc_arr = js_result['data']['ohlc']
    ohlc_dict = {
    'year' : [datetime.date.fromtimestamp(int(s['timestamp'])).year for s in ohlc_arr],
    'month': [datetime.date.fromtimestamp(int(s['timestamp'])).month for s in ohlc_arr],
    'day':   [datetime.date.fromtimestamp(int(s['timestamp'])).day for s in ohlc_arr],
    'Open' : [float(s['open']) for s in ohlc_arr],
    'High' : [float(s['high']) for s in ohlc_arr],
    'Low'  : [float(s['low']) for s in ohlc_arr],
    'Close': [float(s['close']) for s in ohlc_arr],
    'Volume':[float(s['volume']) for s in ohlc_arr]
    }
    df = pandas.DataFrame(ohlc_dict)
    df.index = pandas.to_datetime(df[['day', 'month', 'year']])
    return df


def get_candles_binance(pair, step, limit):
    pass