from pathlib import Path
import scrapy
import re
import json

class MultiDomainSpider(scrapy.Spider):
    name = "multi_domain_spider"

    start_urls = [
        'https://books.toscrape.com/',
        'https://www.rapidfacto.com/'
    ]

    domain_patterns = {
        #'books.toscrape.com': r'https://books.toscrape.com/catalogue/category/books/mystery_3/index.html',
        #'quotes.toscrape.com': r'https://quotes.toscrape.com/tag',
        'books.toscrape.com': r'https://books.toscrape.com/catalogue/.*',
        #'quotes.toscrape.com': r'https://quotes.toscrape.com/tag/.*',
        'rapidfacto.com': r'https://www.rapidfacto.com/contact-us/'
    }

    def parse(self, response):
        
        domain = response.url.split("/")[2]
        print("domain: ", domain)
        pattern = self.domain_patterns.get(domain)
        print("pattern: ", pattern)
        fileName = f"{domain}.html"
        Path(fileName+"raw").write_bytes(response.body)
        # we can write a if else or switch case condition
        # to store the data of specific website, 
        # currently in the example i am storing for books.to.scrape.com only. :)
        cards = response.css(".product_pod")
        itemList = []
        for card in cards: 
            title = card.css("h3>a::text").get()
            price = card.css(".price_color::text").get()
            itemList.append({"title": title, "price": price})

        print("item list: ", itemList)
        json_data = json.dumps(itemList, indent=4, ensure_ascii=False)
        Path(fileName).write_text(json_data, encoding='utf-8')