import scrapy
import json
from datetime import datetime

class FeelingSpider(scrapy.Spider):
    name = "feeling_spider"
    
    # Multi-platform crawling
    custom_settings = {
        'CONCURRENT_REQUESTS': 4,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json'
    }

    def start_requests(self):
        # Blog platforms
        platforms = [
            'https://medium.com/tag/emotions/archive/',
            'https://www.blogger.com/search?q=I%20feel'
        ]
        for url in platforms:
            yield scrapy.Request(url=url, callback=self.parse_blog)

        # Twitter API integration
        yield scrapy.Request(
            url="https://api.twitter.com/2/tweets/search/recent?query=I%20feel",
            headers={"Authorization": f"Bearer {self.settings.get('TWITTER_BEARER_TOKEN')}"},
            callback=self.parse_tweets
        )

    def parse_blog(self, response):
        for post in response.css('article.post'):
            yield {
                'content': post.css('div.post-content ::text').getall(),
                'author': post.css('span.author-name ::text').get(),
                'date': datetime.now().isoformat(),
                'platform': 'blog'
            }

    def parse_tweets(self, response):
        data = json.loads(response.text)
        for tweet in data.get('data', []):
            yield {
                'content': [tweet['text']],
                'author': tweet['author_id'],
                'date': tweet['created_at'],
                'platform': 'twitter'
            }