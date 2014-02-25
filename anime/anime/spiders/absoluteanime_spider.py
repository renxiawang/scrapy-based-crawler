#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from anime.items import AnimeItem


class AbsoluteAnimeSpider(CrawlSpider):
    name = "absoluteanime"
    allowed_domains = ["www.absoluteanime.com"]
    start_urls = [
        "http://www.absoluteanime.com/anime.html?page=0"
        "http://www.absoluteanime.com/anime.html?page=a",
        "http://www.absoluteanime.com/anime.html?page=b",
        "http://www.absoluteanime.com/anime.html?page=c",
        "http://www.absoluteanime.com/anime.html?page=d",
        "http://www.absoluteanime.com/anime.html?page=e",
        "http://www.absoluteanime.com/anime.html?page=f",
        "http://www.absoluteanime.com/anime.html?page=g",
        "http://www.absoluteanime.com/anime.html?page=h",
        "http://www.absoluteanime.com/anime.html?page=i",
        "http://www.absoluteanime.com/anime.html?page=j",
        "http://www.absoluteanime.com/anime.html?page=k",
        "http://www.absoluteanime.com/anime.html?page=l",
        "http://www.absoluteanime.com/anime.html?page=m",
        "http://www.absoluteanime.com/anime.html?page=n",
        "http://www.absoluteanime.com/anime.html?page=o",
        "http://www.absoluteanime.com/anime.html?page=p",
        "http://www.absoluteanime.com/anime.html?page=q",
        "http://www.absoluteanime.com/anime.html?page=r",
        "http://www.absoluteanime.com/anime.html?page=s",
        "http://www.absoluteanime.com/anime.html?page=t",
        "http://www.absoluteanime.com/anime.html?page=u",
        "http://www.absoluteanime.com/anime.html?page=v",
        "http://www.absoluteanime.com/anime.html?page=w",
        "http://www.absoluteanime.com/anime.html?page=x",
        "http://www.absoluteanime.com/anime.html?page=y",
        "http://www.absoluteanime.com/anime.html?page=z"
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=(r'.*',), restrict_xpaths=(
            "//*[@class=\"aa_section\"]/div[3]/table/tr/td[2]/a",)), callback='parse_item'),
    )

    def parse_item(self, response):
        sel = Selector(response)
        info_section = sel.xpath(
            "//*/div[@class=\"aa_section_content aa_section_profile\"]/table/tr[position()>1]")
        anim_section = sel.xpath(
            "//*/div[@class=\"aa_section_content aa_section_anime\"]/table/tr[position()>1]")
        char_section = sel.xpath(
            "//*/div[@class=\"aa_section_content aa_section_characters\"]/table/tr[position()>1]")
        desc_section = sel.xpath(
            "//*/div[@class=\"aa_section_content aa_section_description\"]")

        anime = AnimeItem()
        anime[u"url"] = response.url
        img_file = sel.xpath(
            "//*/div[@class=\"aa_section_content aa_section_profile\"]/table/tr[2]/td[position()=2 or position()=3]/a/@href").extract()[0]
        anime[u"image"] = re.sub(r"index.*htm", img_file, response.url)

        anime[u"us_info"], anime[u"jp_info"] = self.parse_infos(info_section)
        anime[u"us_info"][u"related"], anime[u"jp_info"][u"related"] = self.parse_animes_or_chars(
            anim_section, anime[u"url"], section_type="anime")
        anime[u"us_info"][u"characters"], anime[u"jp_info"][
            u"characters"] = self.parse_animes_or_chars(char_section, anime[u"url"], section_type="chars")
        anime[u"description"] = self.parse_desc(desc_section)

        return anime

    def parse_infos(self, info_section):
        # infos = [InfoItem(), InfoItem()] # ius_info, jp_info
        infos = [dict(), dict()]  # ius_info, jp_info

        # record last field name if current field name is "· · ·"
        last_field = ''

        for row in info_section:  # for each row in table
            current_field = row.xpath("th/div/text()").extract()[0].lower()

            # complete characters is in char_section
            if current_field == u"characters":
                break

            for (count, col) in enumerate(row.xpath("td")):
                value = col.xpath("text()|a/text()").extract()

                if current_field != u"· · ·":
                    if value != [] and value[0] != u"\xa0":
                        if current_field == "company" or current_field == "genre":
                            value = re.split(r", |/", ''.join(value))
                        infos[count][current_field] = value

                    last_field = current_field
                else:
                    if value == [] or value[0] == u"\xa0":
                        # empty value
                        continue
                    elif infos[count].get(last_field, None) != None:
                        # extend new list of values to existing list
                        existed_values = infos[count][last_field]
                        existed_values.extend(value)
                        infos[count][last_field] = existed_values
                    else:
                        infos[count][last_field] = value

        return infos[0], infos[1]

    def parse_animes_or_chars(self, section, base_url, section_type="chars"):
        '''
        parse related anime section or characters section
        '''
        if section == None:
            return None

        if section_type == 'chars':
            url_pattern = r"index.*htm"
        else:
            url_pattern = r"[a-zA-Z0-9\-_]*/index.*htm"

        us_items = []
        jp_items = []

        for row in section:
            if row.xpath("td[1]/text()|td[1]/a/text()").extract() != [] and \
                    row.xpath("td[1]/text()|td[1]/a/text()").extract()[0] != u"\xa0" and \
                    row.xpath("td[2]/text()|td[2]/a/text()").extract() != [] and \
                    row.xpath("td[2]/text()|td[2]/a/text()").extract()[0] != u"\xa0":

                us_item = {}
                jp_item = {}

                # us_name
                us_item[u"name"] = row.xpath(
                    "td[1]/text()|td[1]/a/text()").extract()[0]
                # jp_name
                jp_item[u"name"] = row.xpath(
                    "td[2]/text()|td[2]/a/text()").extract()[0]

                if row.xpath("td[1]/a/@href").extract() != []:  # url
                    url_file = row.xpath(
                        "td[1]/a/@href").extract()[0].strip("../")
                    url = re.sub(url_pattern, url_file, base_url)
                    us_item[u"url"] = url
                    jp_item[u"url"] = url

                us_items.append(us_item)
                jp_items.append(jp_item)

            if row.xpath("td[3]/text()|td[3]/a/text()").extract() != [] and \
                    row.xpath("td[3]/text()|td[3]/a/text()").extract()[0] != u"\xa0" and \
                    row.xpath("td[4]/text()|td[4]/a/text()").extract() != [] and \
                    row.xpath("td[4]/text()|td[4]/a/text()").extract()[0] != u"\xa0":

                us_item = {}
                jp_item = {}

                # us_name
                us_item[u"name"] = row.xpath(
                    "td[3]/text()|td[3]/a/text()").extract()[0]
                # jp_name
                jp_item[u"name"] = row.xpath(
                    "td[4]/text()|td[4]/a/text()").extract()[0]
                if row.xpath("td[3]/a/@href").extract() != []:
                    url_file = row.xpath(
                        "td[3]/a/@href").extract()[0].strip("../")
                    url = re.sub(url_pattern, url_file, base_url)
                    us_item[u"url"] = url
                    jp_item[u"url"] = url

                us_items.append(us_item)
                jp_items.append(jp_item)

        return us_items, jp_items

    def parse_desc(self, desc_section):
        if desc_section == None:
            return None

        desc = []

        for sec in desc_section:
            text = "\n".join(
                sec.xpath("p[@class!=\"aa_section_footer\" or not(@class)]/text()").extract())
            desc.append(text)

        return desc
