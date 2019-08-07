# coding=utf-8

import os, re, csv, collections
import requests, json
from bs4 import BeautifulSoup

from app.models import PageInfo

URL_HOST = "http://cy.ncss.org.cn"
URL_ALL = "http://cy.ncss.org.cn/search.html"
URL_SEARCH = "http://cy.ncss.org.cn/search.html?isAjax=true"
CODE_HUNAN = 430000


def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__,
                      sort_keys=True, indent=4)


class ProjectView():
    def __init__(self, name=None, university=None, product_types=None, description=None, detail_url=None):
        self.name = name
        self.university = university
        if product_types is None:
            self.product_types = []
        else:
            self.product_types = product_types
        self.description = description
        self.detail_url = detail_url

    def to_json(self):
        return {
            "name": self.name,
            "university": self.university,
            "product_types": self.product_types,
            "description": self.description,
            "detail_url": self.detail_url
        }


def download():
    try:
        data = {
            "ecCode": "CYDS_2TH",
            "search_EQ_projectIndustryLevelOneId": "",
            "search_EQ_investStageCode": "",
            "search_LIKE_typeCode": "",
            "search_EQ_wasBindUniTechnology": "",
            "search_LIKE_wasEquityStructure": "",
            "search_EQ_locationCode": "",
            "search_LIKE_name": "",
            "ec_p": 1,
            "p": "page"
        }

        if not os.path.exists("download"):
            os.mkdir("download")

        for page in range(1, 1000):
            raw = str(page) + ".html"
            data["ec_p"] = page
            response = requests.post(URL_SEARCH, data=data)
            if response.status_code != 200:
                break
            with open("download/" + raw, "w") as f:
                f.write(response.content)

    except Exception as e:
        print e


def parse_li_contents(file):
    soup = BeautifulSoup(open(file))
    body_contents = soup.body.contents
    li_contents = []

    for cs in body_contents:
        try:
            if cs is not None and str(cs).startswith("<li>"):
                li_contents.append(cs)
        except Exception as e:
            print e.message

    return li_contents


def parse_project_view(li):
    project = ProjectView()

    names = li.select(".name")[0]
    project.name = names.get_text(strip=True).encode("utf-8")
    project.detail_url = URL_HOST + names.next_element["href"]
    project.university = li.select(".tits")[0].get_text(strip=True).encode("utf-8")
    project.description = li.select(".link")[0].get_text(strip=True).encode("utf-8")
    for t in li.select(".one"):
        project.product_types.append(t.get_text(strip=True).encode("utf-8"))

    return project


def parse_pageinfo(content):
    soup = BeautifulSoup(content)
    scripts = soup.select("script")
    script_contents = scripts[-1].get_text()
    pageInfoJson = re.compile(r"\{.*(\};)*").search(script_contents).group().translate(dict.fromkeys(range(32)))
    try:
        pageInfoJson = json.JSONDecoder().decode(pageInfoJson[:-1])
        pageInfo = PageInfo(pageInfoJson)
        return pageInfo
    except Exception as e:
        print e


def response_json():
    projects = []
    with open("result.json", "w+") as f:
        for parent, dirs, files in os.walk("download/"):
            for raw in files:
                li_contents = parse_li_contents(os.path.join(parent, raw))

                for li in li_contents:
                    project = parse_project_view(li)
                    projects.append(project)

        result = toJSON(projects)
        f.write(result.encode("utf-8"))


def response_csv():
    with open("result.csv", "a") as f:
        fieldnames = ["name", "university", "product_types", "description", "detail_url"]
        resultFile = csv.DictWriter(f, fieldnames=fieldnames, dialect="excel")
        resultFile.writeheader()

        for parent, dirs, files in os.walk("download/"):
            for raw in files:
                li_contents = parse_li_contents(os.path.join(parent, raw))

                for li in li_contents:
                    project = parse_project_view(li)

                    data = {
                        "name": project.name,
                        "university": project.university,
                        "product_types": project.product_types,
                        "description": project.description,
                        "detail_url": project.detail_url
                    }
                    resultFile.writerow(data)


def crawl():
    try:
        data = {
            "ecCode": "CYDS_2TH",
            "search_EQ_projectIndustryLevelOneId": "",
            "search_EQ_investStageCode": "",
            "search_LIKE_typeCode": "",
            "search_EQ_wasBindUniTechnology": "",
            "search_LIKE_wasEquityStructure": "",
            "search_EQ_locationCode": "",
            "search_LIKE_name": "",
            "ec_p": 1,
            "p": "page"
        }

        response = requests.post(URL_SEARCH, data=data)

        pageInfo = parse_pageinfo(response.content)
        if PageInfo is not None:
            for p in pageInfo.pageResults:
                p.add(p)

            for page in range(2, pageInfo.totalPage + 1):
                data["ec_p"] = page
                response = requests.post(URL_SEARCH, data=data)
                if response.status_code != 200:
                    break

                pageInfo = parse_pageinfo(response.content)
                if pageInfo is not None:
                    for p in pageInfo.pageResults:
                        p.add(p)


    except Exception as e:
        print e


if __name__ == '__main__':
    pass
