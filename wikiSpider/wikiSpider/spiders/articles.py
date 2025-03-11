from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ArticleSpider(CrawlSpider):
    name = "articles"
    start_urls = ["https://en.wikipedia.org/wiki/Benevolent_dictator_for_life"]
    allowed_domain = ["wikipedia.org"]
    rules = [
        Rule(
            LinkExtractor(r"(/wiki/)((?!:).)*$"),
            callback="parse_item",
            follow=True,
            cb_kwargs={"is_article": True},
        ),
        Rule(
            LinkExtractor(allow=r".*"),
            callback="parse_item",
            cb_kwargs={"is_article": False},
        ),
    ]

    def parse_item(self, response, is_article):
        title = response.css("span.mw-page-title-main::text").extract_first()
        if is_article:
            url = response.url
            text = response.xpath("//div[@id='mw-content-text']//text()").extract()
            lastUpdated = response.css("li#footer-info-lastmod::text").extract_first()
            lastUpdated = (
                lastUpdated.replace("This page was last edited on ", "").strip(".")
                if lastUpdated
                else ""
            )
            print(f"URL is: {url}")
            print(f"Title is: {title} ")
            print(f"Text is: {text}")
            print(f"Last updated: {lastUpdated}")
        else:
            print("This is not an article {}".format(title))
