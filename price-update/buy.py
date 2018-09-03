from ibapi import wrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.utils import iswrapper #just for decorator
from ibapi.common import *
import time
from datetime import datetime

import sys

limitPrice = float(sys.argv[1])
buyCount = float(sys.argv[2])


class TestApp(wrapper.EWrapper, EClient):
    bidPrice = 0
    askPrice = 0
    oID = 0;
    hasBuy = False;
    playBuyOrderTime = datetime.now();

    def __init__(self):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

    @iswrapper
    def nextValidId(self, orderId:int):
        print("setting nextValidOrderId: %d", orderId)
        self.oID = orderId
        # here is where you start using api

        contract = Contract()
        contract.symbol = "TSLA"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "ISLAND"

        self.reqMarketDataType(1)
        #self.reqMktData(19003, contract, "" ,False, False, [])
        self.reqTickByTickData(19004, contract, "BidAsk")

    @iswrapper
    def buy_stock(self):
        print(self.bidPrice)
        global buyCount

        contract = Contract()
        contract.symbol = "TSLA"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "ISLAND"

        order = Order()
        order.action = "BUY"
        order.orderType = "LMT"
        order.totalQuantity = buyCount
        order.lmtPrice = self.bidPrice + 0.01
        #order.orderType = "MTL"
        #order.totalQuantity = 10
        print("place an order" , self.oID)
        self.placeOrder(self.oID, contract,order)
        self.playBuyOrderTime = datetime.now()
        self.oID = self.oID + 1


    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

    @iswrapper
    def accountSummary(self, reqId:int, account:str, tag:str, value:str, currency:str):
        print("Acct Summary. ReqId:" , reqId , "Acct:", account,
            "Tag: ", tag, "Value:", value, "Currency:", currency)

    @iswrapper
    def accountSummaryEnd(self, reqId:int):
        print("AccountSummaryEnd. Req Id: ", reqId)
        # now we can disconnect
        #self.disconnect()

    @iswrapper
    def tickByTickBidAsk(self , tickerId , time , bidPrice,askPrice,bidSize,askSize,attribs):
        print("BID",bidPrice , "ASK", askPrice)
        global limitPrice

        t2 = datetime.now()
        t3 = t2 - self.playBuyOrderTime
        if (t3.seconds > 10 and self.hasBuy == True):
            self.playBuyOrderTime = datetime.now()
            self.reqGlobalCancel()
            self.hasBuy = False

        if(bidPrice<limitPrice and self.hasBuy == False):
                #self.disconnect()

            self.bidPrice = bidPrice
            self.askPrice = askPrice

            #if(self.hasBuy == False and askPrice-bidPrice > 0.3):
            print("start to buy at ..", bidPrice)
            self.buy_stock()
            self.hasBuy = True
        else:
            print("bid price is bigger than limit price")

    @iswrapper
    def orderStatus(self, orderId: OrderId, status: str, filled: float, remaining: float, avgFillPrice: float, permId: int,parentId: int, lastFillPrice: float, clientId: int,whyHeld: str, mktCapPrice: float):
        print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled)
        #print(time.time()-self.playBuyOrderTime)
        global buyCount

        if (filled == buyCount and self.hasBuy == True):

            self.reqGlobalCancel()
            self.Close()

            self.oID = self.oID + 1



            contract = Contract()
            contract.symbol = "TSLA"
            contract.secType = "STK"
            contract.currency = "USD"
            contract.exchange = "ISLAND"

            order = Order()
            order.action = "SELL"
            order.orderType = "LMT"
            order.totalQuantity = 10

            order.lmtPrice = avgFillPrice + 0.5

            #if(self.askPrice-0.01 > avgFillPrice + 0.3):
            #    order.lmtPrice = self.askPrice - 0.01
                #order.lmtPrice = avgFillPrice + 0.3
            #else:
            #    order.lmtPrice = avgFillPrice + 0.3

            #self.placeOrder(self.oID, contract, order)
            #self.hasBuy = False
            #self.nextValidOrderId = self.nextValidOrderId + 1



def main():
    app = TestApp()
    app.connect("127.0.0.1", 7496, clientId=123)
    app.run()

if __name__ == "__main__":
    main()


