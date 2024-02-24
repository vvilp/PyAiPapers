import requests
import re
from pathlib import Path
from bs4 import BeautifulSoup

url="https://papers.nips.cc"
html_text = requests.get(f"{url}/paper_files/paper/2023").text
soup = BeautifulSoup(html_text, "html.parser")
Path("./papers").mkdir(parents=True, exist_ok=True)
# print(len(soup.find_all("li", {"class": "conference"})))
for idx, paper_li in enumerate(soup.find_all("li", {"class": "conference"})):
    try:
        a = paper_li.find("a")
        print(a["href"])
        paper_page = requests.get(f'{url}{a["href"]}')
        paper_soup = BeautifulSoup(paper_page.text, "html.parser")
        title = paper_soup.find("h4").text
        title = re.sub("[^a-zA-Z -]+", "", title)
        for paper_a in paper_soup.find_all("a"):
            if paper_a["href"].endswith(".pdf"):
                paper_pdf = requests.get(f'{url}{paper_a["href"]}')
                with open(f"papers/{title}.pdf", "wb") as f:
                    f.write(paper_pdf.content)
        print(f"Fetched: {title}.pdf")
    except Exception as e:
        print(e)
    if idx == 100:
        break
