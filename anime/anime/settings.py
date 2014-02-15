# Scrapy settings for anime project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'anime'

SPIDER_MODULES = ['anime.spiders']
NEWSPIDER_MODULE = 'anime.spiders'

ITEM_PIPELINES = {
    'anime.pipelines.AnimePipeline': 300,
    'scrapy_mongodb.MongoDBPipeline': 800,
}

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'anime'
MONGODB_COLLECTION = 'absoluteanime'

MONGODB_UNIQUE_KEY = u'url'
# MONGODB_ADD_TIMESTAMP = True
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'anime (+http://www.yourdomain.com)'
