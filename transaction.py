class Transaction:
    direction: str = "BUY"
    amount: float = 10
    candle = {}

    def __init__(self, dirctn: str, amt: float, cndl):
        self.direction = dirctn
        self.amount = amt
        self.candle = cndl