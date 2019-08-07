# encoding=utf-8

# Created by max on 9/29/18

import os
import sys
import time
import re
import json

import requests
from bs4 import BeautifulSoup

import pandas as pd
from pandas import Series, DataFrame

# 长沙市高校毕业生租房和生活补贴拟发放名单（第十四批 2018 年 9 月）
url = "http://www.cshr.com.cn/csrcwhr/cjcx/rcxz.aspx"
params = {"kscode": None}
data = {"__EVENTTARGET": "AspNetPager1",
        "__EVENTARGUMENT": 1}

url_summary = "http://www.cshr.com.cn/hd/csxz22/xzzxlist.ashx"
params_summary = {"size": 20,
                  "page": 1,
                  "str": 9201}

# url_detail = "http://www.cshr.com.cn/hd/csxz22/rcxz22detail.html"
url_detail = "http://www.cshr.com.cn/hd/csxz22/detail.ashx"
params_detail = {"id": None}

HEAD_GRUADUATE = "长沙市高校毕业生"


def parse_summary():
    global params_detail

    response = requests.post(url_summary, params_summary)
    news = response.json()

    for n in news:
        newsLink = n["newsLink"]
        newsTitle = n["newsTitle"]
        newsAddTime = n["newsAddTime"]

        # Only search the name list page
        if HEAD_GRUADUATE in newsTitle:
            params_detail["id"] = newsLink
            parse_detail()


def parse_detail():
    response = requests.post(url_detail, params_detail)
    detail = response.json()[0]
    nr = detail["nr"]
    date_news = detail["tjsj"]

    soup = BeautifulSoup(nr, "html5lib")
    links = soup.find_all("a")
    kscode = links[0].attrs["href"].split("=")[-1]

    get_graduates(kscode, date_news)


class Graduate():
    """
    Init with:

    g = Graduate(*data_list)
    """

    def __init__(self, _, name, id, gender, date_immigrate, degree, university, date_graduate, company):
        self.name = name
        self.id = id
        self.gender = gender
        self.data_immigrate = date_immigrate
        self.degree = degree
        self.university = university
        self.date_graduate = date_graduate
        self.company = company

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def get_graduate(soup):
    """Get graduates in one page.

    Args:
        soup (BeautifulSoup): From get_get_graduates function.

    Returns:

    """
    table = soup.find("table", id="list1")
    trs = table.find_all("tr")

    header = [td.text.strip() for td in trs.pop(0).find_all("td")][1:]
    data_graduates = []

    for tr in trs:
        texts = [td.text.strip() for td in tr.find_all("td")][1:]
        data_graduates.append(texts)

    return header, data_graduates


def get_graduates(kscode, date_news):
    """Get all graduates in a link.
    like http://www.cshr.com.cn/csrcwhr/cjcx/rcxz.aspx?kscode=368

    Args:
        kscode (int): From detail page.
        date_news (str): As part of file name.

    Returns:

    """
    global params
    global data

    data_g = []
    params["kscode"] = kscode

    print("\nDate: ", date_news)

    total_pages = 0
    response = requests.post(url, params, data)
    soup = BeautifulSoup(response.text, "html5lib")
    div = soup.find("div", id="AspNetPager1")
    total_pages = int(div.find("div").text.split("页")[0][3:])

    for i in range(1, total_pages + 1):
        print("    Page: ", i)

        data["__EVENTARGUMENT"] = i
        response = requests.post(url, params, data)
        soup = BeautifulSoup(response.text, "html5lib")

        # get data in one page
        header, data_graduates = get_graduate(soup)

        data_g.extend(data_graduates)

    df = DataFrame(data_g, columns=header)
    df.to_csv("".join(["graduates_", date_news, ".csv"]), index=False)


def get_abroads():
    pass


def get_skills():
    pass


def get_doctorals():
    pass


def main(args):
    parse_summary()


if __name__ == "__main__":
    start = time.time()
    print("Start: " + str(start))

    main(sys.argv[1:])

    elapsed = (time.time() - start)
    print("Used {0:0.3f} seconds".format(elapsed))
