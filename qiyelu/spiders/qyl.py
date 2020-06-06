# -*- coding: utf-8 -*-
import scrapy
from ..items import QiyeluItem


class QylSpider(scrapy.Spider):
    name = 'qyl'
    allowed_domains = ['qy6.com']
    start_urls = ['http://www.qy6.com/qyml/']
    base_http = 'http://www.qy6.com'

    def parse(self, response):
        hangyes = response.xpath('//td[@valign="top"]/a/@href').getall()
        for hangye in hangyes:
            if hangye[0] == 'h':
                yield scrapy.Request(url=hangye, callback=self.each_hangye)
            else:
                yield scrapy.Request(url=self.base_http + hangye, callback=self.each_hangye)

    def each_hangye(self, response):
        titles1 = response.xpath('//tr[@class="tr1"]/td/a[1]/@href').getall()
        titles2 = response.xpath('//tr[@class="tr2"]/td/a[1]/@href').getall()

        for com1 in titles1:
            yield scrapy.Request(url=com1, callback=self.each_company)
        for com2 in titles2:
            yield scrapy.Request(url=com2, callback=self.each_company)

        next_page = response.xpath('//td[@nowrap][1]/a[last()-1]/@href').get()
        if next_page is not None:
            if next_page[0] == 'h':
                yield scrapy.Request(url=next_page, callback=self.each_hangye)
            else:
                yield scrapy.Request(url=self.base_http + next_page, callback=self.each_hangye)

    def each_company(self, response):
        com_name = response.xpath('//table[@width="450"]//font[@class="f5"]/text()').get()
        cont_name = response.xpath('//table[@width="450"]//table//tr[2]//tr[1]//a//text()').get()
        if com_name:
            dianhua = response.xpath('//table[@width="450"]//table//tr[2]//tr[2]/td[2]/text()').get()
            dianhua = dianhua if dianhua else '空'
            chuanzhen = response.xpath('//table[@width="450"]//table//tr[2]//tr[3]/td[2]/text()').get()
            chuanzhen = chuanzhen if chuanzhen else '空'
            mobile = response.xpath('//table[@width="450"]//table//tr[2]//tr[4]/td[2]/text()').get().strip()
            mobile = mobile if mobile else '空'
            address = response.xpath('//td[@class="lh13"]/span/text()').get()
            address = address if address else '空'

            # print(com_name, cont_name, dianhua, chuanzhen, mobile)
            # print('address', address)

            item = QiyeluItem()
            item['com_name'] = com_name
            item['cont_name'] = cont_name
            item['dianhua'] = dianhua
            item['chuanzhen'] = chuanzhen
            item['mobile'] = mobile
            item['address'] = address
            yield item

        else:
            # print('each_company', response.url)
            lianxiwomen = response.xpath('//div[@class="nav"]/a[last()]/@href').get()
            yield scrapy.Request(url=lianxiwomen, callback=self.each_company2, dont_filter=True)

    def each_company2(self, response):
        print('each_company2')
        com_name = response.xpath('//font[@class="f5"]/text()').get()

        cont_name = response.xpath('//table[@align="center"]//tr//font/text()').get()
        dianhua = response.xpath('//table[@align="center"][1]/tbody/tr[2]/td[2]/text()').get()
        dianhua = dianhua if dianhua else '空'
        chuanzhen = response.xpath('//table[@align="center"][1]/tbody/tr[3]/td[2]/text()').get()
        chuanzhen = chuanzhen if chuanzhen else '空'
        mobile = response.xpath('//table[@align="center"][1]/tbody/tr[4]/td[2]/text()').get().strip()
        mobile = mobile if mobile else '空'
        address = response.xpath('//table[@align="center"][1]/tbody/tr[6]/td[2]//text()').get()

        if mobile:
            item = QiyeluItem()
            item['com_name'] = com_name
            item['cont_name'] = cont_name
            item['dianhua'] = dianhua
            item['chuanzhen'] = chuanzhen
            item['mobile'] = mobile
            item['address'] = address
            yield item
