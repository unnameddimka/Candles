import pandas_ta as ta
import pandas as pd
from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.lib import TrailingStrategy
from data_sources import get_candles_bitstamp




class ImbaStrata(Strategy):
    ma_period = 40
    retest_window = 10

    def init(self):
        super().init()
        self.sma_trend = self.I(
            ta.sma,
            pd.Series(self.data.Close),
            self.ma_period
        )

    def next(self):
        super().next()
        if not self.position:
            # no position. Looking for crossover down.
            if crossover(self.sma_trend, self.data.Low):
                self.buy()
            # no position. Looking for crossover down.
            if crossover(self.data.High, self.sma_trend):
                self.sell()

        else:
            # we have position. Checking for crossing to close.

            if self.position.is_long:
            # we have position. Checking for crossing to close.
                if self.data.Close < self.sma_trend:
                    self.position.close()
            else:
                if self.data.Close > self.sma_trend:
                    self.position.close()


if __name__ == '__main__':
    BTCUSDT = get_candles_bitstamp('btcusd', 86400, 1000)
    print(BTCUSDT)
    bt = Backtest(BTCUSDT, ImbaStrata, cash=10_000_000, commission=.002)
    stats = bt.optimize(
        ma_period = range(10, 200, 5),
        maximize='Return [%]',
    )
    #stats = bt.run()
    bt.plot()
    print(stats)

