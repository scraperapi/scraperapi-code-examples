import scrapy

"""
SCRAPER SETTINGS

You need to define the following values below:

- API_KEY --> Find this on your dashboard, or signup here to create a 
                free account here https://dashboard.scraperapi.com/signup

To use this script you need to modify a couple settings in the settings.py file:
                
- CONCURRENT_REQUESTS  --> Set this equal to the number of concurrent threads available
                in your plan. For reference: Free Plan (5 threads), Hobby Plan (10 threads),
                Startup Plan (25 threads), Business Plan (50 threads), 
                Enterprise Plan (up to 5,000 threads).

- RETRY_TIMES  --> We recommend setting this to 5 retries. For most sites 
                95% of your requests will be successful on the first try,
                and 99% after 3 retries. 

- ROBOTSTXT_OBEY  --> Set this to FALSE as otherwise Scrapy won't run.

- DOWNLOAD_DELAY & RANDOMIZE_DOWNLOAD_DELAY --> Make sure these have been commented out as you
                don't need them when using Scraper API.


"""

API_KEY = 'YOUR_API_KEY'


class QuotesSpider(scrapy.Spider):
    name = "proxy_port_spider"

    def start_requests(self):
        meta = {
            "proxy": f"http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001"
            }

        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta=meta)

    def parse(self, response):
        """
        Insert the parsing code for your use case here...
        """
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }