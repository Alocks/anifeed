from lxml import etree

from dataclasses import dataclass
from datetime import datetime

from anifeed.utils.wranglers import get_toml_config
from anifeed.controllers.serializers.base_serializer import BaseSerializer


@dataclass
class RssFeedData:
    title: str
    link: str
    description: str


class RssSerializer(BaseSerializer):
    @property
    def output_format(self):
        return "xml"

    @property
    def feed_data(self):
        data = get_toml_config(table_name="rss-feed-data")
        return RssFeedData(
            title=data.get("TITLE"),
            link=data.get("LINK"),
            description=data.get("DESCRIPTION"))

    def serialize_animes(self) -> str:
        animes_list = self._animes_list
        rss = etree.Element('rss', version="2.0")
        channel = etree.SubElement(rss, 'channel')

        etree.SubElement(channel, 'title').text = self.feed_data.title
        etree.SubElement(channel, 'link').text = self.feed_data.link
        etree.SubElement(channel, 'description').text = self.feed_data.description
        etree.SubElement(channel, 'language').text = 'en-us'

        now = datetime.now()
        etree.SubElement(channel, 'lastBuildDate').text = now.strftime("%a, %d %b %Y %H:%M:%S +0000")

        for article in animes_list:
            item = etree.SubElement(channel, 'item')

            # Required Item Fields
            etree.SubElement(item, 'title').text = article['title']
            etree.SubElement(item, 'link').text = article['link']
            etree.SubElement(item, 'description').text = article['summary']

            # Unique identifier (GUID)
            etree.SubElement(item, 'guid', isPermaLink="true").text = article['link']

            # Publication Date
            pub_date = article.get('pubDate', now).strftime("%a, %d %b %Y %H:%M:%S +0000")
            etree.SubElement(item, 'pubDate').text = pub_date

        xml_string = etree.tostring(
            rss,
            encoding='utf-8',
            xml_declaration=True,
            pretty_print=True
        ).decode()

        return xml_string
