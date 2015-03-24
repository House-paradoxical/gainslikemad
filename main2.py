from clientpy2 import *
from tick_info import *
import datetime
import sys
import re

my_profile = Profile()
equity_array = []

def initialize_equity():
    #CURRENT EQUITIES
    match  = re.findall('(\w+) \d+', qrun("MY_SECURITIES") )
    for equity_name in match:
        equity_array.append(Equity(equity_name))

def qrun(*commands):
    ret = run("CounterLogic_EMY", "yubodoxical", *commands)
    print ret
    return ret

def highfrequency(equity):
    if (equity.minask - equity.maxbid) < equity.minask / 30:
        trade(equity, "BID")
        trade(equity, "ASK")

def trade(equity, ordertype):
    if ordertype == "ASK" :
        qrun("ASK " + str(equity.name) + " " + str(equity.minask-0.001) + " " +str(int(equity.my_owned)))
    if ordertype == "BID" :
        shares = 0
        if my_profile.money < 250: # my_profile.net_worth()/4:
            shares = int(my_profile.money / equity.minask)
        else:
            shares = int(my_profile.money / 10 / equity.minask)
        qrun("BID " +equity.name + " " + str(equity.maxbid+0.001) + " " +str(int(shares)))
    
def initialize_ticker(profile=my_profile): #runs at the start of each tick to get values for everything

    #INITIALIZE EQUITY_ARRAY
    if len(equity_array) == 0:
        initialize_equity()

    # set up run parameters for run()
    run_parameters = "MY_CASH"
    run_parameters += "\nMY_SECURITIES"
    run_parameters += "\nMY_ORDERS"
    run_parameters += "\nSECURITIES"
    for equity in equity_array:
        run_parameters += "\nORDERS " + equity.name

    raw_output = run("CounterLogic_EMY", "yubodoxical", run_parameters)
    output_string = re.split('MY_CASH_OUT|MY_SECURITIES_OUT|MY_ORDERS_OUT|SECURITIES_OUT|SECURITY_ORDERS_OUT ', raw_output)

    #MY_CASH
    match = re.search('(\S+)', output_string[1] )
    my_profile.money = float(match.group(1))
    if my_profile.starting_money == -1:
        my_profile.starting_money = my_profile.money

    #MY_SECURITIES
    for equity in equity_array:
        match = re.search(equity.name + ' (\S+)', output_string[2])
        equity.my_owned = float(match.group(1))
        if equity.my_owned == 0:
            start_time = 0
        match = re.search(equity.name + ' \S+ (\S+)', output_string[2])
        equity.my_dividend_ratio = float(match.group(1))

    #MY_ORDERS
    for equity in equity_array:
        match = re.search('BID ' + equity.name + ' (\S+)', output_string[3])
        if match:
            equity.my_bid = float(match.group(1))
        else:
            equity.my_bid = 0
        match = re.search('ASK ' + equity.name + ' \S+ (\S+)', output_string[3])
        if match:
            equity.my_ask = float(match.group(1))
        else:
            equity.my_ask = 0

    #SECURITIES
    for equity in equity_array:
        match = re.search(equity.name + ' (\S+)', output_string[4])
        equity.net_worth = float(match.group(1))
        match = re.search(equity.name + ' \S+ (\S+)', output_string[4])
        equity.dividend_ratio = float(match.group(1))
        match = re.search(equity.name + ' \S+ \S+ (\S+)', output_string[4])
        equity.volatility = float(match.group(1))

    #ORDERS
    index_counter = 5
    for equity in equity_array:
        #bid price
        match = re.findall('BID ' + equity.name + ' (\S+)', output_string[index_counter])
        float_match = []
        for x in match:
            y = float(x)
            float_match.append(y)
        equity.bid_price = float_match

        #bid shares
        match = re.findall('BID ' + equity.name + ' \S+ (\S+)', output_string[index_counter])
        float_match = []
        for x in match:
            y = float(x)
            float_match.append(y)
        equity.bid_shares = float_match

        #ask price
        match = re.findall('ASK ' + equity.name + ' (\S+)', output_string[index_counter])
        float_match = []
        for x in match:
            y = float(x)
            float_match.append(y)
        equity.ask_price = float_match

        #ask shares
        match = re.findall('ASK ' + equity.name + ' \S+ (\S+)', output_string[index_counter])
        float_match = []
        for x in match:
            y = float(x)
            float_match.append(y)
        equity.ask_shares = float_match
        index_counter = index_counter + 1
    
    # DOIN SOME SHIT
    for equity in equity_array:
        string = qrun("ORDERS " + str(equity.name))

        equity.bidavg = 0
        equity.bidlot = 0
        equity.maxlot = 0
        equity.maxbid = 0
        tuples = re.findall(r'BID \w+\s(\d+\.\d+) (\d+)', string)
        for tuple in tuples:
            equity.bidavg += float(tuple[0])*float(tuple[1])
            equity.bidlot += float(tuple[1])
            if float(tuple[0]) > equity.maxbid:
                equity.maxlot = float(tuple[1])
                equity.maxbid = float(tuple[0])
        equity.bidavg = equity.bidavg/(equity.bidlot+1)

        equity.askavg = 0
        equity.asklot = 0
        equity.minlot = 0
        equity.minask = float("inf")
        tuples = re.findall(r'ASK \w+\s(\d+\.\d+) (\d+)', string)
        for tuple in tuples:
            equity.askavg += float(tuple[0])*float(tuple[1])
            equity.asklot += float(tuple[1])
            if float(tuple[0]) < equity.minask:
                equity.minlot = float(tuple[1])
                equity.minask = float(tuple[0])
        equity.askavg = equity.askavg/(equity.asklot+1)

        if my_profile.money > my_profile.starting_money / 2:
           if (equity.minask - equity.maxbid) < float(equity.minask)/20:
               qrun("BID " + str(equity.name) + " " + str(equity.minask) + " " + str(int(my_profile.money / 2 / equity.minask)))
            #else:
            #    italy = (equity.maxbid - equity.minask)/2 + equity.minask
             #   qrun("BID " + str(equity.name) + " " + str(italy) + " " + str(int(float(my_profile.money) / float(italy)) ))
        if(equity.my_owned > 0):
            print equity.dividend_ratio * 100
            print equity.my_dividend_ratio * 100
            if (equity.dividend_ratio / equity.my_dividend_ratio + 0.001) > 1.1:
                if(equity.dividend_ratio / equity.my_dividend_ratio) > 1.3:
                    qrun("ASK " + str(equity.name) + " " + str(equity.maxbid) + " " +str(int(equity.my_owned)))
                else:
                    trade(equity, "ASK")
            else:
                highfrequency(equity)
        
        highfrequency(equity)
                
def main():
    try:
        while True:
            print my_profile.money
            initialize_ticker()
    finally:
        main()
                
if __name__ == "__main__":
    main()
