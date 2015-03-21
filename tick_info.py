import sys

class Profile:
    def __init__(self, starting_money=1000):
        self.money = starting_money

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
