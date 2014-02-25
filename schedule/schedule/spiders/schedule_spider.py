from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from schedule.items import ScheduleItem


class ScheduleSpider(CrawlSpider):
    name = "schedule"
    allowed_domains = ["espn.go.com"]
    start_urls = ["http://espn.go.com/nba/schedule/_/date/20140223"]

    rules = (
        Rule(
            SgmlLinkExtractor(
                allow=(r'http://espn\.go\.com/nba/boxscore\?id=.*',)),
            callback='parse_result'),
        Rule(SgmlLinkExtractor(allow=(r'.*',), restrict_xpaths=(
            "//div[@class=\"floatleft\"]/a[1]",)), callback='parse_item', follow=True),
    )

    # parse schedule on the http://espn.go.com/nba/schedule/_/date/xxx pages
    # which are not start yet
    def parse_item(self, response):
        sel = Selector(response)

        tables = sel.xpath("//*[@id=\"my-teams-table\"]/div[1]/div/table")
        for table in tables:
            # no game scheduled table
            no_game = table.xpath("tr[@class=\"evenrow\"]/td/text()")
            if len(no_game) == 1:
                continue
            # finished_game
            finished_game = table.xpath("tr[2]/td[1]/text()").extract()
            if len(finished_game) == 1 and finished_game[0] == u"RESULT":
                continue
            # game scheduled table
            try:
                game_date = table.xpath(
                    "tr[1]/td/text()").extract()[0].split(',')[1].strip()
                table_rows = table.xpath("tr[position()>2]")
                for row in table_rows:
                    game = ScheduleItem()
                    game['date'] = game_date

                    if row.xpath("td[1]/a[2]/text()|td[1]/a[1]/text()").extract() == []:
                        continue

                    game['home'] = row.xpath("td[1]/a[2]/text()").extract()[0]
                    game['away'] = row.xpath("td[1]/a[1]/text()").extract()[0]
                    game['time'] = row.xpath(
                        "td[2]/text()|td[2]/a/text()").extract()[0] + ' ET'
                    yield game
            except Exception, e:
                raise e

    def parse_result(self, response):
        sel = Selector(response)

        game = ScheduleItem()

        try:
            datetime = sel.xpath(
                "//*[@id=\"gamepackageTop\"]/div[4]/div/p[1]/text()").extract()[0]

            game['time'] = datetime.split(',')[0]
            game['date'] = (','.join(datetime.split(',')[1:])).strip()
            game['away'] = sel.xpath(
                "//*[@id=\"gamepackageTop\"]/div[5]/div[2]/p[2]/span/text()").extract()[0].strip(': ')
            game['home'] = sel.xpath(
                "//*[@id=\"gamepackageTop\"]/div[5]/div[2]/p[3]/span/text()").extract()[0].strip(': ')

            yield game
        except Exception, e:
            raise e
