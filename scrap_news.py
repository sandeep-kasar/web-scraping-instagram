import urllib.request
from bs4 import BeautifulSoup
import csv


class Scraper:
    def __init__(self, site):
        self.site = site

    def save_data(self,data):
        headers = data[0].keys()
        with open("news_data.csv", 'w') as out_file:
            dict_writer = csv.DictWriter(out_file,headers)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    def scrape(self):
        news_list = []
        r = urllib.request.urlopen(self.site)
        html = r.read()
        parser = "html.parser"
        sp = BeautifulSoup(html,parser)
        section = sp.find('section',class_="mainbox")
        article = section.find('article',class_="leftcol MT30")
        div_list = article.find('div',class_="listingholder")
        for div in div_list:
            news_dict = {}
            figure = div.find('figure')
            if figure != -1:
                news_dict['figure'] = figure.find('img').get('src')
            h2 = div.find('h2')
            if h2 != -1:
                news_dict['title'] = h2.select('a')[0].text
                news_dict['date'] = div.select('span')[0].text
            short_description = div.find('p')
            if short_description != -1:
                news_dict['short_desc'] = short_description.get_text()
            if news_dict:
                news_list.append(news_dict)
        self.save_data(news_list)

              
news = "https://www.loksatta.com/sampadkiya/agralekh/"
Scraper(news).scrape()
