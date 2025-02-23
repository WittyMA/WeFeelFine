import scrapy
from scrapy.crawler import CrawlerProcess

class FeelingSpider(scrapy.Spider):
    name = "feeling_spider"
    start_urls = [
        "https://www.facebook.com/posts",  # Replace with real URLs
    ]

    def parse(self, response):
        for post in response.css("div.post"):
            yield {
                "url": post.css("a::attr(href)").get(),
                "content": post.css("p::text").getall(),
                "author": post.css("span.author::text").get(),
                "date": post.css("span.date::text").get()
            }

# Run the crawler (test)
if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEED_FORMAT": "json",
        "FEED_URI": "output.json"
    })
    process.crawl(FeelingSpider)
    process.start()