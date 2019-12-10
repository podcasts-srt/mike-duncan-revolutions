#!/usr/bin/env python
"""

 Provides a crawler to extract links from a website (https://www.revolutionspodcast.com/).
__author__ = "Manasse Ngudia"
__email__ = "manasse@mnsuccess.com"

This python script (podcast.py) aims to browse all the pages of the website https://www.revolutionspodcast.com/ in order to extract all the information about each episode of the podcast (title, date, link page, audio link).

To run this script, you would need:

1. install python 3 on your machine
2. Install the pip manager for Python (https://pip.pypa.io/en/stable/installing/)
3. Install SCRAPY package via PIP (https://pip.pypa.io/en/stable/installing/)

Once this step is complete, you can execute the script and generate the JSON file (data.json) by typing this command:

scrapy runspider podcast.py -o data.json

"""
import scrapy
from scrapy.selector import Selector

class PodCastSpider(scrapy.Spider):
    name = 'podcast_spider'
    start_urls = ['https://www.revolutionspodcast.com/']

    def parse(self, response):
        sel = Selector(response)
        h2s = sel.xpath("//div[@id='beta-inner']/h2/text()") 
        for counter, h2 in enumerate(h2s,1):
            date = h2
            title = sel.xpath("//div[@id='beta-inner']/h2[{}]/following-sibling::div/div/h3/a/text()".format(counter))
            page = sel.xpath("//div[@id='beta-inner']/h2[{}]/following-sibling::div/div/h3/a/@href".format(counter))
            audio = sel.xpath("//div[@id='beta-inner']/h2[{}]/following-sibling::div/div/div/div/p[contains(text(), 'Direct Link:')]/a/@href".format(counter))
            yield {
                'Title': title.get(),
                'Date': date.get(),
                'Page': page.get(),
                'Audio': audio.get(),
            }
        NEXT_PAGE_SELECTOR = '.pager-right a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
        else:
            yield {
                'Title': "0.00- Introduction",
                'Date': "unknown",
                'Page': "https://www.revolutionspodcast.com/2013/09/000-introduction.html",
                'Audio': "https://traffic.libsyn.com/revolutionspodcast/000-_Introduction.mp3",
            }

