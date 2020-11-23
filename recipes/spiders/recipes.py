import scrapy

from scrapy.loader import ItemLoader
from recipes.items import RecipesItem
from scrapy.linkextractors import LinkExtractor

class ParSpider(scrapy.Spider):
    name = 'recepti'
    start_urls = ['https://recepti.gotvach.bg/?s=1,8']

    #receptions_page = LinkExtractor(restrict_xpaths='//div[@class="prevgrid mod"]/div/a[@class="title"]/@href')


    def parse(self, response):

        recipes_page_links = response.xpath('//div[@class="prevgrid mod"]/div/a[@class="title"]/@href')
        yield from response.follow_all(recipes_page_links, self.parse_name)

        pagination_links = response.xpath('//div[@class="pagination"]/a[@class="next"]/@href')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_name(self, response):

        
        name = response.xpath("//h1/text()").get()   
        products = response.xpath("//section/ul/li").getall()
        #qty = response.xpath("//section/ul/li/text()").getall()
        description = response.xpath("//p[@class='desc']").getall()

        item = ItemLoader(item=RecipesItem(), response=response)
        item.add_value('name', name )
        item.add_value('products', products )
        #item.add_value('qty', qty )
        item.add_value('description', description )
        

        return item.load_item()