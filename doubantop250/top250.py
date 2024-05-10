import requests
import pprint
from bs4 import BeautifulSoup
from utils import url_Manager
import openpyxl
import pandas as pd

page_index = range(0, 250, 25)
lst = list(page_index)

htmls = []

def download_all_pages():  # return the list of the html content
    for idx in page_index:
        url = f"https://movie.douban.com/top250?start={idx}&filter="
        print("downloading this page", url)
        r = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
        print(r.status_code, "status_code")
        if r.status_code != 200:
            raise Exception("error")
        htmls.append(r.text)
    return htmls


htmls = download_all_pages()
# print(len(htmls))



def parse_single_html(html):
    datas = []
    soup = BeautifulSoup(html, "html.parser")
    article_items = (
        soup.find("div", class_="article")
        .find("ol", class_="grid_view")
        .find_all("div", class_="item")
    )
    for article_item in article_items:
        rank = article_item.find("div", class_="pic").find("em").get_text()
        info = article_item.find("div", class_="info")
        title = info.find("div", class_="hd").find("span", class_="title").get_text()
        stars = info.find("div", class_="bd").find("div", class_="star").find_all("span")
        rating = stars[0]["class"][0]
        rating_num = stars[1].get_text()
        comment = stars[3].get_text()

        datas.append({
            "rank": rank,
            "title": title,
            "rating": rating.replace("rating", "").replace("-t", ""),
            "rating_num": rating_num,
            "comments": comment.replace("人评价", "")
        })
    return datas


# pprint.pprint(parse_single_html(htmls[0]))

all_datas = []
for html in htmls:
    data = parse_single_html(html)
    print(len(data))
    all_datas.extend(data)

print(len(all_datas),"dataset")

df = pd.DataFrame(all_datas)
df.to_excel("douban_top250.xlsx")


