import candle_getter
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

import logging
import sys
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
rootLogger.setLevel(logging.INFO)


if __name__ == '__main__':
    cg = candle_getter.getters['bitly']
    candle_data = cg.get_candles('btcusd', 86400,500)

    candle_json_dict_data = {
        'x': [datetime.fromtimestamp(int(candle.timestamp)) for candle in candle_data],
        'open': [candle.open for candle in candle_data],
        'high': [candle.high for candle in candle_data],
        'low': [candle.low for candle in candle_data],
        'close': [candle.close for candle in candle_data]
    }

    fig = go.Figure(data=[go.Candlestick(candle_json_dict_data)])
    fig.show()
