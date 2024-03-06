import pandas_ta as ta
import pandas as pd


from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.lib import TrailingStrategy
from data_sources import get_candles_bitstamp


class TrailingStopper(TrailingStrategy):
    pair_name = 'Unknown'
    sl_atr_range = 1
    atr_window = 14
    sma_trend_window = 200
    trend_confirmation_offset = 1
    offset_unit_size = 0.0001
    deal_percent = 10

    def init(self):
        super().init()
        self.atr = self.I(
            ta.atr,
            pd.Series(self.data.High),
            pd.Series(self.data.Low),
            pd.Series(self.data.Close),
            self.atr_window
        )
        self.sma_trend = self.I(
            ta.sma,
            pd.Series(self.data.Close),
            self.sma_trend_window

        )

    def next(self):
        super().next()
        self.set_trailing_sl(self.sl_atr_range)
        if self.position:
            pass
        else:
            if crossover(self.data.Close, self.sma_trend+self.trend_confirmation_offset*self.offset_unit_size):
                self.buy(size=self.deal_percent/100)
            if crossover(self.sma_trend-self.trend_confirmation_offset*self.offset_unit_size, self.data.Close):
                self.sell(size=self.deal_percent/100)


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


if __name__ == '__main__':
    #
    # ADABTC = get_candles_bitstamp('adabtc', 86400, 1000)
    # bt = Backtest(ADABTC, TrailingStopper, cash=10, commission=.002)
    # stats = bt.optimize(
    #     pair_name='adabtc',
    #     sl_atr_range=range(1, 5, 1),
    #     atr_window=range(1, 10, 1),
    #     sma_trend_window=range(25, 100, 10),
    #     trend_confirmation_offset=range(1, 100, 1),
    #     maximize='Return [%]',
    #     offset_unit_size=0.0000001
    # )
    # bt.plot()
    # print(stats)

    # XRPBTC = get_candles_bitstamp('xrpbtc', 86400, 1000)
    # bt = Backtest(XRPBTC, TrailingStopper, cash=10, commission=.002)
    # stats = bt.optimize(
    #     pair_name='xrpbtc',
    #     sl_atr_range=range(1, 5, 1),
    #     atr_window=range(5, 15, 1),
    #     sma_trend_window=range(25, 35, 5),
    #     trend_confirmation_offset=range(1, 100, 1),
    #     maximize='Return [%]',
    #     offset_unit_size=0.000001
    # )
    # bt.plot()
    # print(stats)
    #
    # ETHBTC = get_candles_bitstamp('ethbtc', 86400, 1000)
    # bt = Backtest(ETHBTC, TrailingStopper, cash=10, commission=.002)
    # stats = bt.optimize(
    #     pair_name='ethbtc',
    #     sl_atr_range=range(1, 5, 1),
    #     atr_window=range(10, 30, 5),
    #     sma_trend_window=range(30, 50, 10),
    #     trend_confirmation_offset=range(1, 100, 1),
    #     maximize='Return [%]',
    #     offset_unit_size = 0.0001
    # )
    # bt.plot()
    # print(stats)

    BTCUSDT = get_candles_bitstamp('btcusd', 86400, 1000)
    print(BTCUSDT)
    bt = Backtest(BTCUSDT, TrailingStopper, cash=10_000_000, commission=.002)
    stats = bt.optimize(
        pair_name='btcusd',
        sl_atr_range = range(1, 5, 1),
        atr_window = range(10, 30, 5),
        sma_trend_window = range(30, 50, 10),
        deal_percent = range(5,50,5),
        trend_confirmation_offset = range(100, 2000, 100),
        maximize='Return [%]',
        offset_unit_size = 1
     )
    # stats = bt.run()
    bt.plot()
    print(stats)
    #

