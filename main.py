import requests
from bs4 import BeautifulSoup
from newspaper import Article
from tqdm import tqdm
import pandas as pd


def repeatitive(links, urls):
    for link in links:
        if link.a['href'] in urls :
            return True
    return False


def scrap_year(year : int):
    page = 95
    scrap_data = []
    url_list = []
    while True:
        main_page_url = f"https://www.ana.press/page/archive.xhtml?mn=3&wide=0&dy=13&ms=0&pi={page}&yr={year}"
        page += 1

        html = requests.get(main_page_url).text
        soup = BeautifulSoup(html, features='lxml')
        links = soup.find_all('h3')

        if repeatitive(links, url_list):
            break

        for link in tqdm(links):
            page_url = "https://www.ana.press/" + link.a['href']
            url_list.append(link.a['href'])
            try:
                article = Article(page_url)
                article.download()
                article.parse()
                scrap_data.append({"url": page_url,
                                   "title": article.title ,
                                   "text": article.text})
            except:
                print(f"Failed to process page : {page_url}")

    df = pd.DataFrame(scrap_data)
    df.to_csv(f'ana-{page-1}.csv')


if __name__ == '__main__':
    scrap_year(1401)
