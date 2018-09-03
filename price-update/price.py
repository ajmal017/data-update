import json
import sys
import time
from datetime import datetime
from datetime import datetime
from ibapi import wrapper
from ibapi.client import EClient
from ibapi.common import *
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.utils import iswrapper  # just for decorator
from pytz import timezone

from lib.Object import Object

south_africa = timezone('US/Eastern')
sa_time = datetime.now(south_africa)
a = sa_time.strftime('%Y-%m-%d %H:%M')
print(a)

from pymongo import MongoClient


client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.price

class TestApp(wrapper.EWrapper, EClient):
    bidPrice = 0
    askPrice = 0
    oID = 0;
    hasBuy = False;
    playBuyOrderTime = datetime.now();

    def __init__(self):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)



    def eric(self):
        print("sdfsdf")





    @iswrapper
    def nextValidId(self, orderId:int):

        print("sss")
        print("setting nextValidOrderId: %d", orderId)
        self.oID = orderId
        # here is where you start using api


        contract = Contract()
        contract.symbol = "TSLA"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "ISLAND"

        print("sdfsdf")
        self.reqMarketDataType(1)
        # self.reqMktData(19003, contract, "" ,False, False, [])
        # self.reqTickByTickData(19004, contract, "BidAsk")

        # queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")
        self.reqHistoricalData(4101, contract, "", "4 M", "5 mins", "TRADES", 1, 1, True, [])

        print("sss")


    @iswrapper
    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print("HistoricalData. ", reqId, " Date:", bar.date, "Open:", bar.open, "High:", bar.high, "Low:", bar.low, "Close:",
              bar.close, "Volume:", bar.volume, "Count:", bar.barCount, "WAP:", bar.average)
        print("a")

        me = Object()
        me.symbol = "TSLA"
        me.date = bar.date
        me.open = bar.open
        me.close = bar.close
        me.high = bar.high
        me.low = bar.low
        me.volume = bar.volume

        filter = Object()
        filter.symbol = "TSLA"
        filter.date = bar.date

        db.m5_price.create_index(
            [("symbol", -1), ("date", 1)],
            unique=True
        )

        db.m5_price.replace_one(json.loads(filter.toJSON()), json.loads(me.toJSON()), True)

    @iswrapper
    def historicalData(self, reqId:int, bar: BarData):
        print("HistoricalData. ", reqId, " Date:", bar.date, "Open:", bar.open,"High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume,"Count:", bar.barCount, "WAP:", bar.average)
        print("a")

        me = Object()
        me.symbol = "TSLA"
        me.date = bar.date
        me.open = bar.open
        me.close = bar.close
        me.high = bar.high
        me.low = bar.low
        me.volume = bar.volume

        filter = Object()
        filter.symbol = "TSLA"
        filter.date = bar.date

        db.m5_price.create_index(
            [("symbol", -1), ("date", 1)],
            unique=True
        )

        db.m5_price.replace_one( json.loads(filter.toJSON()), json.loads(me.toJSON()) , True )

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


def main():
    app = TestApp()
    app.connect("127.0.0.1", 7496, clientId=123)
    app.run()

if __name__ == "__main__":
    main()


