from scrapy.selector import Selector
from scrapy.spider import Spider
from schedule.items import ScheduleItem


class NbaScheduleSpider(Spider):
    name = "nba_schedule"
    allowed_domains = ["nba.com"]
    start_urls = [
        "http://www.nba.com/schedules/national_tv_schedule/"
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath("//*[@id=\"scheduleMain\"]/table//tr[not(@class)]")
        items = []
        date = ""  # record the date for a group of games

        for site in sites:
            item = ScheduleItem()
            item['date'] = site.xpath("td[@class=\"dt\"]/text()").extract()[0]

            if item['date'] == u" ":
                item['date'] = date
            else:
                date = item['date']

            item['home'] = site.xpath(
                "td[@class=\"gm\"]/a[2]/text()").extract()[0]
            item['away'] = site.xpath(
                "td[@class=\"gm\"]/a[1]/text()").extract()[0]
            item['time'] = site.xpath("td[@class=\"tm\"]/text()").extract()[0]
            items.append(item)

        return items
