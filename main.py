from clientpy2 import *
from tick_info import *
import socket
import sys
import sys
import re

my_profile = Profile()
equity_array = []

def initialize_equity():
    #CURRENT EQUITIES
    match  = re.findall('(\w+) \d+', qrun("MY_SECURITIES") )
    for equity_name in match:
        equity_array.append(Equity(equity_name))
def qrun(*command): #quick run
    ret = run("CounterLogic_EMY", "yubodoxical", *command)
    return ret

def initialize_ticker(profile=my_profile): #runs at the start of each tick to get values for everything
    #MY_CASH
    match  = re.search('MY_CASH_OUT (\d+)', qrun("MY_CASH") )
    my_profile.money = float(match.group(1))

    if equity_array.len == 0:
        initialize_equity()

    #MY_SECURITIES
    output_string = qrun("MY_SECURITIES")
    for equity in equity_array:
        match = re.search(equity.name + ' (\S+)', output_string)
        equity.my_owned = float(match.group(1))
        match = re.search(equity.name + ' \S+ (\S+)', output_string)
        equity.my_dividend_ratio = float(match.group(1))

    #MY_ORDERS
    output_string = qrun("MY_ORDERS")
    for equity in equity_array:
        match = re.search('BID ' + equity.name + ' (\S+)', output_string)
        

    qrun('BID EA 1 2')
    qrun('ASK EA 1000 1')
    output_string = qrun("MY_ORDERS")
    #print output_string
    
    
    #ORDERS
    for equity in equity_array:
        output_string = qrun("ORDERS " + equity.name)
        match = re.findall('BID ' + equity.name + ' (\S+)', output_string)
        float_match=[]
        for x in match:
            y = float(x)
            float_match.append(y)
        equity.bid_price = float_match
        match = re.findall('BID ' + equity.name + ' \S+ (\S+)', output_string)
        float_match=[]
        for x in match:
            y = float(x)
            float_match.append(y)
        equity.bid_shares = float_match

        match = re.finall('ASK ' + equity.name + ' (\S+)', output_string)
        float_match=[]
        for x in match:
            y = float(x)
            float_match.append(y)
        equity.ask_price = float_match
        match = re.finall('ASK ' + equity.name + ' \S+ (\S+)', output_string)
        float_match=[]
        for x in match:
            y = float(x)
            float_match.append(y)
        equity.ask_shares = float_match

    #SECURITIES
    output_string = qrun("SECURITIES")
    for equity in equity_array:
        match = re.search(equity.name + ' (\S+)', output_string)
        equity.net_worth = float(match.group(1))
        match = re.search(equity.name + ' \S+ (\S+)', output_string)
        equity.dividend_ratio = float(match.group(1))
        match = re.search(equity.name + ' \S+ \S+ (\S+)', output_string)
        equity.volatility = float(match.group(1))
