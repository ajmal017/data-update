# -*- coding: utf-8 -*-
import scrapy


connection = pymysql.connect(host='127.0.0.1',
                             port=8989,
                             user='root',
                             password='root',
                             db='stock',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cur = connection.cursor()
cur.execute("""REPLACE INTO daily_price(`id`,`date`,`open_price`,`high_price`,`close_price`,`low_price`,
              `volume`,`amount`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",('002007',date,open_price,high_price,close_price,
              low_price,volume,amount))

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://quotes.money.163.com/service/chddata.html?code=1002007&start=20040610&end=20180131&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP']

    def parse(self, response):


        example['file_urls'] = ['http://quotes.money.163.com/service/chddata.html?code=1002007&start=20040610&end=20180131&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP']

        return example
