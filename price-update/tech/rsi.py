from ibapi import wrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.utils import iswrapper #just for decorator
from ibapi.common import *
import time
from datetime import datetime

import json
import sys

from datetime import datetime
from pytz import timezone

from ..lib.Object import Object

south_africa = timezone('US/Eastern')
sa_time = datetime.now(south_africa)
a = sa_time.strftime('%Y-%m-%d %H:%M')
print(a)

from pymongo import MongoClient


def avgGain(array):
    sum = 0
    for d in array:
        if(d>0):
            sum = sum+d
    return sum/len(array)

def avgLoss(array):
    sum = 0
    for d in array:
        if(d<0):
            sum = sum+d
    return sum/len(array)

client = MongoClient()
client = MongoClient('localhost', 27017)

db = client.price
cursor = db.m5_price.find({}).sort("date",1)
#cursor = db.m5_price.find({}).sort("date",1).limit(200).skip(6630-200)
i = 0
pre_close_price = 0
diff = []
ag = 0
al = 0
last_change = 0
for document in cursor:

    if(i > 0):
        for b in document.items():
            if(b[0]== 'close'):
                diff.append(b[1]-pre_close_price)
                last_change = b[1]-pre_close_price
                pre_close_price = b[1]
    else:
        for b in document.items():
            if(b[0]== 'close'):
                pre_close_price = b[1]

    if(i == 6):
        #print(diff)
        ag = avgGain(diff)
        al = avgLoss(diff)
        rs = abs(ag/al)
        rsi = 100-100/(1+rs)
        #print(ag)
        #print(al)
        #print(rs)
        print(rsi)
        print(pre_close_price)

    if (i > 6):
        if(last_change>0):
            ag = (ag*5+last_change)/6
            al = (al*5)/6
        else:
            ag = (ag * 5) / 6
            al = (al * 5+last_change)/ 6
        rs = abs(ag / al)
        rsi = 100 - 100 / (1 + rs)
        #print(ag)
        #print(al)
        #print(rs)
        print(str(last_change) + "=>" + str(pre_close_price) + "=>" + str(rsi) + "=>" )
        for b in document.items():
            if(b[0]=='date'):
                me = Object()
                me.symbol = "TSLA"
                me.date = b[1]
                me.rsi = rsi

                filter = Object()
                filter.symbol = "TSLA"
                filter.date = bb[1]

                db.rsi_6.create_index(
                    [("symbol", -1), ("date", 1)],
                    unique=True
                )

                db.rsi_6.replace_one(json.loads(filter.toJSON()), json.loads(me.toJSON()), True)


        #sys.exit()
    i = i + 1





