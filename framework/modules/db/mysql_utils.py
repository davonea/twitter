#!/usr/bin/env python
# -*- coding: utf-8 -*-

from framework.modules.db.mysql_conn import MyPymysqlPool
from framework.modules.bases.log import *


@singleton
class MysqlUtils():
    def __init__(self):
        self.mysql = MyPymysqlPool("mysql")


    @log("mysql")
    def add_article(self, article):

        ssql = "select a.article_id from article a where url='{}';".format(article["url"])
        logger().info("".format(article["url"]))
        logger().info("sql：{}".format(ssql))
        one = self.mysql.getOne(ssql)
        if not one:
            c = ""
            v = ""
            values = []
            for k, value in article.items():
                c += "{},".format(k)
                v += "%s,"
                if k == "date":
                    values.append(value)
                    continue
                values.append(str(value))

            isql = "insert into article ({}) VALUES({});".format(c[0:-1], v[0:-1])
            # isql = isql.replace('{}'.format(article["date"]), 'str_to_date("{}","%Y-%m-%d")'.format(article["date"]))
            # article["date"] = ''
            logger().info("sql：{}".format(isql))
            result = self.mysql.insert(isql, values)
            logger().info("{}".format(result, article))
        else:
            logger().warning("url {}".format(article["url"]))

    @log("mysql")
    def add_site(self, site):

        ssql = "select a.site_id from site a where site_name_en='{}';".format(site["site_name_en"])
        logger().info("{}".format(site["site_name_en"]))
        logger().info("sql：{}".format(ssql))
        one = self.mysql.getOne(ssql)
        if not one:
            isql = "insert into site ({}) VALUES({});".format(",".join([k for k in site.keys()]),
                                                                 str(',%s' * len(site))[1:])
            values = [v for v in site.values()]
            logger().info("sql：{}， values：{}".format(isql, values))
            result = self.mysql.insert(isql, values)
            logger().info("{}".format(result, site))
        else:
            logger().warning("site{}".format(site["site_name_en"]))

    @log("mysql")
    def get_site_info(self, site_name_en):
        ssql = "select a.author_xpath, a.date_xpath, a.content_xpath from site a where site_name_en='{}';".format(site_name_en)
        logger().info("{}，sql：{}".format(site_name_en, ssql))
        site = self.mysql.getOne(ssql)
        r = {}
        if not site:
            logger().warning("{}".format(site_name_en))
            return False

        r["author_xpath"] = site[0]
        r["date_xpath"] = site[1]
        r["content_xpath"] = site[2]
        return r


def main():
    mysql = MysqlUtils()
    import datetime
    datetime.date.today()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    print(date)
    article = {"site_name_en": "bbc", "description_en": "this is test msg!", 'author': 'ayue', 'title_en': 'test',
               "title_zh": '', "url": "www.bbc.com", "date": "2021-10-21"}
    mysql.add_article(article)

    # mysql.get_site_info("bbc")

if __name__ == '__main__':
    main()