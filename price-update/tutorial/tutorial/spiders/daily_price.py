# -*- coding: utf-8 -*-
# run the script by scrapy runspider index.py
import scrapy
import pymysql.cursors
import pymysql
from scrapy.selector import Selector
import time


connection = pymysql.connect(host='127.0.0.1',
                             port=8989,
                             user='root',
                             password='root',
                             db='stock',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cur = connection.cursor()
#http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/002007.phtml?year=2017&jidu=3

class BlogSpider(scrapy.Spider):
    name = 'blogspider'

    print 444444
    print time.strftime("%Y", time.localtime())
    print time.strftime("%m", time.localtime())

    #start_urls = ['http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/002007.phtml?year=2012&jidu=3',
    #              'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/002007.phtml?year=2012&jidu=2',
    #              'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/002007.phtml?year=2012&jidu=1',
    #              'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/002007.phtml?year=2012&jidu=4',
    #              'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/002007.phtml?year=2012&jidu=1',
    #              ]

    file_urls = ['http://quotes.money.163.com/service/chddata.html?code=1002007&start=20040610&end=20180131&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP']

    def parse(self, response):
        titles = response.selector.xpath('//*[@id="FundHoldSharesTable"]').extract()
        #//*[@id="FundHoldSharesTable"]/tbody/tr
        print titles
        titles = response.selector.xpath('//*[@id="FundHoldSharesTable"]/tr')
        #//*[@id="FundHoldSharesTable"]/tbody/tr

        for title in titles[1:]:
            date = title.xpath('normalize-space(td[1]/div/a//text())').extract()
            date = str(date).replace('[u\'','').replace('\']','')


            open_price = title.xpath('td[2]//text()').extract()[0]
            high_price = title.xpath('td[3]//text()').extract()[0]
            close_price = title.xpath('td[4]//text()').extract()[0]
            low_price = title.xpath('td[5]//text()').extract()[0]
            volume = title.xpath('td[6]//text()').extract()[0]
            amount = title.xpath('td[7]//text()').extract()[0]

            print "writing to db"
            cur.execute("""REPLACE INTO daily_price(`id`,`date`,`open_price`,`high_price`,`close_price`,`low_price`,
              `volume`,`amount`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",('002007',date,open_price,high_price,close_price,
              low_price,volume,amount))
            print "wrote to db"

            #print str(date).replace('[u\'','').replace('\']',''),open_price[0],high_price[0]

        connection.commit()

