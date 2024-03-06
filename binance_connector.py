import keycrypt
from binance.client import Client
import json

cl = None


def connect():
    keys = keycrypt.read_and_decrypt("config/enckey.js")
    cl = Client(keys["apikey"],keys["secretkey"])
    res = cl.get_account()
    f = open('results/res1.js','w')
    json.dump(res,f)


if __name__ == '__main__':
    connect()

