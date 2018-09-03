# -*- coding: utf-8 -*-
import pymysql.cursors
import pymysql
import datetime
from datetime import datetime

def requiredArg (capital_dict, fundamental_id, date):
    capital_dict[fundamental_id]
    for key in capital_dict[fundamental_id]:
        if (date > key):
            c = capital_dict[fundamental_id][key]
    return c

def getFundamentalByDateRange(fundamental_index, date):
    fundamental_in_range = []
    print date

    for key in fundamental_index:
        if(date >= fundamental_index[key]['start'] and date <= fundamental_index[key]['end']):
            fundamental_in_range.append(key)
    return fundamental_in_range

def getLastpriceBeforeDate(cur,fundamental_id, date):
    sql = "SELECT * FROM daily_price WHERE id =%s and date<%s order by date desc limit 1 "
    args = [fundamental_id, date]
    cur.execute(sql, args)
    row = cur.fetchone()
    return row['close_price']

def getFundamentalIncreaseOrDecrease(fundamental_index, date):
    change = {}
    i = []
    d = []
    for key in fundamental_index:
        if(date == fundamental_index[key]['start']):
            i.append(key)
        if (date == fundamental_index[key]['end']):
            d.append(key)

    change["increase"] = i
    change["decrease"] = d

    return change

connection = pymysql.connect(host='127.0.0.1',
                             port=8989,
                             user='root',
                             password='root',
                             db='stock',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cur = connection.cursor()

fundamental_index = {}
sql = "SELECT * FROM fundamental_tag WHERE tag_id =%d"
cur.execute(sql % 1)
seq = []
all_date = []

for row in cur.fetchall():
    #print row['fundamental_id']
    f = {}
    seq.append(row['fundamental_id'])

    sql = "SELECT MIN(date) as bb FROM daily_price WHERE id =%s"
    cur.execute(sql % row['fundamental_id'])
    min_date = cur.fetchone()

    #print min_date['bb']

    sql = "SELECT MAX(date) as bb FROM daily_price WHERE id =%s"
    cur.execute(sql % row['fundamental_id'])
    max_date = cur.fetchone()

    f["start"] = min_date['bb']
    f["end"] = max_date['bb']
    fundamental_index[row['fundamental_id']] = f

    all_date.append(min_date['bb'])
    #all_date.append(max_date['bb'])

all_date = list(set(all_date))
all_date.sort()
list(set(all_date))
print fundamental_index
print seq
print (all_date)
s = ','.join(seq)



#sql = "SELECT * FROM daily_price WHERE id in (%s) order by `date` asc"
#cur.execute(sql % s)
#for row in cur:
#    print(row)

# update base index
capital_dict = {}
sql = "select * FROM fundamental_capital WHERE fundamental_id in (%s) ORDER BY date ASC"
cur.execute(sql % s)
for row in cur:
    fundamental_id = row['fundamental_id']
    capital = row['capital']
    date = row['date']

    if fundamental_id in capital_dict:
        a = capital_dict[fundamental_id]
    else:
        a = {}
    a[date] = capital
    capital_dict[fundamental_id] = a

print capital_dict


price_dict = {}
first = True
sql = "SELECT * FROM daily_price WHERE id in (%s) order by `date` asc"
cur.execute(sql % s)
for row in cur:

    date = row['date']
    id = row['id']
    close_price = row['close_price']

    if date in price_dict:
        a = price_dict[date]
    else:
        a = {}

    a[id] = close_price
    price_dict[date] = a

    if first:
        first = False
        print price_dict

print 555
print price_dict
print 555555
print(price_dict)
    #print row


first = True
index_base_fundamental = []
base_index_value = 0;
print all_date
for date in all_date:
    if first:
        print ("初始化 指数基数")


        fundamental_list = getFundamentalByDateRange(fundamental_index , date)
        print fundamental_list
        for fundamental_id in fundamental_list:
            index_base_fundamental.append(fundamental_id);
            base_index_value = price_dict[date][fundamental_id] * requiredArg(capital_dict,fundamental_id,date)
            print ("基期市值")
            print base_index_value
        first = False
    else:
        print ("指数基数 的 更新")

        print ("指数修正 ")
        print date
        print ("修正前总市值")
        before_total_cap = 0
        for fundamental_id in index_base_fundamental:
            fundamental_capital = requiredArg(capital_dict, fundamental_id, date)
            last_price = getLastpriceBeforeDate(cur,fundamental_id,date)
            before_total_cap += fundamental_capital * last_price
        print before_total_cap

        print ("总市值变动额")
        change_cap = 0
        change = getFundamentalIncreaseOrDecrease(fundamental_index , date)
        for fundamental_id in change['increase']:
            vol = requiredArg(capital_dict, fundamental_id, date)
            change_cap += price_dict[date][fundamental_id]*vol
        for fundamental_id in change['decrease']:
            vol = requiredArg(capital_dict, fundamental_id, date)
            change_cap -= price_dict[date][fundamental_id] * vol
        print change_cap

        print ("最新基期市值")
        base_index_value = base_index_value*(before_total_cap+change_cap)/before_total_cap
        print base_index_value
        #getFundamentalByDateRange(fundamental_index, date)


#print (fundamental_index)
#print (s)
    #capital = requiredArg(capital_dict, row['id'], row['date'])

    #print capital * row['close_price']


