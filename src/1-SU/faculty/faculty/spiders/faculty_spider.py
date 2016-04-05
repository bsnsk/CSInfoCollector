import scrapy
import os
from os import system

class FacultySpider(scrapy.Spider):
    name = "faculty"
    allowed_domains = ["stanford.edu"]
    start_urls = [
            "http://www-cs.stanford.edu/directory/faculty"
    ]

    def person_parse(self, response):
        name = response.xpath('//title/text()').extract()[0].replace(' ', '_').replace('|', '')\
                .lower().replace("'s", "").replace("home_page", "").replace("_page", "")\
                .replace('\n', '').strip('_').strip()
        filename = "../../../data/1-SU/" + name + "/index.html"
        print response.url,
        if os.path.isfile(filename):
            print " ... (skip)"
            return
        else:
            print " ..."
        system('mkdir "../../../data/1-SU/' + name + '"')
        with open(filename, "w") as f:
            f.write(response.body)

    def parse(self, response):
        for sel in response.xpath("//table/tr/td/a"):
            name = sel.xpath("text()").extract()[0].replace(' ', '_')
            link = sel.xpath("@href").extract()[0]
            if (name.upper() != "CLICK_HERE"):
                print "%s @@@ '%s'" % (name, link)
                yield scrapy.Request(link, callback=self.person_parse)
