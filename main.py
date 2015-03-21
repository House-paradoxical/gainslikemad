from clientpy2 import *
from tick_info import *
import sys
import re

my_profile = Profile()
# AAPL=1, ATVI=2, EA=3, FB=4, GOOG=5, MSFT=6, SBUX=7, SNY=8, TSLA=9, TWTR=10
equity_array = []

def initialize_equity():
    #CURRENT EQUITIES
    match  = re.findall('(\w+) \d+', qrun("MY_SECURITIES") )
    for equity_name in match:
        equity_array.append(Equity(equity_name))

def qrun(*commands):
    ret = run("CounterLogic_EMY", "yubodoxical", *commands)
    return ret

def initialize_ticker(profile=my_profile): #runs at the start of each tick to get values for everything

    #INITIALIZE EQUITY_ARRAY
    if len(equity_array) == 0:
        initialize_equity()
    
    #MY_CASH
    match = re.search('MY_CASH_OUT (\d+)', run("CounterLogic_EMY", "yubodoxical", "MY_CASH") )
    my_profile.money = float(match.group(1))

    #MY_SECURITIES
    output_string = run("CounterLogic_EMY", "yubodoxical", "MY_SECURITIES")
    for equity in equity_array:
        match = re.search(equity.name + ' (\S+)', output_string)
        equity.my_owned = float(match.group(1))
        match = re.search(equity.name + ' \S+ (\S+)', output_string)
        equity.my_dividend_ratio = float(match.group(1))

    #MY_ORDERS
    output_string = run("CounterLogic_EMY", "yubodoxical", "MY_ORDERS")
    for equity in equity_array:
        match = re.search('BID ' + equity.name + ' (\S+)', output_string)
        if match:
            equity.my_bid = float(match.group(1))
        else:
            equity.my_bid = 0
        match = re.search('ASK ' + equity.name + ' \S+ (\S+)', output_string)
        if match:
            equity.my_ask = float(match.group(1))
        else:
            equity.my_ask = 0

    #ORDERS
    for equity in equity_array:
        output_string = run("CounterLogic_EMY", "yubodoxical", "ORDERS " + equity.name)
        
        #bid price
        match = re.findall('BID ' + equity.name + ' (\S+)', output_string)
        float_match = []
        for x in match:
            y = float(x)
            float_match.append(y)
        equity.bid_price = float_match

        #bid shares
        match = re.findall('BID ' + equity.name + ' \S+ (\S+)', output_string)
        float_match = []
        for x in match:
            y = float(x)
            float_match.append(y)
        equity.bid_shares = float_match

        #ask price
        match = re.findall('ASK ' + equity.name + ' (\S+)', output_string)
        float_match = []
        for x in match:
            y = float(x)
            float_match.append(y)
        equity.ask_price = float_match

        #ask shares
        match = re.findall('ASK ' + equity.name + ' \S+ (\S+)', output_string)
        float_match = []
        for x in match:
            y = float(x)
            float_match.append(y)
        equity.ask_shares = float_match

    #SECURITIES
    output_string = run("CounterLogic_EMY", "yubodoxical", "SECURITIES")
    for equity in equity_array:
        match = re.search(equity.name + ' (\S+)', output_string)
        equity.net_worth = float(match.group(1))
        match = re.search(equity.name + ' \S+ (\S+)', output_string)
        equity.dividend_ratio = float(match.group(1))
        match = re.search(equity.name + ' \S+ \S+ (\S+)', output_string)
        equity.volatility = float(match.group(1))
