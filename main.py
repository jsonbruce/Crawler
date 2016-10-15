# coding=utf-8

import requests
from bs4 import BeautifulSoup
import pandas as pd
import pprint

target = "https://yz.chsi.com.cn/bsbm/cjcx/cjcxAction.do;jsessionid=7FB1E4EBDF2EF84BB972734E1DC37CDA"
params = {
    "bkdwdm": 90002,
    "xm": "",
    "zjhm": "",
    "ksbh": ""
}

xdata_path = "data/xdata.all.xls"
result = []


def parser(params):
    response = requests.post(target, params)
    if response.status_code == 200:
        rt = response.text

        r = {}
        soup = BeautifulSoup(rt, "html")
        table = soup.find("table", {"class": "cjtable"})

        for row in table.findAll("tr"):
            cells = row.findAll("td")

            if len(cells) == 2:
                r[cells[0].getText(strip=True).translate(dict.fromkeys(range(32)))] = cells[1].getText(
                    strip=True).translate(dict.fromkeys(range(32)))

        if len(r) > 1:
            result.append(r)


def main():
    xdata = pd.read_excel(xdata_path, sheetname="Sheet1")

    for d in xdata.itertuples():
        params["xm"] = d[2]
        params["zjhm"] = d[4]

        parser(params)

        # pprint.pprint(result)


if __name__ == '__main__':
    main()

    with open("result", "w+") as r:
        r.write(str(result))
