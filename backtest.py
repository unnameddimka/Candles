import pandas
import pandas_ta as ta
import pandas as pd
import requests
import datetime

from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG


class RsiOscillator(Strategy):

    upper_bound = 80
    lower_bound = 30
    rsi_window = 14

    # Do as much initial computation as possible
    def init(self):
        self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_window)

    # Step through bars one by one
    # Note that multiple buys are a thing here
    def next(self):
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.lower_bound, self.rsi):
            self.buy()


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
    df.index = pd.to_datetime(df[['day', 'month', 'year']])
    return df


if __name__ == '__main__':

    BTCUSDT = get_candles_bitstamp('btcusd', 86400, 500)
    print(BTCUSDT)
    bt = Backtest(BTCUSDT, RsiOscillator, cash=10_000_000, commission=.002)
    stats = bt.optimize(
        upper_bound=range(50, 90, 5),
        lower_bound=range(20, 50, 5),
        rsi_window=range(10, 30, 2),
        maximize='Return [%]'
    )
    # stats = bt.run()
    bt.plot()