from urllib.request import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MultiDomainSpider(CrawlSpider):
    name = "multi_domain_spider"
    
    # Example start URLs
    start_urls = [
        # 'https://books.toscrape.com/',
        # 'https://quotes.toscrape.com/'
        'http://localhost:8002/quotes.html',
        #'http://localhost:8001/books.html'
    ]
    
    # Updated domain patterns with simpler URL matching
    domain_patterns = {
        # 'books.toscrape.com': r'/catalogue/.*',
        # 'quotes.toscrape.com': r'/page/.*'
        'localhost:8001': r'/catalogue/.*',
        'localhost:8002': r'/page/.*'
    }
    
    rules = (
        Rule(
            LinkExtractor(
                allow=[domain_patterns['localhost:8001']],
                allow_domains=['books.toscrape.com','localhost']
                ),
            callback='log_discovered_url',
            follow=True,
            process_links='filter_links_for_books'
        ),
        Rule(
            LinkExtractor(
                allow=[domain_patterns['localhost:8002']],
                allow_domains=['quotes.toscrape.com', 'localhost'],
                ),
            callback='log_discovered_url',
            follow=True,
            process_links='filter_links_for_quotes'
        ),
    )
    
    def filter_links_for_books(self, links):
        return self.filter_links(links, 'http://localhost:8001')
    
    # Filter links for quotes (localhost:8002)
    def filter_links_for_quotes(self, links):
        return self.filter_links(links, 'http://localhost:8002')

    # General filtering method
    def filter_links(self, links, server_url):
        filtered_links = []
        print("links: ", links)
        print("server_url: ", server_url)
        for link in links: 
            if server_url == "http://localhost:8002":
                if link.url.startswith("https://quotes.toscrape.com"):
                    filtered_links.append(link)
            elif server_url == "http://localhost:8001":
                if link.url.startswith("https://books.toscrape.com"): 
                    filtered_links.append(link)
            # simialry if you have other servers running or domain
            # add the respective condition for them as well. 
        print(f"Filtered links for {server_url}: {filtered_links}")
        return filtered_links
                
    
    def log_discovered_url(self, response):
        # domain = response.url.split("/")[2]
        # pattern = self.domain_patterns.get(domain)
        # print(f"Discovered URL for {domain} -> : [{response.url}] which follows the regex pattern: {pattern}")
        print("url: ", response.url)

    def parse_start_url(self, response):
        self.log_discovered_url(response)