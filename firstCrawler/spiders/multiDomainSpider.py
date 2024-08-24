from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MultiDomainSpider(CrawlSpider):
    name = "multi_domain_spider"
    
    # Example start URLs
    start_urls = [
        'https://books.toscrape.com/',
        'https://rapidfacto.com/',
        'https://quotes.toscrape.com/'
    ]
    
    domain_patterns = {
        'books.toscrape.com': r'https://books.toscrape.com/catalogue/.*',
        'www.rapidfacto.com': r'https://www.rapidfacto.com/pricing/.*',
        'quotes.toscrape.com': r'https://quotes.toscrape.com/tag/.*'
    }

    rules = (
        # Rule for the specific domain with a hardcoded regex pattern
        Rule(
            LinkExtractor(allow=[domain_patterns['books.toscrape.com']]),
            callback='log_discovered_url',
            follow=True
        ),
        Rule(
            LinkExtractor(allow=[domain_patterns['www.rapidfacto.com']]),
            callback='log_discovered_url',
            follow=True
        ),
        Rule(
            LinkExtractor(allow=[domain_patterns['quotes.toscrape.com']]),
            callback='log_discovered_url',
            follow=True
        )
    )

    def log_discovered_url(self, response):
        domain = response.url.split("/")[2]
        pattern = self.domain_patterns.get(domain)
        print(f"Discovered URL for {domain} -> : [{response.url}] which follows the regex pattern: {pattern}")

    def parse_start_url(self, response):
        self.log_discovered_url(response)
