from datetime import datetime

from binance import Client
import configparser


class Transaction:
    direction: str = "BUY"
    amount: float = 10
    candle = {}

    def __init__(self, dirctn: str, amt: float, cndl):
        self.direction = dirctn
        self.amount = amt
        self.candle = cndl


class Strategy:

    @staticmethod
    def evaluate(candle_scope: []):
        last_candle = candle_scope[-1]
        if last_candle["open"] < last_candle["close"]:
            # the candle is green
            return Transaction("BUY", 10, last_candle)
        else:
            return Transaction("SELL", 10, last_candle)


class MegaStrata(Strategy):

    @staticmethod
    def evaluate(candle_scope: []):
        if len(candle_scope) < 3:
            return None
        if (candle_scope[-1]["open"] < candle_scope[-1]["close"] and
                candle_scope[-2]["open"] < candle_scope[-2]["close"] and
                candle_scope[-3]["open"] < candle_scope[-3]["close"]):
            return Transaction("BUY", 10, candle_scope[-1])
        elif (candle_scope[-1]["open"] > candle_scope[-1]["close"] and
                candle_scope[-2]["open"] > candle_scope[-2]["close"] and
                candle_scope[-3]["open"] > candle_scope[-3]["close"]):
            return Transaction("SELL", 10, candle_scope[-1])
        else:
            return None


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
count = 0

acc = Account()
acc.strat = MegaStrata()
for candle in candles:
    count += 1
    result = acc.strat.evaluate(candles[:count])
    if result is not None:
        acc.commit_tran(result)
    # print(str(candle))
mega_result = str(acc.evaluate(candles[-1]))

print("-----------------")

# acc = Account()
# for candle in candles:
#    count += 1
#    result = acc.strat.evaluate(candles[:count])
#    if result is not None:
#        acc.commit_tran(result)
#    # print(str(candle))
print("---- final MegaStrata account value = " + mega_result)
