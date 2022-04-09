from flask import Flask
#!/usr/bin/python3
import pywikibot
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')

def hello():
    site = pywikibot.Site("en", "wikipedia")

    president_list = ["Joe Biden", "Donald Trump", "Barack Obama", "George W. Bush", "Bill Clinton"]
    # print(president_list)
    pageContent = "<table border=1 align=center ><tr><th colspan=5><h1>Last Five US Presidents</h1></th></tr>"
    pageContent = pageContent + "<tr><th align=center width=4% >#<th>Name<th> WikiData ID<th>Description<th>Image</tr>"
    i = 1
    for president in president_list:
        page = pywikibot.Page(site, president)
        code = str(pywikibot.ItemPage.fromPage(page))
        Qcode = code[11:-2]
        WDUrl = "https://www.wikidata.org/wiki/" + Qcode
        webpage = urlopen(WDUrl).read()
        soup = BeautifulSoup(webpage)
        title = soup.find("meta", property="og:title")
        description = soup.find("meta", property="og:description")
        image = soup.find("meta", property="og:image")
        fname = title["content"] + ".jpg"
        urlretrieve(image["content"], fname)
        pageContent = pageContent + "<tr><td>" + str(i) + "<td>" + title["content"] + "<td align=center>" + Qcode + "<td>" + description["content"] + "<td>"
        pageContent = pageContent + "<img src=" + "\"" + image["content"] + "\"" + "width=\"100\" height=\"125\" ></tr>"
        i = i + 1
    pageContent = pageContent + "</table>"
    return pageContent

if __name__ == "__main__":
    app.run()