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

    hardcoded_by_title = {
        '1.5- Cavaliers and Roundheads': 'https://traffic.libsyn.com/revolutionspodcast/005-Cavaliers_and_Roundheads.mp3'
    }

    def parse(self, response):
        sel = Selector(response)
        h2s = sel.xpath("//div[@id='beta-inner']/div[contains(@class, 'entry-author-mike_duncan')]") 
        for counter, h2 in enumerate(h2s,1):
            date = sel.xpath("//div[@id='beta-inner']/div[contains(@class, 'entry-author-mike_duncan')][{}]/preceding-sibling::h2[1]/text()".format(counter))
            title = sel.xpath("//div[@id='beta-inner']/div[contains(@class, 'entry-author-mike_duncan')][{}]/div/h3/a/text()".format(counter))
            page = sel.xpath("//div[@id='beta-inner']/div[contains(@class, 'entry-author-mike_duncan')][{}]/div/h3/a/@href".format(counter))
            audio1 = sel.xpath("//div[@id='beta-inner']/div[contains(@class, 'entry-author-mike_duncan')][{}]/div/div/div/p/a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'direct link:')]/@href".format(counter))
            audio2 = sel.xpath("//div[@id='beta-inner']/div[contains(@class, 'entry-author-mike_duncan')][{}]/div/div/div/p[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'direct link:')]/a/@href".format(counter))

            print "audio1: ", audio1.get()
            print "audio2: ", audio2.get()

            audio = audio1.get() if audio1.get() else audio2.get()
            if title.get() in self.hardcoded_by_title.keys():
                audio = self.hardcoded_by_title[title.get()]

            yield {
                'Title': title.get(),
                'Date': date.get(),
                'Page': page.get(),
                'Audio': audio,
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


