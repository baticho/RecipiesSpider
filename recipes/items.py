# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipesItem(scrapy.Item):
    name = scrapy.Field()
    products = scrapy.Field()
    #qty = scrapy.Field()
    description = scrapy.Field()