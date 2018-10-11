import sqlite3

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

from epapers.settings import SQLITE_DB_NAME


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):

        assert "id" in item.keys()
        conn = sqlite3.connect(SQLITE_DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM epapers WHERE id= (?) ", (item["id"],))
        if cursor.fetchone():
            for image_url in item['thumb']:
                yield scrapy.Request(image_url)
            cursor.execute('INSERT INTO epapers VALUES (?)', (item['id'],))
            conn.commit()
        else:
            raise DropItem("Already uploaded")
        cursor.close()

    # def item_completed(self, results, item, info):
    #     image_paths = [x['path'] for ok, x in results if ok]
    #     if not image_paths:
    #         raise DropItem("Item contains no images")
    #     item['image_paths'] = image_paths
    #     return item
