from pathlib import Path
import scrapy
import re
import json

class MultiDomainSpider(scrapy.Spider):
    name = "multi_domain_spider"

    start_urls = [
        'https://books.toscrape.com/',
        #'https://rapidfacto.com/'
    ]

    domain_patterns = {
        #'books.toscrape.com': r'https://books.toscrape.com/catalogue/category/books/mystery_3/index.html',
        #'quotes.toscrape.com': r'https://quotes.toscrape.com/tag',
        'books.toscrape.com': r'https://books.toscrape.com/catalogue/.*',
        #'quotes.toscrape.com': r'https://quotes.toscrape.com/tag/.*',
        #'www.rapidfacto.com': r'https://www.rapidfacto.com/pricing/.*'
    }

    def __init__(self, *args, **kwargs):
        super(MultiDomainSpider, self).__init__(*args, **kwargs)
        self.processed_urls = set()
    
    def parse(self, response):
        domain = response.url.split("/")[2]
        pattern = self.domain_patterns.get(domain)
        fileName = f"{domain}.html"
        Path(fileName+"raw").write_bytes(response.body)

        # Extract data
        cards = response.css(".product_pod")
        itemList = []
        for card in cards:
            title = card.css("h3>a::text").get()
            price = card.css(".price_color::text").get()
            item_url = response.urljoin(card.css("h3>a::attr(href)").get())

            # Skip if this URL has already been processed
            if item_url in self.processed_urls:
                continue
            
            self.processed_urls.add(item_url)
            itemList.append({"title": title, "price": price, "url": item_url})

        print("item list: ", itemList)
        jsonFileName = f"{domain}.json"

        # Load existing data
        if Path(jsonFileName).exists():
            with open(jsonFileName, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        # Append new data to existing data
        existing_data.extend(itemList)

        # Write updated data back to file
        with open(jsonFileName, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)

        # Follow the links which are matching the pattern
        for link in response.css('a::attr(href)').getall():
            full_url = response.urljoin(link)
            if re.match(pattern, full_url):
                yield response.follow(full_url, callback=self.parse)
            else:
                self.logger.warning(f"No pattern found for domain: {domain}, {full_url}")
