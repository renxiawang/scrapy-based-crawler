# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AnimePipeline(object):

    def process_item(self, item, spider):
        if u"us_info" in item:
            for (k, v) in item[u"us_info"].items():
                if v is None or v == []:
                    del item[u"us_info"][k]

        if u"jp_info" in item:
            for (k, v) in item[u"jp_info"].items():
                if v is None or v == []:
                    del item[u"jp_info"][k]

        return item
