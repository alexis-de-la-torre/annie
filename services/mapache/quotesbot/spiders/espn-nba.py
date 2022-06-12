# -*- coding: utf-8 -*-
import re

import scrapy


class EspnNbaSpider(scrapy.Spider):
    name = "espn-nba"
    start_urls = [
        'https://espndeportes.espn.com/basquetbol/nba/calendario',
    ]

    def parse(self, response):
        for day in response.css("#fittPageContainer > div:nth-child(4) > div > div > section > div > div:nth-child(3) > div"):

            team_a_logo_link = day.css("div.Table__Scroller > table > tbody > tr > td.events__col.Table__TD > div > span > a:nth-child(1)::attr(href)")\
                .extract_first()

            team_a_logo_id = re.search('\_\/nombre\/(.+?)\/.*', team_a_logo_link).group(1)

            team_b_logo_link = day.css(
                "div.Table__Scroller > table > tbody > tr > td.colspan__col.Table__TD > div > span.Table__Team > a:nth-child(1)::attr(href)") \
                .extract_first()

            team_b_logo_id = re.search('\_\/nombre\/(.+?)\/.*', team_b_logo_link).group(1)

            yield {
                'date': day.css("div.Table__Title::text").extract_first(),
                'time': day.css("div.Table__Scroller > table > tbody > tr > td.date__col.Table__TD > a::text").extract_first(),
                'team-a-id': team_a_logo_id,
                'team-b-id': team_b_logo_id,
                'team-a': day.css("div.Table__Scroller > table > tbody > tr > td.events__col.Table__TD > div > span > a:nth-child(2)::text").extract_first(),
                'team-b': day.css("div.Table__Scroller > table > tbody > tr > td.colspan__col.Table__TD > div > span.Table__Team > a:nth-child(2)::text").extract_first(),
                'team-a-logo': f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/{team_a_logo_id}.png&h=500&w=500",
                'team-b-logo': f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/{team_b_logo_id}.png&h=500&w=500"
            }