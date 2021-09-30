from binance import Client
import configparser


config = configparser.ConfigParser()
config.read('config/main.ini')
candles = []

bin_client = Client(config["DEFAULT"]["api_key"], config["DEFAULT"]["api_secret"])
for kline in bin_client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 month ago UTC"):
    # print(kline)

    candles.append({"open_time": kline[0],
                    "open": kline[1],
                    "max": kline[2],
                    "min": kline[3],
                    "close": kline[4],
                    "volume": kline[5],
                    "close_time": kline[6],
                    "coin_vol": kline[7],
                    "num_trades": kline[8]})

for candle in candles:
    print(str(candle))
