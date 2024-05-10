from bs4 import BeautifulSoup
from utils import url_Manager
import re
import requests

pattern = r'^http://www.crazyant.net/\d+.html$'
root_url = "http://www.crazyant.net/"

urls = url_Manager.Urlmanager()
urls.add_new_url(root_url)
print(urls.new_urls)

fout = open("craw_all_pages.txt","w")
while urls.has_new_url():
    curr_url = urls.get_url()
    print(f"current is {curr_url}")
    r = requests.get(curr_url,timeout = 3)
    if(r.status_code != 200):
        print("erro, status code wrong!",curr_url)
        continue
    soup = BeautifulSoup(r.text,"html.parser")
    title = soup.title.string
    print(f"title is {title}")
    fout.write("%s\t%s\n"%(curr_url,title))
    fout.flush()  #立即写入而非先缓存最后写入
    links = soup.find_all("h2",class_="entry-title")
    print(links)
    for link in links:
        sb = link.find("a")
        href = sb["href"]
        print("href is",href)
        if href is None:
            continue
        if re.match(pattern, href):
            print("match!")
            urls.add_new_url(href)
            print(urls.new_urls)

fout.close()


