# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
from scrapy.utils.markup import remove_tags

class RecipesPipeline:
    def process_item(self, item, spider):
        item['name'] = item.get('name')[0]
        item['products'] = item.get('products')
        #item['qty'] = item.get('qty')
        item['description'] = item.get('description')

        return item

class DatabasePipeline:
	conn = sqlite3.connect('recipes.db')
	cursor = conn.cursor()
	couter = 1
	product_counter = 1
	products = []

	def open_spider(self, spider):
		pass

	def process_item(self, item, spider):

		name = item['name']
		print("""insert into recipes values (?, ?)""", (self.couter, name))
		self.cursor.execute("""insert into recipes values (?, ?)""", (self.couter, name))

		description_counter = 1
		for description in item['description']:
			#print("""insert into order values (?, ?, ?)""", (self.couter, description_counter, remove_tags(description)))
			self.cursor.execute("""insert into recipes_order values (?, ?, ?)""", (self.couter, description_counter, remove_tags(description).strip()))
			description_counter+=1	

		for product_and_qty in item['products']:
			data = remove_tags(product_and_qty).split('-')
			product = data[0].strip()
			try:
				qty = data[1].strip()
			except:
				qty = 'На вкус'
								
			if product not in self.products:
				self.products.append(product)
				self.cursor.execute("""insert into products values (?, ?)""", (self.product_counter, product))
				self.product_counter+=1
			self.cursor.execute("""insert into main values (?, (select distinct id from products where name = ?), ?)""", (self.couter, product, qty))

		self.couter+=1

		return item

	def close_spider(self, spider):
		self.conn.commit()
		self.cursor.close()
		self.conn.close()