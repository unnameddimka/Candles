# from main import Strategy
from transaction import Transaction

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
    name = "three green buy, three red sell"

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


class CounterMegaStrata(Strategy):
    name = "three green sell, three red buy"

    @staticmethod
    def evaluate(candle_scope: []):
        if len(candle_scope) < 3:
            return None
        if (candle_scope[-1]["open"] < candle_scope[-1]["close"] and
                candle_scope[-2]["open"] < candle_scope[-2]["close"] and
                candle_scope[-3]["open"] < candle_scope[-3]["close"]):
            return Transaction("SELL", 10, candle_scope[-1])
        elif (candle_scope[-1]["open"] > candle_scope[-1]["close"] and
                candle_scope[-2]["open"] > candle_scope[-2]["close"] and
                candle_scope[-3]["open"] > candle_scope[-3]["close"]):
            return Transaction("BUY", 10, candle_scope[-1])
        else:
            return None


def get_strat_array() -> list:
    return [MegaStrata, CounterMegaStrata]

