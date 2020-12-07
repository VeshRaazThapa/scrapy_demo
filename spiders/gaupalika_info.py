# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from demo.items import DemoItem


class GaupalikaInfoSpider(scrapy.Spider):
    name = 'gaupalika_info'
    allowed_domains = ['gov.np']
    start_urls = ['https://www.mofaga.gov.np/local-contact/village-mun-prov-1',
                  'https://www.mofaga.gov.np/local-contact/village-mun-prov-2',
                  'https://www.mofaga.gov.np/local-contact/village-mun-prov-3',
                  'https://www.mofaga.gov.np/local-contact/village-mun-prov-4',
                  'https://www.mofaga.gov.np/local-contact/village-mun-prov-5',
                  'https://www.mofaga.gov.np/local-contact/village-mun-prov-6',
                  'https://www.mofaga.gov.np/local-contact/village-mun-prov-7'
    ]

    def parse(self, response):
        palika_links = response.xpath('//*[@class="badge badge-success"]/a/@href').extract()
        for palika_ink in palika_links:
            yield Request(url=palika_ink + '/staff',
                          callback=self.inner_page)
        next_page_urls = response.xpath('//*[@class="page-link"]/@href').extract()
        for next_page_url in next_page_urls:
            yield Request(url=next_page_url,
                          callback=self.parse)

    def inner_page(self,response):
        item = DemoItem()
        # designations = response.xpath("//*[@class='views-field views-field-field-designation active']").extract()
        # for designation in designations:
        table_rows = response.xpath('//tr')
        for table_row in table_rows:
                # print(table_row)
                designation = table_row.xpath('//td[3]/text()').extract_first()
                if 'प्रमुख प्रशासकिय अधिकृत' in designation or 'लेखा अधिकृत' in designation:
                    phone_num = table_row.xpath("//td[6]/text()").extract_first()
                    name = table_row.xpath("//td[2]/a/text()").extract_first()
                    email= table_row.xpath("//td[5]/text()").extract_first()
                    item['name'] = name.replace('\n', '')
                    item['phone_num'] = phone_num.replace('\n', '')
                    item['designation'] = designation.replace('\n', '')
                    item['email'] = email.replace('\n', '')
                    return item
