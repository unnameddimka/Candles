import logging
import sys
import requests
import json
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
rootLogger.setLevel(logging.INFO)


class Candle:
    def __init__(self, dict):
        self.open = 0
        self.close = 0
        self.high = 0
        self.low = 0
        self.timestamp = 0
        self.volume = 0
        self.__dict__ = dict


class CandleGetter:
    def __init__(self):
        rootLogger.info('CandleGetter created')
        self.get_candles = lambda: print('getting candles')
        pass


def get_candles_bitly(pair,step, limit ):
    rootLogger.info(f'getting candles from bitly pair:{pair},step:{step},limit:{limit}')
    url = f"https://www.bitstamp.net/api/v2/ohlc/{pair}/?step={step}&limit={limit}"
    data = requests.get(url)
    js_result = data.json()
    ohlc_arr = js_result['data']['ohlc']
    rootLogger.info(f'got {len(ohlc_arr)} candles')
    return [Candle(d) for d in ohlc_arr]


getters = dict()
getters['bitly'] = CandleGetter()
getters['bitly'].get_candles = get_candles_bitly

if __name__ == '__main__':
    cg = getters['bitly']
    cg.get_candles('btcusd',86400,10)
