import sys

class Profile:
    def __init__(self):
        self.money = 0
        self.starting_money = -1
        
class Equity:
    def __init__(self, name=""):
        self.name = name
        self.my_owned = 0
        self.my_dividend_ratio = 0
        self.my_bid = 0
        self.my_ask = 0

        self.net_worth = 0
        self.dividend_ratio = 0
        self.volatility = 0

        self.bids = 0
        self.bids_shares = 0
        self.asks = 0
        self.asks_shares = 0

        self.time = 0
        self.askavg = 0
        self.asklot = 0
        self.minlot = 0
        self.minask = float("inf")
