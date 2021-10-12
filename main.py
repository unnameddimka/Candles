from datetime import datetime
from binance import Client
import configparser

from strats import Strategy
import strats
from transaction import Transaction


class Account:
    usd: float
    asset: float
    strat: Strategy
    signal_count: int

    def __init__(self):
        self.usd = 100
        self.asset = 0
        self.strat = Strategy()
        self.signal_count = 0

    def commit_tran(self, tran: Transaction):

        asset_in_usd = tran.amount / float(tran.candle["close"])
        ts = int(tran.candle["open_time"])
        print("signal number " + str(self.signal_count))
        print(" time: " +
              datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M:%S') + " " +
              tran.direction + " " + str(asset_in_usd) + " for " + str(tran.amount) + " USD")
        print("price: "+tran.candle["close"])
        if tran.direction == "BUY":
            if tran.amount > self.usd:
                print("not enough money for tran.")
                return
            # decreasing usd balance
            self.usd -= tran.amount
            # increasing asset balance
            self.asset += asset_in_usd
        elif tran.direction == "SELL":
            # increasing usd balance
            self.usd += tran.amount
            # decreasing asset balance
            self.asset -= asset_in_usd
        print("current saldo: " + str(self.asset) + " asset and " + str(self.usd) + "USD")
        print("---")
        self.signal_count += 1

    def evaluate(self, cdl):
        asset_value = self.asset * float(cdl["close"])
        return asset_value + self.usd

#   main code. :)


config = configparser.ConfigParser()
config.read('config/main.ini')
candles = []

bin_client = Client(config["DEFAULT"]["api_key"], config["DEFAULT"]["api_secret"])
for kline in bin_client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "2020-01-01"):
    # print(kline)  "1 year ago UTC"

    candles.append({"open_time": kline[0],
                    "open": kline[1],
                    "max": kline[2],
                    "min": kline[3],
                    "close": kline[4],
                    "volume": kline[5],
                    "close_time": kline[6],
                    "coin_vol": kline[7],
                    "num_trades": kline[8]})


for strat in strats.get_strat_array():
    print('--------starting testing strategy "'+strat.name + '"')
    acc = Account()
    acc.strat = strat
    count = 0
    for candle in candles:
        count += 1
        result = acc.strat.evaluate(candles[:count])
        if result is not None:
            acc.commit_tran(result)
    # print(str(candle))
    mega_result = str(acc.evaluate(candles[-1]))
    print('--------strategy "'+strat.name+'" is '+mega_result)
