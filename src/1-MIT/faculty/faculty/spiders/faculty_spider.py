import scrapy
import os
from os import system
from faculty.items import FacultyItem

class FacultySpider(scrapy.Spider):
    name = "faculty"
    allowed_domains = ["mit.edu"]
    start_urls = [
            "https://www.eecs.mit.edu/people/faculty-advisors"
    ]

    def person_info_parse(self, response):
        url = response.url
        item = response.meta['item']
        name = item['name']
        filename = url[len(item['link']):].rstrip('/')
        if filename == "":
            return
        target_filename = "../../../data/1-MIT/" + name.encode('utf-8') + "/" + filename.lstrip('/').encode('utf-8')
        system('mkdir -p "' + '/'.join(target_filename.split('/')[:-1]) + '"')
        if os.path.isdir(target_filename):
            target_filename = target_filename + "/index.html"
        if target_filename.split("/")[-1].find('.') == -1:
            target_filename = target_filename + ".html"
        with open(target_filename, "w") as f:
            f.write(response.body)

    def person_index_parse(self, response):
        item = response.meta['item']
        name = item['name']
        if name == "":
            return
        filename = "../../../data/1-MIT/" + name.encode('utf-8') + "/index.html"
        print response.url,
        if os.path.isfile(filename):
            print " ... (skip)"
            return
        else:
            print " ..."
        system('mkdir "../../../data/1-MIT/' + name.encode('utf-8') + '"')
        with open(filename, "w") as f:
            f.write(response.body)
        for sel in response.xpath('//a/@href'):
            url = sel.extract()
            if url.find(":") != -1 and url.startswith(item['link']):
                url= url[len(item['link']):]
            if url.find(":") == -1 and url[-4:] != ".pdf":
                url = response.urljoin(url)
                yield scrapy.Request(url, meta={'item':item}, callback=self.person_info_parse)


    def parse(self, response):
        for sel in response.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " views-field-title ")]')\
                .xpath('*[contains(concat(" ", normalize-space(@class), " "), " card-title ")]'):
            if len(sel.xpath("a").extract()) == 0:
                continue
            name = sel.xpath("a/text()").extract()[0]
            link = sel.xpath("a/@href").extract()[0]
            if (name.upper() != "CLICK_HERE") and link.startswith("http"):
                print "%s @@@ '%s'" % (name, link)
                item = FacultyItem()
                item['name'] = name
                item['link'] = link.rstrip('/')
                yield scrapy.Request(url=link, meta={'item': item}, callback=self.person_index_parse)