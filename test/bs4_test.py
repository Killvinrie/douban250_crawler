from bs4 import BeautifulSoup

with open("./test.html",encoding = "utf-8")as file:
    html_doc = file.read()

soup = BeautifulSoup(html_doc, "html.parser")

links = soup.find_all('a')

print(type(links))

for link in links:
    print(link.name,link["href"],link.get_text())