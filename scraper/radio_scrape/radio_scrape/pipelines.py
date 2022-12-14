# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from radio_scrape.etc_MySQL import MySQL

import requests
from slugify import slugify


class SaveEpisode:
    def process_item(self, episode, spider):
        print(episode, "\n\n")
        mySQL = MySQL()
        mySQL.insert_episode(episode)
        return episode

class GetFileSize:
    def process_item(self, episode, spider):
        header = requests.head(episode['mp3'], stream=True).headers
        if 'Content-length' in header.keys():
            episode['file_size'] = header['Content-length']
        else:
            # 0 recomended when file size unknown (https://validator.w3.org/feed/docs/error/UseZeroForUnknown.html) 
            episode['file_size'] = 0
        
        return episode

class ShowSlug:
    def process_item(self, show, spider):
        slug = slugify(f"{show['source']}-{show['showName']}")
        show['slug'] = slug
        return show


class SaveShow:
    def process_item(self, show, spider):
        mySQL = MySQL()
        mySQL.insert_show(show)
        return show
