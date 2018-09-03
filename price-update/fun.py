# -*- coding: utf-8 -*-
# run the script by scrapy runspider fun.py
from __future__ import division
import scrapy
from pymongo import MongoClient

from scrapy.selector import Selector
import re
import math
import json
import gzip
import ast

client = MongoClient('127.0.0.1', 27017)

db = client.stock
collection = db.fundamental

#connection = pymysql.connect(host='127.0.0.1',
#                             port=8989,
#                             user='root',
#                             password='root',
#                             db='stock',
#                             charset='utf8mb4',
#                             cursorclass=pymysql.cursors.DictCursor)
#cur = connection.cursor()
#http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/002007.phtml?year=2017&jidu=3

class BlogSpider(scrapy.Spider):
    name = 'blogspider'

    start_urls = ['http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=&sortRule=-1&page=2&pageSize=20&js=var%20uBbVOftU={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1517353374426']
    #start_urls = ['http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=80&sort=symbol&asc=1&node=sh_a&symbol=&_s_r_a=page']

    def parse(self, response):

        #print response.body

        #if "1,600000,浦发银行" in response.body:
        #    pattern = re.compile('pages:(\d+)')
        #    m = pattern.search(response.body)
        #    if m:
                # 使用 Match 获得分组信息
        #        print 'matching string:', m.group()
        #        pattern = re.compile('\d+')
        #        m = pattern.search(m.group())
        #        if m:
        #            for x in range(1, int(m.group())+1):
        #                url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=A&sortRule=1&page="
        #                url += str(x)
        #                url += "&pageSize=20&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.41302840247096695"

                        #yield scrapy.Request(url, callback=self.parse)

        if "pages" in response.body:

            s = response.body.split("rank:[\"")
            s = s.pop()

            items = s.split("\",\"")
            for k in items:
                item = k.split(",")
                print item[1]
                print item[2]
                #cur.execute("""REPLACE INTO fundamental(`id`,`name`) VALUES (%s,%s)""",
                #            (item[1], item[2]))

                post = { '$set': { 'name': item[2] } }
                query = {'id': item[1]}

                post_id = collection.update_one(query,post,True)


            #xx = u"([\u4e00-\u9fff]+)"
            #pattern = re.compile(xx)
            #m = pattern.findall(body)
            #if m:
            #    print str(m)
                #.encode('utf-8').decode('unicode-escape')


                #cur.execute("""INSERT INTO fundamental(`id`,`name`) VALUES (%s,%s)""",
                #            ('002037', s))
                #connection.commit()
                #  low_price,volume,amount))
                #cur.execute("""REPLACE INTO daily_price(`id`,`date`,`open_price`,`high_price`,`close_price`,`low_price`,
                #  `volume`,`amount`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",('002007',date,open_price,high_price,close_price,
                #  low_price,volume,amount))


            #print str(date).replace('[u\'','').replace('\']',''),open_price[0],high_price[0]
        print "测试"
        print 55



