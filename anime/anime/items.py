# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

# info = {
#     title,
#     released,
#     dates,
#     company,
#     creator,
#     director,
#     genre,
#     similar,
#     related,
#     characters
# }
class AnimeItem(Item):
    url = Field()
    image = Field()
    us_info = Field()
    jp_info = Field()
    description = Field()
    pass

